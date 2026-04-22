import streamlit as st
import requests

# API endpoint
API_URL = "https://mist460-api-collins-c3dhhkhsapcse8dh.canadacentral-01.azurewebsites.net/api/course-recommendations"

st.title("Course Recommendations for a Job")
st.write("Paste a job description to get the top 5 most relevant courses from the catalog.")

job_description = st.text_area(
    "Job Description",
    height=220,
    placeholder="e.g. Data engineer building ETL pipelines in Python and SQL on Azure. "
                "Experience with machine learning, relational databases, and cloud data warehouses."
)

if st.button("Recommend Courses"):
    if not job_description or not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        try:
            with st.spinner("Embedding job description and scoring courses..."):
                response = requests.get(
                    API_URL,
                    params={"job_description": job_description, "top_k": 5},
                    timeout=60
                )

            if response.status_code == 200:
                data = response.json().get("data", [])

                if not data:
                    st.info("No course recommendations found.")
                else:
                    st.success(f"Top {len(data)} matching courses:")
                    for rank, course in enumerate(data, start=1):
                        header = (
                            f"#{rank} — {course.get('SubjectCode', '')} {course.get('CourseNumber', '')}: "
                            f"{course.get('Title', '')}  (similarity: {course.get('similarity', 0):.3f})"
                        )
                        with st.expander(header, expanded=(rank == 1)):
                            st.write(f"**Credits:** {course.get('Credits', 'N/A')}")
                            st.write(f"**Description:** {course.get('CourseDescription', 'N/A')}")
                            best_chunk = course.get("best_matching_chunk")
                            if best_chunk:
                                st.caption("Best matching chunk from the course description:")
                                st.markdown(f"> {best_chunk}")
            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Failed to connect to API: {str(e)}")
