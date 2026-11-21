"""Transparent rule-based feedback, with optional AI explanation analysis."""
import os

RUBRIC = [
    "Scope the issue before making disruptive changes",
    "Gather relevant diagnostic evidence",
    "Explain a plausible, safe troubleshooting plan",
    "Adapt when new information is introduced",
]

def evaluate(history, reasoning, solution, follow_up_answer, api_key=""):
    """Return an evidence-focused report. No automated hiring decisions."""
    observations = []
    if "Check nearby devices" in history:
        observations.append("Checked whether the issue affects other users.")
    if "Inspect Wi-Fi status" in history:
        observations.append("Inspected the affected laptop's connection state.")
    if "Run adapter diagnostics" in history:
        observations.append("Collected adapter and authentication evidence.")
    if "Restart office router" in history:
        observations.append("Restarted a shared router; review whether this was necessary and appropriately scoped.")
    if not observations:
        observations.append("No diagnostic actions were recorded.")
    report = {
        "source": "Rule-based review",
        "observations": observations,
        "rubric": RUBRIC,
        "analysis": "Review the candidate's written reasoning and proposed next steps alongside their recorded actions. No hiring recommendation is generated.",
    }
    key = api_key or os.getenv("OPENAI_API_KEY", "")
    if not key:
        return report
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        prompt = f"""You are reviewing a fictional entry-level IT support simulation for a HUMAN reviewer.
Use only the evidence provided. Evaluate against these job-related criteria: {RUBRIC}.
Give 2-4 concise bullets for demonstrated strengths, gaps/risks, and evidence from the actual words/actions.
Do not infer personality, protected traits, or make a hiring decision. Do not assign a candidate ranking.
Actions (in order): {history}
Initial reasoning: {reasoning}
Proposed resolution: {solution}
Response to follow-up: {follow_up_answer}
"""
        response = client.responses.create(model="gpt-4.1-mini", input=prompt, max_output_tokens=400)
        report["analysis"] = response.output_text
        report["source"] = "AI-assisted review (human verification required)"
    except Exception as exc:
        report["analysis"] = "AI was unavailable; showing the rule-based review instead. Check your API key, connectivity, model access, and billing."
        report["source"] = "Rule-based fallback"
        report["error_type"] = type(exc).__name__
    return report
