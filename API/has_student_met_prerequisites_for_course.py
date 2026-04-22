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
        rows = cursor.fetchall()
        conn.close()
        columns = [col[0] for col in cursor.description] if cursor.description else []
        missing = [dict(zip(columns, row)) for row in rows]
        return {
            "met_prerequisites": len(missing) == 0,
            "missing_prerequisites": missing
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))