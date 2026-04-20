import streamlit as st
import requests

# API endpoint
API_URL = "https://mist460-api-collins-c3dhhkhsapcse8dh.canadacentral-01.azurewebsites.net/api/course-sections"

st.title("Course Sections Finder")
st.write("Find sections offered this semester")

# Input fields
col1, col2 = st.columns(2)
with col1:
    subject_code = st.text_input("Subject Code (optional)", value="MIST", max_chars=10)
with col2:
    course_number = st.text_input("Course Number (optional)", value="460", max_chars=10)

# Search button
if st.button("Get Sections"):
    try:
        # Call API
        params = {}
        if subject_code:
            params["subject_code"] = subject_code
        if course_number:
            params["course_number"] = course_number
        
        response = requests.get(API_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            sections = data.get("data", [])
            
            if sections:
                st.success(f"Found {len(sections)} section(s)")
                
                # Display results
                for section in sections:
                    with st.expander(f"{section.get('SubjectCode', '')} {section.get('CourseNumber', '')} - Section {section.get('SectionNumber', '')}"):
                        st.write(f"**Title:** {section.get('Title', 'N/A')}")
                        st.write(f"**Instructor:** {section.get('InstructorName', 'N/A')}")
                        st.write(f"**CRN:** {section.get('CRN', 'N/A')}")
                        st.write(f"**Semester:** {section.get('SectionSemester', 'N/A')} {section.get('SectionYear', '')}")
                        st.write(f"**Remaining Openings:** {section.get('RemainingOpenings', 'N/A')}")
            else:
                st.info("No sections found")
        else:
            st.error(f"Error: {response.status_code}")
    
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")