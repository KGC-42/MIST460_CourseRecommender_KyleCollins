from fastapi import APIRouter, HTTPException
from get_db_connection import get_db_connection

router = APIRouter()

@router.get("/course-prerequisites")
def get_course_prerequisites(subject_code: str = None, course_number: str = None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "EXEC procGetCoursePrerequisites @SubjectCode=?, @CourseNumber=?",
            (subject_code, course_number)
        )
        rows = cursor.fetchall()
        conn.close()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        data = [dict(zip(columns, row)) for row in rows]
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))