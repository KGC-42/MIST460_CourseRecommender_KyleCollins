import streamlit as st
import requests

API_URL = "https://mist460-api-collins-c3dhhkhsapcse8dh.canadacentral-01.azurewebsites.net/api/course-prerequisites"

st.title("Course Prerequisites Finder")
st.write("Find prerequisites for any course")

col1, col2 = st.columns(2)
with col1:
    subject_code = st.text_input("Subject Code", value="MIST", max_chars=10)
with col2:
    course_number = st.text_input("Course Number", value="460", max_chars=10)

if st.button("Get Prerequisites"):
    if subject_code and course_number:
        try:
            response = requests.get(
                API_URL,
                params={
                    "subject_code": subject_code,
                    "course_number": course_number
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                prerequisites = data.get("data", [])
                
                if prerequisites:
                    st.success(f"Found {len(prerequisites)} prerequisite(s)")
                    st.table(prerequisites)
                else:
                    st.info("No prerequisites found for this course")
            else:
                st.error(f"Error: {response.status_code}")
        
        except Exception as e:
            st.error(f"Failed to connect to API: {str(e)}")
    else:
        st.warning("Please enter both subject code and course number")