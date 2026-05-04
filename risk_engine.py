def simulate_risk(alert_text, severity, impact):
    alert = alert_text.lower()

    if severity == "critical" and "authentication" in alert:
        return "CRITICAL RISK: Potential unauthorized access → possible data breach"

    if severity == "critical" and "database" in alert:
        return "CRITICAL RISK: Data loss or service outage likely"

    if "latency" in alert or "packet loss" in alert:
        return "RISK: Degraded user experience → potential customer impact"

    if "cpu" in alert or "disk" in alert:
        return "RISK: Resource exhaustion → possible system slowdown or crash"

    if "backup" in alert or "maintenance" in alert:
        return "LOW RISK: Expected operational behavior"

    return "UNKNOWN RISK: Requires human evaluation"