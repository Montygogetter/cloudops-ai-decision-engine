def recommend_action(severity, confidence, alert_text):
    severity = severity.lower()
    alert_lower = alert_text.lower()

    reason_flags = []

    if "production" in alert_lower or "prod" in alert_lower:
        reason_flags.append("production environment mentioned")

    if "authentication" in alert_lower or "access denied" in alert_lower:
        reason_flags.append("authentication or access issue detected")

    if "failed" in alert_lower or "error" in alert_lower:
        reason_flags.append("failure/error language detected")

    if severity == "critical":
        action = "Escalate immediately to on-call/cloud operations lead."
    elif severity == "high":
        action = "Investigate within the SLA window and correlate with related alerts."
    elif severity == "medium":
        action = "Monitor, correlate with related alerts, and review if repeated."
    else:
        action = "Suppress or log for trend analysis unless repeated."

    if confidence < 0.60:
        action += " Human review recommended due to low model confidence."

    reason = "Reason: " + "; ".join(reason_flags) if reason_flags else "Reason: Based on predicted severity and alert pattern."

    return action, reason