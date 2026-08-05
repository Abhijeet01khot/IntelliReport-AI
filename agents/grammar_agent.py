from utils.llm import generate


def grammar_agent(report: str):

    prompt = f"""
You are a professional English editor.

Improve the report below by:

- Correcting grammar
- Correcting spelling
- Improving sentence structure
- Improving readability
- Keeping the meaning unchanged
- DO NOT shorten the report.
- Return ONLY the corrected report.

Report:

{report}
"""

    return generate(prompt)