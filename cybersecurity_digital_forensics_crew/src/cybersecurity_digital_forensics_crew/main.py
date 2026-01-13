#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from cybersecurity_digital_forensics_crew.crew import (
    CybersecurityDigitalForensicsCrew
)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew with explicit, security-relevant inputs.
    """
    inputs = {
        "case_id": f"CASE-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        "timeframe": "last_24_hours",
        "environment_context": "enterprise_windows_domain"
    }

    try:
        CybersecurityDigitalForensicsCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"Error while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "case_id": "TRAINING-CASE",
        "environment_context": "training_environment"
    }

    try:
        CybersecurityDigitalForensicsCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"Error while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CybersecurityDigitalForensicsCrew().crew().replay(
            task_id=sys.argv[1]
        )
    except Exception as e:
        raise Exception(f"Error while replaying the crew: {e}")


def test():
    """
    Test the crew execution and return evaluation results.
    """
    inputs = {
        "case_id": "TEST-CASE",
        "environment_context": "test_environment"
    }

    try:
        CybersecurityDigitalForensicsCrew().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"Error while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with a trigger payload (e.g., from SOAR or webhook).
    """
    import json

    if len(sys.argv) < 2:
        raise Exception(
            "No trigger payload provided. Please provide JSON payload as argument."
        )

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "case_id": trigger_payload.get("case_id", "TRIGGERED-CASE"),
        "environment_context": trigger_payload.get(
            "environment_context", "unknown"
        )
    }

    try:
        return CybersecurityDigitalForensicsCrew().crew().kickoff(
            inputs=inputs
        )
    except Exception as e:
        raise Exception(
            f"Error while running the crew with trigger: {e}"
        )