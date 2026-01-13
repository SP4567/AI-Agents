"""
Volatility Runner
-----------------
Runs Volatility memory analysis in read-only mode.
"""

import subprocess

def run_volatility(memory_image: str, plugin: str):
    try:
        result = subprocess.run(
            ["volatility", "-f", memory_image, plugin],
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "plugin": plugin,
            "output": result.stdout.splitlines()
        }

    except Exception as e:
        return {"error": str(e)}
