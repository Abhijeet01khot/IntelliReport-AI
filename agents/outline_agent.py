from utils.llm import generate

def outline_agent(research_notes: str):
    prompt = f"""
You are an expert report planner.

Using the research notes below, create a professional report outline.

Research Notes:
{research_notes}

Generate only a structured outline like:

1. Introduction
2. Background
3. Key Concepts
4. Applications
5. Advantages
6. Challenges
7. Future Scope
8. Conclusion
"""

    return generate(prompt)