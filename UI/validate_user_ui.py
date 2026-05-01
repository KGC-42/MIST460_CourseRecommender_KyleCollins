import streamlit as st
import requests

API_URL = "https://mist460-api-collins-c3dhhkhsapcse8dh.canadacentral-01.azurewebsites.net/api/validate-user"

st.title("Sign In")
st.write("Enter your email and password to access the Course Recommender.")

with st.form("login_form"):
    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Sign In")

if submitted:
    if not email or not password:
        st.warning("Please enter both email and password.")
    else:
        try:
            response = requests.post(
                API_URL,
                json={"username": email, "password": password},
                timeout=30,
            )

            if response.status_code != 200:
                st.error(f"Error {response.status_code}: {response.text}")
            else:
                result = response.json()
                if result.get("valid"):
                    st.session_state["user_id"] = result.get("AppUserID")
                    st.session_state["full_name"] = result.get("FullName")
                    st.success(f"Welcome, {result.get('FullName') or 'user'}!")
                    st.rerun()
                else:
                    st.error(result.get("message") or "Invalid credentials")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
