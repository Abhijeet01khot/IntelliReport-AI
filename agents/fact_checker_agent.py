from utils.llm import generate


def fact_checker_agent(report: str):

    prompt = f"""
You are an AI fact-checking assistant.

Review the report below.

Tasks:

- Check factual accuracy.
- Correct any obvious factual mistakes.
- Remove misleading information.
- Preserve formatting.
- Do NOT rewrite the entire report.
- Return ONLY the corrected report.

Report:

{report}
"""

    return generate(prompt)