import os
from dotenv import load_dotenv
import google.generativeai as genai

from tools import web_search, read_webpage
from memory import ResearchMemory
from prompts import plan_prompt, extract_prompt, synthesize_prompt

# Load environment
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def is_substantive(text):
    if not text or len(text) < 100:
        return False
    bad_phrases = [
        "no information",
        "cannot be extracted",
        "not available",
        "generic",
        "navigation"
    ]
    return not any(b in text.lower() for b in bad_phrases)


class ResearchAgent:
    def __init__(self, model="gemini-2.5-flash"):
        self.model = genai.GenerativeModel(model)
        self.memory = ResearchMemory()

    def llm(self, prompt):
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.0,
                "max_output_tokens": 1024
            }
        )
        return response.text.strip()

    def research(self, question):
        # 1️⃣ PLAN
        plan = self.llm(plan_prompt(question))
        sub_questions = [
            q.strip("-• ").strip()
            for q in plan.split("\n")
            if len(q.strip()) > 5
        ]

        # 2️⃣ RETRIEVE + READ
        for sq in sub_questions:
            links = web_search(sq)
            for link in links[:2]:
                try:
                    text = read_webpage(link)

                    claims = self.llm(extract_prompt(text, question))

                    if not is_substantive(claims):
                        claims = self.llm(
                            f"Summarize the key technical ideas from the following text:\n\n{text}"
                        )

                    if is_substantive(claims):
                        self.memory.add(claims, link)

                except Exception:
                    continue

        # 3️⃣ FALLBACK IF RETRIEVAL FAILED
        if not self.memory.notes:
            return self.llm(
                f"""
Explain the topic '{question}' using general technical knowledge.
Do NOT cite sources.
Be factual, structured, and concise.
"""
            )

        # 4️⃣ SYNTHESIZE
        return self.llm(
            synthesize_prompt(question, self.memory.summary())
        )