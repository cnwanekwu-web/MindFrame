"""Fictional IT support scenario and deterministic branching."""
TICKET = {
    "id": "IT-1042",
    "employee": "Jordan M. (fictional)",
    "message": "My laptop won't connect to OfficeNet Wi-Fi. I have a meeting soon. Can you help?",
}

TOOLS = {
    "Check nearby devices": "Three coworkers can connect to OfficeNet. The problem appears limited to Jordan's laptop.",
    "Inspect Wi-Fi status": "Wi-Fi is enabled. OfficeNet is visible, but the laptop reports 'Can't connect to this network'.",
    "Run adapter diagnostics": "The wireless adapter is functioning. The saved OfficeNet profile reports an authentication error.",
    "Restart office router": "The office router restarts. Other employees briefly lose connectivity; Jordan still cannot connect.",
}

def follow_up(history):
    """Choose a follow-up from actions actually performed."""
    if "Restart office router" in history:
        return "After the router restart, three coworkers report losing their connection. How would you respond, and what would you do differently?"
    if "Run adapter diagnostics" in history:
        return "You discover an authentication error in the saved Wi-Fi profile. How would you safely confirm the cause and restore access?"
    if "Check nearby devices" in history:
        return "Other employees can connect normally. What does that tell you about the likely scope, and what would you check next?"
    return "Jordan says their phone connects to OfficeNet, but their laptop does not. What would you investigate next?"




Test gemini:


import streamlit as st
from google import genai

# Read our private API key
api_key = st.secrets["GEMINI_API_KEY"]

# Connect to Gemini
client = genai.Client(api_key=api_key)


# A sample response from a fictional candidate

# Testing whether Gemini recognizes a meaningless response
candidate_response = "ahsklksjs;"


prompt = f"""
You are evaluating a candidate in an IT support simulation.

Candidate response:
{candidate_response}

Determine whether the response is meaningful and
relevant to troubleshooting.


Evaluate:
1. Relevance to the problem
2. Technical reasoning
3. Troubleshooting approach

Feedback guidelines:
1. Use professional, neutral, and encouraging language.
2. Evaluate only the skills demonstrated in the response.
3. Do not make assumptions about the candidate's
   intelligence, personality, or professionalism.
4. If a response is meaningless, explain that there
   is insufficient evidence to evaluate their skills.
5. Recognize relevant reasoning even when the
   candidate's answer is short or unconventional.
6. Explain what the candidate demonstrated well
   and what could be improved.
7. Do not make hiring recommendations or decisions.
"""


response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)


print("\nMINDFRAME AI FEEDBACK:\n")
print(response.text)
