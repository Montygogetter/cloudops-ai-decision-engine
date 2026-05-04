def calculate_priority_score(severity, confidence, alert_text):
    severity = severity.lower()
    alert_lower = alert_text.lower()

    score = 0

    # Severity weight
    if severity == "critical":
        score += 50
    elif severity == "high":
        score += 40
    elif severity == "medium":
        score += 25
    elif severity == "informational":
        score += 5
    elif severity == "false_positive":
        score += 0
    else:
        score += 10

    # Confidence weight
    score += confidence * 20

    # Context risk indicators
    if "production" in alert_lower or "prod" in alert_lower:
        score += 20

    if "database" in alert_lower:
        score += 15

    if "authentication" in alert_lower or "login" in alert_lower or "access denied" in alert_lower:
        score += 15

    if "failed" in alert_lower or "error" in alert_lower:
        score += 10

    if "latency" in alert_lower or "packet loss" in alert_lower:
        score += 10

    if "backup completed" in alert_lower or "scheduled backup" in alert_lower:
        score -= 15

    if "maintenance" in alert_lower:
        score -= 10

    return round(score, 2)