"""
Log Analyzer
------------
Parses logs and extracts security-relevant events.
No assumptions, no enrichment beyond evidence.
"""

def analyze_logs(log_entries: list):
    findings = []

    for entry in log_entries:
        message = entry.get("message", "").lower()

        if any(k in message for k in ["failed login", "authentication failure"]):
            findings.append({
                "timestamp": entry.get("timestamp"),
                "type": "authentication_failure",
                "description": entry.get("message"),
                "source": entry.get("source")
            })

        if any(k in message for k in ["process started", "powershell", "cmd.exe"]):
            findings.append({
                "timestamp": entry.get("timestamp"),
                "type": "process_execution",
                "description": entry.get("message"),
                "source": entry.get("source")
            })

        if "connection" in message and "denied" in message:
            findings.append({
                "timestamp": entry.get("timestamp"),
                "type": "network_block",
                "description": entry.get("message"),
                "source": entry.get("source")
            })

    return findings
