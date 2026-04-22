from fastapi import APIRouter, HTTPException
from get_db_connection import get_db_connection

router = APIRouter()

@router.get("/has-student-met-prerequisites")
def has_student_met_prerequisites(student_id: int, subject_code: str, course_number: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(
            "EXEC procHasStudentMetPrerequisitesForCourse @StudentID=%s, @SubjectCode=%s, @CourseNumber=%s",
            (student_id, subject_code, course_number)
        )
        missing = cursor.fetchall()
        conn.close()
        return {
            "met_prerequisites": len(missing) == 0,
            "missing_prerequisites": missing
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))