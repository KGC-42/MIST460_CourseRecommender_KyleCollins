import json
import math
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query
from openai import OpenAI

from get_db_connection import get_db_connection

load_dotenv()

router = APIRouter()

EMBEDDING_MODEL = "text-embedding-3-small"


def _cosine_similarity(a, b):
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for x, y in zip(a, b):
        dot += x * y
        norm_a += x * x
        norm_b += y * y
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))


def _parse_embedding(raw):
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8")
    if isinstance(raw, str):
        return json.loads(raw)
    return raw


@router.get("/course-recommendations")
def get_course_recommendations(
    job_description: str = Query(..., min_length=1, description="Job description to match against course catalog"),
    top_k: int = Query(5, ge=1, le=20),
    semester: str | None = Query(None, description="Optional semester filter (e.g. 'Spring')"),
    year: int | None = Query(None, description="Optional year filter (e.g. 2026)")
):
    try:
        openai_client = OpenAI()
        embedding_response = openai_client.embeddings.create(
            input=job_description,
            model=EMBEDDING_MODEL
        )
        query_embedding = embedding_response.data[0].embedding

        conn = get_db_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(
            "EXEC procGetCourseRecommendationsForSelectedJob "
            "@Semester=%s, @Year=%s",
            (semester, year)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"data": []}

        courses_by_id = {}
        for row in rows:
            course_id = row["CourseID"]
            chunk_embedding = _parse_embedding(row["Embedding"])
            similarity = _cosine_similarity(query_embedding, chunk_embedding)

            course = courses_by_id.get(course_id)
            if course is None:
                course = {
                    "CourseID": course_id,
                    "SubjectCode": row["SubjectCode"],
                    "CourseNumber": row["CourseNumber"],
                    "Title": row["Title"],
                    "CourseDescription": row["CourseDescription"],
                    "Credits": None,
                    "similarity": similarity,
                    "best_matching_chunk": row["Evidence"],
                    "_section_ids": set(),
                    "sections": [],
                }
                courses_by_id[course_id] = course
            elif similarity > course["similarity"]:
                course["similarity"] = similarity
                course["best_matching_chunk"] = row["Evidence"]

            section_id = row.get("SectionID")
            if section_id is not None and section_id not in course["_section_ids"]:
                course["_section_ids"].add(section_id)
                course["sections"].append({
                    "SectionID": section_id,
                    "SectionSemester": row["SectionSemester"],
                    "SectionYear": row["SectionYear"],
                    "RemainingOpenings": row["RemainingOpenings"],
                    "CRN": row["CRN"],
                    "SectionNumber": row["SectionNumber"],
                })

        for course in courses_by_id.values():
            course["similarity"] = round(course["similarity"], 4)
            course.pop("_section_ids", None)

        ranked = sorted(courses_by_id.values(), key=lambda c: c["similarity"], reverse=True)
        return {"data": ranked[:top_k]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
