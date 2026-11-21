
"""MindFrame evidence-based candidate evaluator."""

import os
from openai import OpenAI

RUBRIC = [
    "Scopes the issue before making disruptive changes",
    "Gathers relevant diagnostic evidence",
    "Explains a plausible and safe troubleshooting plan",
    "Adapts when new information is introduced",
]


def evaluate(history, results, reasoning, solution, follow_up_answer, api_key=""):
    """Analyze observable simulation evidence without making hiring decisions."""

    observations = []

    for action, result in zip(history, results):
        if action == "Check nearby devices":
            observations.append({
                "observation": "Investigated whether the issue affected multiple employees.",
                "evidence": result,
            })

        elif action == "Inspect Wi-Fi status":
            observations.append({
                "observation": "Inspected the affected laptop's connection state.",
                "evidence": result,
            })

        elif action == "Run adapter diagnostics":
            observations.append({
                "observation": "Collected wireless adapter and authentication evidence.",
                "evidence": result,
            })

        elif action == "Restart office router":
            observations.append({
                "observation": "Restarted shared network equipment.",
                "evidence": result,
            })

    if not observations:
        observations.append({
            "observation": "No diagnostic actions were recorded.",
            "evidence": "No diagnostic results available.",
        })

    report = {
        "source": "Rule-based review",
        "observations": observations,
        "rubric": RUBRIC,
        "analysis": (
            "Review the candidate's written explanations alongside their "
            "recorded actions. No hiring recommendation is generated."
        ),
    }

    key = api_key or os.getenv("OPENAI_API_KEY", "")

    if not key:
        return report

    try:
        client = OpenAI(api_key=key)

        prompt = f"""
You are MindFrame, an assistant supporting a human reviewer
of a fictional entry-level IT support simulation.

Analyze only the evidence provided below.

REVIEW CRITERIA:
{RUBRIC}

DIAGNOSTIC ACTIONS AND RESULTS:
{list(zip(history, results))}

CANDIDATE REASONING:
{reasoning}

PROPOSED RESOLUTION:
{solution}

RESPONSE TO NEW INFORMATION:
{follow_up_answer}

Return your review under these headings:

OBSERVED STRENGTHS
Identify actions or explanations supported by evidence.

AREAS TO EXPLORE
Identify missing steps, unclear reasoning, or possible risks.

EVIDENCE
Connect each observation to an actual action, result, or candidate statement.

FOLLOW-UP QUESTIONS
Suggest two useful questions for a human interviewer.

LIMITATIONS
Mention important information that cannot be determined from this simulation.

RULES:
- Never invent actions or evidence.
- Distinguish observed behavior from assumptions.
- Do not infer personality, intelligence, or protected traits.
- Do not rank, hire, or reject the candidate.
- Do not treat one simulation as a complete measure of ability.
- Use clear, professional language.
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            max_output_tokens=650,
        )

        report["analysis"] = response.output_text
        report["source"] = "AI-assisted review — human verification required"

    except Exception as exc:
        report["analysis"] = (
            "AI analysis was unavailable. The rule-based observations "
            "are displayed instead. Check API configuration and access."
        )
        report["source"] = "Rule-based fallback"
        report["error_type"] = type(exc).__name__

    return report
