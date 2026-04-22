import json
import math
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query
from langchain_openai import OpenAIEmbeddings

from get_db_connection import get_db_connection

load_dotenv()

router = APIRouter()

_embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


def _cosine_similarity(a, b):
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for x, y in zip(a, b):
        dot += x * y
        norm_a += x * x
        norm_b += y * y
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))


@router.get("/course-recommendations")
def get_course_recommendations(
    job_description: str = Query(..., min_length=1, description="Job description to match against course catalog"),
    top_k: int = Query(5, ge=1, le=20)
):
    try:
        query_embedding = _embedding_model.embed_query(job_description)

        conn = get_db_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute("EXEC procGetAllCourseChunks")
        chunks = cursor.fetchall()
        conn.close()

        if not chunks:
            return {"data": []}

        best_per_course = {}
        for chunk in chunks:
            course_id = chunk["CourseID"]
            chunk_embedding = json.loads(chunk["Embedding"])
            similarity = _cosine_similarity(query_embedding, chunk_embedding)

            existing = best_per_course.get(course_id)
            if existing is None or similarity > existing["similarity"]:
                best_per_course[course_id] = {
                    "CourseID": course_id,
                    "SubjectCode": chunk["SubjectCode"],
                    "CourseNumber": chunk["CourseNumber"],
                    "Title": chunk["Title"],
                    "CourseDescription": chunk["CourseDescription"],
                    "Credits": float(chunk["Credits"]) if chunk["Credits"] is not None else None,
                    "similarity": similarity,
                    "best_matching_chunk": chunk["ChunkText"],
                }

        ranked = sorted(best_per_course.values(), key=lambda x: x["similarity"], reverse=True)
        top = ranked[:top_k]

        for item in top:
            item["similarity"] = round(item["similarity"], 4)

        return {"data": top}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
