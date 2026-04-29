from get_db_connection import get_db_connection
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE = 500
CHUNK_OVERLAP = 20
EMBEDDING_MODEL = "text-embedding-3-small"


def split_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        if end >= text_len:
            chunks.append(text[start:].strip())
            break

        break_point = text.rfind(' ', start, end)
        if break_point == -1 or break_point <= start:
            break_point = end

        chunks.append(text[start:break_point].strip())
        start = max(break_point - chunk_overlap, start + 1)

    return [c for c in chunks if c]


def create_embeddings_for_chunks():
    conn = get_db_connection()
    cursor = conn.cursor(as_dict=True)

    client = OpenAI()

    cursor.execute("EXEC procGetAllCourses")
    all_courses = cursor.fetchall()

    for each_course in all_courses:
        course_id = each_course['CourseID']
        course_description = each_course['CourseDescription']

        chunks_for_each_course = split_text(course_description)
        if not chunks_for_each_course:
            continue

        response = client.embeddings.create(
            input=chunks_for_each_course,
            model=EMBEDDING_MODEL
        )
        embeddings_for_chunks = [item.embedding for item in response.data]

        for course_chunk, chunk_embedding in zip(chunks_for_each_course, embeddings_for_chunks):
            embedding_vector_literal = json.dumps(chunk_embedding)
            cursor.execute(
                "EXEC procInsertChunk @ChunkText=%s, @Embedding=%s, @CourseID=%s",
                (course_chunk, embedding_vector_literal, course_id)
            )

        print(f"Embeddings created for CourseID: {course_id}")

    conn.commit()
    cursor.close()
    conn.close()
    print("All embeddings created and stored in the database.")

if __name__ == "__main__":
    create_embeddings_for_chunks()
