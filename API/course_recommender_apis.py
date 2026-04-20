import streamlit as st
import importlib
import sys
import os

sys.path.append(os.path.dirname(__file__))

st.title("Course Recommender System")

api_end_point = st.selectbox(
    "Select a course recommendation functionality:",
    (
        "Get Course Sections for Specified Course",
        "Get Course Prerequisites",
        "Check Student Prerequisites"
    )
)

if api_end_point == "Get Course Sections for Specified Course":
    import get_course_sections_for_specified_course_ui
elif api_end_point == "Get Course Prerequisites":
    import get_course_prerequisites_ui
elif api_end_point == "Check Student Prerequisites":
    import has_student_met_prerequisites_for_course_ui