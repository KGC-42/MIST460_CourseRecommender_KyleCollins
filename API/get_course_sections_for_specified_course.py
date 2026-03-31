from fastapi import APIRouter, HTTPException
from get_db_connection import get_db_connection

router = APIRouter()

@router.get("/course-sections")
def get_course_sections_for_specified_course(subject_code: str = None, course_number: str = None):
    """Get sections for a specific course offered this semester"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "EXEC procGetCourseSectionsForSpecifiedCourse @SubjectCode=?, @CourseNumber=?",
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