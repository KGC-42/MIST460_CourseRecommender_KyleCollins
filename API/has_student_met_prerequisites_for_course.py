from fastapi import APIRouter, HTTPException
from get_db_connection import get_db_connection

router = APIRouter()

@router.get("/has-student-met-prerequisites")
def has_student_met_prerequisites_for_course(student_id: int, subject_code: str, course_number: str):
    """Check if student has met prerequisites for a course"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "EXEC procHasStudentMetPrerequisitesForCourse @StudentID=?, @SubjectCode=?, @CourseNumber=?",
            (student_id, subject_code, course_number)
        )
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        conn.close()
        
        # If results is empty, student met all prerequisites
        if len(results) == 0:
            return {
                "met_prerequisites": True,
                "missing_prerequisites": []
            }
        else:
            return {
                "met_prerequisites": False,
                "missing_prerequisites": results
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))