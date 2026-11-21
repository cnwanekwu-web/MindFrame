"""Employer-facing evidence report (fictional demo)."""
import streamlit as st

def show_report(data):
    st.header("Employer review dashboard")
    st.caption("Demo candidate · Fictional scenario · Human review required")
    st.subheader("Decision timeline")
    for number, action in enumerate(data["history"], start=1):
        st.write(f"**{number}. {action}**")
        st.caption(data["results"][number - 1])
    st.subheader("Candidate's own words")
    st.write("**Reasoning:**", data["reasoning"])
    st.write("**Proposed resolution:**", data["solution"])
    st.write("**Adaptive challenge:**", data["challenge"])
    st.write("**Response:**", data["follow_answer"])
    st.subheader("Review observations")
    st.caption(data["report"]["source"])
    for item in data["report"]["observations"]:
        st.write("•", item)
    st.write("**Reasoning analysis**")
    st.write(data["report"]["analysis"])
    with st.expander("Job-related review rubric"):
        for criterion in data["report"]["rubric"]:
            st.write("•", criterion)
    st.info("MindFrame supports evidence-based review. A person makes all employment decisions; the AI does not determine suitability or rank candidates.")
