
"""MindFrame employer-facing evidence report."""

import streamlit as st


def show_report(data):

    st.header("Employer Review Dashboard")
    st.caption(
        "Fictional candidate demonstration · Human review required"
    )

    st.divider()

    st.subheader("1. Simulation overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Diagnostic actions", len(data["history"]))

    with col2:
        st.metric("Evidence records", len(data["results"]))

    st.subheader("2. Candidate decision timeline")

    for number, (action, result) in enumerate(
        zip(data["history"], data["results"]), start=1
    ):
        with st.expander(f"{number}. {action}", expanded=False):
            st.write("**Diagnostic result:**")
            st.write(result)

    st.subheader("3. Candidate explanations")

    with st.expander("View candidate's reasoning"):
        st.write(data["reasoning"])

    with st.expander("View proposed resolution"):
        st.write(data["solution"])

    with st.expander("View adaptive follow-up"):
        st.write(data["challenge"])
        st.write("**Candidate response:**")
        st.write(data["follow_answer"])

    st.divider()

    st.subheader("4. Evidence-based observations")
    st.caption(data["report"]["source"])

    for item in data["report"]["observations"]:
        with st.container(border=True):
            st.write(f"**{item['observation']}**")
            st.caption("Supporting diagnostic evidence")
            st.write(item["evidence"])

    st.subheader("5. AI analysis")
    st.markdown(data["report"]["analysis"])

    with st.expander("View job-related review criteria"):
        for criterion in data["report"]["rubric"]:
            st.write(f"• {criterion}")

    st.divider()

    st.subheader("6. Reviewer feedback")

    with st.form("reviewer_feedback_form"):
        rating = st.selectbox(
            "How accurate was the AI's analysis?",
            [
                "Accurate",
                "Partially accurate",
                "Inaccurate",
            ],
        )

        comments = st.text_area(
            "What should MindFrame improve?",
            placeholder=(
                "Describe an inaccurate observation or "
                "suggest an improvement..."
            ),
        )

        submitted = st.form_submit_button(
            "Submit reviewer feedback"
        )

    if submitted:
        if not comments.strip():
            st.warning("Please enter feedback before submitting.")
        else:
            feedback = {
                "rating": rating,
                "comments": comments.strip(),
            }

            st.session_state["reviewer_feedback"] = feedback

            st.success("Reviewer feedback recorded for this session.")

    if st.session_state.get("reviewer_feedback"):
        feedback = st.session_state["reviewer_feedback"]

        with st.expander("View submitted feedback"):
            st.write("**Rating:**", feedback["rating"])
            st.write("**Comments:**", feedback["comments"])

    st.divider()

    st.info(
        "MindFrame provides evidence to support human review. "
        "It does not determine candidate suitability, rank candidates, "
        "or make employment decisions."
    )
