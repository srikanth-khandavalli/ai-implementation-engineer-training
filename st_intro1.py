import streamlit as st

st.title("Profile Shortlist Application")
user_name = st.text_input("Candidate Name: ",value="Srikanth")
exp = st.slider("Experience Years: ", min_value=0,max_value=20,value=2)
role = st.selectbox("Target Role: ",["AI Implementation Engineer","ML Engineer","Data Engineer"])

st.write(f"Profile: {user_name}, {role} ({exp}) Yrs")

st.divider()
# st.subheader("Shortlisted candidates:")

# shortlisted_list=[]

# if st.button("Shortlist This Candidate"):
#     candidate_summary=f"{user_name} ({role})"
#     shortlisted_list.append(candidate_summary)

# st.write(f"Total Shortlisted candidates: {len(shortlisted_list)}")
# st.write(shortlisted_list)

if "shortlisted_list" not in st.session_state:
    st.session_state.shortlisted_list=[]

col1, col2 = st.columns([1,1])


with col1:
    if st.button("Shortlist this candidate", type = "primary"):
        candidate_summary=f"{user_name} ({role})"
        st.session_state.shortlisted_list.append(candidate_summary)

with col2:
    if st.button("Clear candiate list"):
        st.session_state.shortlisted_list=[]


st.write(f"Total Shortlisted: {len(st.session_state.shortlisted_list)}")
for idx, candidate in enumerate(st.session_state.shortlisted_list, 1):
    st.write(f"{idx}. {candidate}")