import streamlit as st

st.title("Interactive Playground")

user_name = st.text_input("Candidate Name:", value="Srikanth")
experience = st.slider("Years of Experience:", min_value=0, max_value=20, value=5)
role = st.selectbox("Target Role:", ["AI Implementation Engineer", "ML Engineer", "Data Engineer", "AI Architect"])

st.write(f"**Profile:** {user_name} | {role} ({experience} yrs exp)")

# # -------------------------------------------------------------
# # THE TRAP: A standard Python variable
# # -------------------------------------------------------------
# st.divider()
# st.subheader("Shortlisted Candidates")

# shortlisted_list = []  # ⚠️ Resets to empty on every rerun!

# if st.button("Shortlist This Candidate"):
#     candidate_summary = f"{user_name} ({role})"
#     shortlisted_list.append(candidate_summary)

# # Display shortlisted candidates
# st.write(f"Total Shortlisted: **{len(shortlisted_list)}**")
# st.write(shortlisted_list)

# -------------------------------------------------------------
# THE FIX: Session State Initialization & Persistence
# -------------------------------------------------------------
if "shortlisted_candidates" not in st.session_state:
    st.session_state.shortlisted_candidates = []

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Shortlist This Candidate", type="primary"):
        candidate_summary = f"{user_name} ({role}, {experience} yrs)"
        st.session_state.shortlisted_candidates.append(candidate_summary)

with col2:
    if st.button("Clear List"):
        st.session_state.shortlisted_candidates = []

# Display persistent candidates
st.write(f"Total Shortlisted: **{len(st.session_state.shortlisted_candidates)}**")
for idx, candidate in enumerate(st.session_state.shortlisted_candidates, 1):
    st.write(f"{idx}. {candidate}")