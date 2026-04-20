import pyodbc
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# LangChain text splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load env variables
load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_db_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=YOUR_SERVER_NAME;"
        "DATABASE=YOUR_DATABASE_NAME;"
        "Trusted_Connection=yes;"
    )


def get_embeddings_from_openai(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def create_embeddings_for_chunks():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 🔹 Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    # 🔹 Get courses
    cursor.execute("EXEC procGetAllCourses")
    courses = cursor.fetchall()

    for course in courses:
        course_id = course.CourseID
        course_text = course.CourseDescription

        print(f"Processing CourseID: {course_id}")

        # 🔹 Split into smaller chunks
        split_chunks = text_splitter.split_text(course_text)

        for chunk in split_chunks:
            # 🔹 Generate embedding
            embedding = get_embeddings_from_openai(chunk)

            # 🔹 Convert to binary
            embedding_bytes = json.dumps(embedding).encode('utf-8')

            # 🔹 Insert into DB
            cursor.execute(
                "EXEC procInsertChunk ?, ?, ?",
                chunk,
                embedding_bytes,
                course_id
            )

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_embeddings_for_chunks()