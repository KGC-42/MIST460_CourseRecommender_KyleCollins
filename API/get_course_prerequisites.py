from fastapi import APIRouter, HTTPException
from get_db_connection import get_db_connection

router = APIRouter()

@router.get("/course-prerequisites")
def get_course_prerequisites(subject_code: str = None, course_number: str = None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(
            "EXEC procGetCoursePrerequisites @SubjectCode=%s, @CourseNumber=%s",
            (subject_code, course_number)
        )
        data = cursor.fetchall()
        conn.close()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))