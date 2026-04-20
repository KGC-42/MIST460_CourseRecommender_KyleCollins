from get_db_connection import get_db_connection
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import os
import json
from dotenv import load_dotenv

load_dotenv()

def create_embeddings_for_chunks():
    conn = get_db_connection()
    cursor = conn.cursor(as_dict=True)

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)

    cursor.execute("EXEC procGetAllCourses")
    all_courses = cursor.fetchall()

    for each_course in all_courses:
        course_id = each_course['CourseID']
        course_description = each_course['CourseDescription']

        chunks_for_each_course = text_splitter.split_text(course_description)
        embeddings_for_chunks = embedding_model.embed_documents(chunks_for_each_course)

        for course_chunk, chunk_embedding in zip(chunks_for_each_course, embeddings_for_chunks):
            embedding_json = json.dumps(chunk_embedding)
            cursor.execute(
                "EXEC procInsertChunk @ChunkText=%s, @Embedding=%s, @CourseID=%s",
                (course_chunk, embedding_json, course_id)
            )

        print(f"Embeddings created for CourseID: {course_id}")

    conn.commit()
    cursor.close()
    conn.close()
    print("All embeddings created and stored in the database.")

if __name__ == "__main__":
    create_embeddings_for_chunks()