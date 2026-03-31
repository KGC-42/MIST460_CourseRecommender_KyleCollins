from fastapi import APIRouter

router = APIRouter()

@router.get("/course-sections")
def get_course_sections(subject_code: str = None, course_number: str = None):
    """Get sections for a specific course"""
    return {
        "data": [
            {"SubjectCode": "MIST", "CourseNumber": "460", "Title": "Database Management", "Instructor": "Dr. Surendra"}
        ]
    }

@router.get("/course-prerequisites")
def get_course_prerequisites(subject_code: str, course_number: str):
    """Get prerequisites for a course"""
    return {
        "data": [
            {"PrerequisiteTitle": "Introduction to Programming", "SubjectCode": "CS", "CourseNumber": "101"}
        ]
    }