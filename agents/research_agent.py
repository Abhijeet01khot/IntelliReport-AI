from utils.llm import generate

def research_agent(topic: str):
    prompt = f"""
You are a professional research assistant.

Research the following topic thoroughly.

Topic:
{topic}

Provide:

1. Introduction
2. Key Concepts
3. Latest Developments
4. Advantages
5. Challenges
6. Future Scope

Return detailed research notes.
"""

    return generate(prompt)