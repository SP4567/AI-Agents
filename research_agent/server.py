from fastapi import FastAPI
from pydantic import BaseModel
from agent import ResearchAgent

app = FastAPI(title="Gemini Research Agent")

agent = ResearchAgent(model="gemini-2.5-flash")


class ResearchRequest(BaseModel):
    question: str


@app.post("/research")
def run_research(req: ResearchRequest):
    return {"answer": agent.research(req.question)}