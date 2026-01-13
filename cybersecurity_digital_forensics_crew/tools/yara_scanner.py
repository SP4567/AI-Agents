"""
YARA Scanner
------------
Runs YARA rules safely via CLI.
Never executes samples.
"""

import subprocess

def run_yara(sample_path: str, rules_path: str = "rules/"):
    try:
        result = subprocess.run(
            ["yara", "-r", rules_path, sample_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        matches = []
        for line in result.stdout.splitlines():
            matches.append(line.strip())

        return matches

    except Exception as e:
        return {"error": str(e)}
