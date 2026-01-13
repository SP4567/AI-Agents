"""
Timeline Builder
----------------
Normalizes and sorts forensic events.
"""

from dateutil import parser

def build_timeline(events: list):
    timeline = []

    for event in events:
        try:
            timeline.append({
                "time": parser.parse(event["timestamp"]),
                "source": event.get("source", "unknown"),
                "description": event.get("description", "")
            })
        except Exception:
            continue

    return sorted(timeline, key=lambda x: x["time"])