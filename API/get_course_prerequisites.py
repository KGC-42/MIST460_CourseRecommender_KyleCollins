from fastapi import APIRouter, HTTPException
from get_db_connection import get_db_connection

router = APIRouter()

@router.get("/course-prerequisites")
def get_course_prerequisites(subject_code: str, course_number: str):
    """Get prerequisites for a specific course"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "EXEC procGetCoursePrerequisites @SubjectCode=?, @CourseNumber=?",
            (subject_code, course_number)
        )
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        conn.close()
        return {"data": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))