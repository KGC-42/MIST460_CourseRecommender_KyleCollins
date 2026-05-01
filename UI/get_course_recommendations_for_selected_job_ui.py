import streamlit as st
import requests

API_BASE = "https://mist460-api-collins-c3dhhkhsapcse8dh.canadacentral-01.azurewebsites.net/api"
RECOMMENDATIONS_URL = f"{API_BASE}/course-recommendations"
JOBS_URL = f"{API_BASE}/jobs"

st.title("Course Recommendations for a Job")
st.write("Pick a job from the catalog to see the top 5 most relevant courses.")


@st.cache_data(ttl=300, show_spinner=False)
def load_jobs():
    response = requests.get(JOBS_URL, timeout=30)
    response.raise_for_status()
    return response.json().get("data", [])


try:
    jobs = load_jobs()
except Exception as e:
    st.error(f"Failed to load jobs: {e}")
    st.stop()

if not jobs:
    st.info("No jobs available in the catalog.")
    st.stop()

job_titles = [job.get("JobTitle", "") for job in jobs]
selected_title = st.selectbox("Job", options=job_titles, index=0)

selected_job = next((j for j in jobs if j.get("JobTitle") == selected_title), None)
selected_description = (selected_job or {}).get("JobDescription", "") or ""

with st.expander("Job description", expanded=False):
    st.write(selected_description or "_No description available._")

if st.button("Recommend Courses"):
    if not selected_description.strip():
        st.warning("This job has no description to match against.")
    else:
        try:
            with st.spinner("Embedding job description and scoring courses..."):
                response = requests.get(
                    RECOMMENDATIONS_URL,
                    params={"job_description": selected_description, "top_k": 5},
                    timeout=60,
                )

            if response.status_code != 200:
                st.error(f"Error {response.status_code}: {response.text}")
            else:
                data = response.json().get("data", [])

                if not data:
                    st.info("No course recommendations found.")
                else:
                    st.success(f"Top {len(data)} matching courses for {selected_title}:")
                    for rank, course in enumerate(data, start=1):
                        header = (
                            f"#{rank} - {course.get('SubjectCode', '')} {course.get('CourseNumber', '')}: "
                            f"{course.get('Title', '')}  (similarity: {course.get('similarity', 0):.3f})"
                        )
                        with st.expander(header, expanded=(rank == 1)):
                            st.write(f"**Credits:** {course.get('Credits', 'N/A')}")
                            st.write(f"**Description:** {course.get('CourseDescription', 'N/A')}")
                            best_chunk = course.get("best_matching_chunk")
                            if best_chunk:
                                st.caption("Best matching chunk from the course description:")
                                st.markdown(f"> {best_chunk}")

        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
