"""
Sandbox Runner
--------------
Interfaces with an external sandbox (Cuckoo / API).
NO local execution.
"""

def run_sandbox(sample_path: str):
    """
    Placeholder for sandbox integration.
    Expected to call isolated VM or remote API.
    """

    # This should be replaced with real sandbox API calls
    return {
        "network_activity": False,
        "file_modifications": False,
        "persistence": False,
        "process_tree": [],
        "note": "Static placeholder result – integrate real sandbox here"
    }
