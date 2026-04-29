import json
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query
from openai import OpenAI

from get_db_connection import get_db_connection

load_dotenv()

router = APIRouter()

EMBEDDING_MODEL = "text-embedding-3-small"


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
        embedding_vector_literal = json.dumps(query_embedding)

        conn = get_db_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(
            "EXEC procGetCourseRecommendationsForSelectedJob "
            "@JobDescription=%s, @Semester=%s, @Year=%s",
            (embedding_vector_literal, semester, year)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"data": []}

        courses_by_id = {}
        for row in rows:
            course_id = row["CourseID"]
            course = courses_by_id.get(course_id)
            if course is None:
                distance = float(row["Distance"])
                course = {
                    "CourseID": course_id,
                    "SubjectCode": row["SubjectCode"],
                    "CourseNumber": row["CourseNumber"],
                    "Title": row["Title"],
                    "CourseDescription": row["CourseDescription"],
                    "Credits": float(row["Credits"]) if row.get("Credits") is not None else None,
                    "similarity": round(1.0 - distance, 4),
                    "best_matching_chunk": row["Evidence"],
                    "sections": [],
                }
                courses_by_id[course_id] = course

            if row.get("SectionID") is not None:
                course["sections"].append({
                    "SectionID": row["SectionID"],
                    "SectionSemester": row["SectionSemester"],
                    "SectionYear": row["SectionYear"],
                    "RemainingOpenings": row["RemainingOpenings"],
                    "CRN": row["CRN"],
                    "SectionNumber": row["SectionNumber"],
                })

        ranked = sorted(courses_by_id.values(), key=lambda c: c["similarity"], reverse=True)
        return {"data": ranked[:top_k]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
