def assess_impact(alert_text):
    alert = alert_text.lower()

    if "database" in alert:
        return "HIGH: Potential data integrity or availability risk"

    if "authentication" in alert or "login" in alert:
        return "HIGH: Potential security breach or unauthorized access"

    if "latency" in alert or "packet loss" in alert:
        return "MEDIUM: User experience degradation"

    if "cpu" in alert or "disk" in alert:
        return "MEDIUM: Resource exhaustion risk"

    if "backup" in alert or "maintenance" in alert:
        return "LOW: Routine operational event"

    return "UNKNOWN: Requires manual assessment"