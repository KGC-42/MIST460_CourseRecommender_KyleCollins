import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))

UI_DIR = os.path.dirname(__file__)


def _run_page(filename):
    with open(os.path.join(UI_DIR, filename), encoding="utf-8") as f:
        exec(f.read(), globals())


if "user_id" not in st.session_state:
    _run_page("validate_user_ui.py")
    st.stop()

st.title("Course Recommender System")

with st.sidebar:
    st.write(f"**Signed in as:** {st.session_state.get('full_name') or 'User'}")
    st.write(f"**User ID:** {st.session_state.get('user_id')}")
    if st.button("Sign Out"):
        for key in ("user_id", "full_name"):
            st.session_state.pop(key, None)
        st.rerun()

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
    _run_page("get_course_sections_for_specified_course_ui.py")
elif api_end_point == "Get Course Prerequisites":
    _run_page("get_course_prerequisites_ui.py")
elif api_end_point == "Check Student Prerequisites":
    _run_page("has_student_met_prerequisites_for_course_ui.py")
elif api_end_point == "Get Course Recommendations for Selected Job":
    _run_page("get_course_recommendations_for_selected_job_ui.py")
elif api_end_point == "Get All Jobs":
    _run_page("get_all_jobs_ui.py")
