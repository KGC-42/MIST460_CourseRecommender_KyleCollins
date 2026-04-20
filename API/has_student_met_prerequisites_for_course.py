import streamlit as st
import requests

API_URL = "https://mist460-api-collins-c3dhhkhsapcse8dh.canadacentral-01.azurewebsites.net/api/has-student-met-prerequisites"

st.title("Student Prerequisites Checker")
st.write("Check if a student has met prerequisites for a course")

col1, col2, col3 = st.columns(3)
with col1:
    student_id = st.number_input("Student ID", min_value=1, value=1)
with col2:
    subject_code = st.text_input("Subject Code", value="MIST", max_chars=10)
with col3:
    course_number = st.text_input("Course Number", value="460", max_chars=10)

if st.button("Check Prerequisites"):
    if subject_code and course_number:
        try:
            response = requests.get(
                API_URL,
                params={
                    "student_id": student_id,
                    "subject_code": subject_code,
                    "course_number": course_number
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                met = data.get("met_prerequisites", False)
                missing = data.get("missing_prerequisites", [])
                
                if met:
                    st.success(f"Student {student_id} HAS MET all prerequisites for {subject_code} {course_number}!")
                else:
                    st.error(f"Student {student_id} has NOT met all prerequisites for {subject_code} {course_number}")
                    if missing:
                        st.write("**Missing Prerequisites:**")
                        st.table(missing)
            else:
                st.error(f"Error: {response.status_code}")
        
        except Exception as e:
            st.error(f"Failed to connect to API: {str(e)}")
    else:
        st.warning("Please enter subject code and course number")