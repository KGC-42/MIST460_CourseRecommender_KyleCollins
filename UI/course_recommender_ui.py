import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))

st.title("Course Recommender System")

api_end_point = st.selectbox(
    "Select a course recommendation functionality:",
    (
        "Get Course Sections for Specified Course",
        "Get Course Prerequisites",
        "Check Student Prerequisites",
        "Get Course Recommendations for Selected Job",
        "Get All Jobs"
    )
)

if api_end_point == "Get Course Sections for Specified Course":
    exec(open(os.path.join(os.path.dirname(__file__), "get_course_sections_for_specified_course_ui.py")).read())
elif api_end_point == "Get Course Prerequisites":
    exec(open(os.path.join(os.path.dirname(__file__), "get_course_prerequisites_ui.py")).read())
elif api_end_point == "Check Student Prerequisites":
    exec(open(os.path.join(os.path.dirname(__file__), "has_student_met_prerequisites_for_course_ui.py")).read())
elif api_end_point == "Get Course Recommendations for Selected Job":
    exec(open(os.path.join(os.path.dirname(__file__), "get_course_recommendations_for_selected_job_ui.py")).read())
elif api_end_point == "Get All Jobs":
    exec(open(os.path.join(os.path.dirname(__file__), "get_all_jobs_ui.py")).read())