import streamlit as st
import requests

API_URL = "https://mist460-api-collins-c3dhhkhsapcse8dh.canadacentral-01.azurewebsites.net/api/jobs"

st.title("All Jobs")
st.write("Browse every job in the catalog")

if st.button("Load Jobs"):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            jobs = response.json().get("data", [])
            if jobs:
                st.success(f"Found {len(jobs)} job(s)")
                st.table(jobs)
            else:
                st.info("No jobs found")
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")
