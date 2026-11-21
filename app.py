"""MindFrame hackathon MVP — run with: python -m streamlit run app.py"""
import streamlit as st
from simulation import TICKET, TOOLS, follow_up
from evaluator import evaluate
from dashboard import show_report

st.set_page_config(page_title="MindFrame", page_icon="🧠", layout="centered")
st.markdown("""<style>
.block-container {max-width: 850px; padding-top: 2rem;}
h1 {color: #7953b2;}
div.stButton > button[kind=primary] {background-color: #7953b2; border-color: #7953b2;}
</style>""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.results = []
    st.session_state.report_data = None

st.title("🧠 MindFrame")
st.caption("Beyond the answer. See the potential. · Fictional hackathon demonstration")

if st.session_state.report_data:
    show_report(st.session_state.report_data)
    if st.button("Start a new simulation"):
        st.session_state.history = []
        st.session_state.results = []
        st.session_state.report_data = None
        st.rerun()
else:
    st.subheader(f"Support ticket #{TICKET['id']}")
    st.info(f"**{TICKET['employee']} writes:** {TICKET['message']}")
    st.write("**Your role:** You are an entry-level IT support technician. Investigate safely, explain what the evidence means, and propose your next step.")
    st.subheader("1. Investigate")
    st.write("Select a diagnostic action. You may run several checks; their order is recorded.")
    action = st.selectbox("Diagnostic tool", list(TOOLS.keys()))
    if st.button("Run diagnostic", type="primary"):
        st.session_state.history.append(action)
        st.session_state.results.append(TOOLS[action])
        st.rerun()
    if st.session_state.history:
        for index, (name, result) in enumerate(zip(st.session_state.history, st.session_state.results), start=1):
            with st.expander(f"{index}. {name}", expanded=index==len(st.session_state.history)):
                st.write(result)
        if st.button("Undo last action"):
            st.session_state.history.pop()
            st.session_state.results.pop()
            st.rerun()
        st.subheader("2. Explain your approach")
        with st.form("assessment_form"):
            reasoning = st.text_area("What have you learned from the evidence? Why did you choose these steps?", height=110)
            solution = st.text_area("What would you do next to safely resolve the issue?", height=110)
            challenge = follow_up(st.session_state.history)
            st.subheader("3. Adaptive follow-up")
            st.warning(challenge)
            follow_answer = st.text_area("How would you respond to this new information?", height=110)
            submitted = st.form_submit_button("Complete simulation and view report", type="primary")
        if submitted:
            if not all([reasoning.strip(), solution.strip(), follow_answer.strip()]):
                st.error("Please complete all three written explanations before submitting.")
            else:
                try:
                    api_key = st.secrets.get("OPENAI_API_KEY", "")
                except Exception:
                    api_key = ""
                with st.spinner("Preparing evidence-based review..."):
                    report = evaluate(st.session_state.history, st.session_state.results, reasoning, solution, follow_answer, api_key)
                st.session_state.report_data = {
                    "history": st.session_state.history.copy(),
                    "results": st.session_state.results.copy(),
                    "reasoning": reasoning, "solution": solution,
                    "challenge": challenge, "follow_answer": follow_answer,
                    "report": report,
                }
                st.rerun()
    else:
        st.caption("Run at least one diagnostic to unlock the written assessment and adaptive follow-up.")
