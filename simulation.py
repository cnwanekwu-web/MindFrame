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
