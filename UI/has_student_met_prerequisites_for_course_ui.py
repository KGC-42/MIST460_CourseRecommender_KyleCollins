import streamlit as st
import requests

API_URL = "https://mist460-api-collins-c3dhhkhsapcse8dh.canadacentral-01.azurewebsites.net/api/has-student-met-prerequisites"

st.title("Student Prerequisites Checker")

student_id = st.session_state.get("user_id")
full_name = st.session_state.get("full_name")

if not student_id:
    st.error("You must be signed in to check prerequisites.")
    st.stop()

st.write(f"Checking prerequisites for **{full_name or 'current user'}** (Student ID: {student_id}).")

col1, col2 = st.columns(2)
with col1:
    subject_code = st.text_input("Subject Code", value="MIST", max_chars=10)
with col2:
    course_number = st.text_input("Course Number", value="460", max_chars=10)

if st.button("Check Prerequisites"):
    if not (subject_code and course_number):
        st.warning("Please enter subject code and course number")
    else:
        try:
            response = requests.get(
                API_URL,
                params={
                    "student_id": student_id,
                    "subject_code": subject_code,
                    "course_number": course_number,
                },
                timeout=30,
            )

            if response.status_code != 200:
                st.error(f"Error: {response.status_code}")
            else:
                data = response.json()
                met = data.get("met_prerequisites", False)
                missing = data.get("missing_prerequisites", [])

                if met:
                    st.success(
                        f"Student {student_id} HAS MET all prerequisites for {subject_code} {course_number}."
                    )
                else:
                    st.error(
                        f"Student {student_id} has NOT met all prerequisites for {subject_code} {course_number}."
                    )
                    if missing:
                        st.write("**Missing Prerequisites:**")
                        st.table(missing)

        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
