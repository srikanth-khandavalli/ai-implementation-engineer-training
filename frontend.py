import requests
import streamlit as st

st.set_page_config(page_title="AI Candidate Extractor", page_icon="⚡", layout="centered")

st.title("⚡ Candidate Profile Extractor")
st.caption("Streamlit Frontend consuming an Asynchronous FastAPI Backend")

# Initialize session history for extracted records
if "history" not in st.session_state:
    st.session_state.history = []

FASTAPI_URL = "http://127.0.0.1:8000/extract"

# Input text area
sample_text = "Srikanth is a Senior Data Engineer at DataStackX with 9 years of experience in PySpark, SQL, and FastAPI."
user_input = st.text_area("Candidate Bio / Raw Profile:", value=sample_text, height=120)

col1, col2 = st.columns([1, 1])

with col1:
    submit_btn = st.button("Extract via FastAPI", type="primary")

with col2:
    clear_btn = st.button("Clear History")

if clear_btn:
    st.session_state.history = []
    st.rerun()

if submit_btn:
    if len(user_input.strip()) < 10:
        st.warning("Please enter at least 10 characters.")
    else:
        with st.spinner("Calling FastAPI microservice..."):
            try:
                # HTTP POST call to our local microservice
                payload = {"raw_text": user_input}
                response = requests.post(FASTAPI_URL, json=payload, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    st.success("Extraction Successful!")

                    # Persist record in session_state
                    st.session_state.history.append(data)

                    # Display formatted output
                    st.subheader("Extracted Result:")
                    st.json(data)
                else:
                    st.error(f"Backend returned HTTP {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI. Did you forget to run `uvicorn backend:app --reload`?")
            except Exception as e:
                st.error(f"Request failed: {str(e)}")

# Display historical submissions persisted in session state
if st.session_state.history:
    st.divider()
    st.subheader(f"Extracted Candidates Pool ({len(st.session_state.history)})")
    for idx, item in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{item.get('name')} — {item.get('company')}"):
            st.write(f"**Experience:** {item.get('experience_years')} years")
            st.write(f"**Skills:** {', '.join(item.get('skills', []))}")