def plan_prompt(question):
    return f"""
You are a research planner.
Break the following research question into 3–5 concrete sub-questions.

Question:
{question}

Sub-questions:
"""


def extract_prompt(text, question):
    return f"""
You are a technical research reader.

From the text below, extract factual claims or explanations
that help answer this research question:

{question}

Only include concrete technical information.
Avoid meta commentary.

TEXT:
{text}

CLAIMS:
"""


def synthesize_prompt(question, notes):
    return f"""
You are a research synthesizer.

Using ONLY the notes below, answer the research question.
If the notes are insufficient, say so explicitly.

QUESTION:
{question}

NOTES:
{notes}

ANSWER:
"""