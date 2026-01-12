from agent import ResearchAgent

if __name__ == "__main__":
    agent = ResearchAgent(model="gemini-2.5-flash")

    question = input("Research question: ")
    answer = agent.research(question)

    print("\n=== RESEARCH OUTPUT ===\n")
    print(answer)