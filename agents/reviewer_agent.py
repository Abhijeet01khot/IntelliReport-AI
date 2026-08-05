from utils.llm import generate

def reviewer_agent(report: str):
    prompt = f"""
You are a senior technical reviewer.

Review the following report.

Check for:

1. Grammar
2. Technical Accuracy
3. Missing Sections
4. Readability
5. Professional Writing Style

If the report is good enough, write:

APPROVED

Otherwise write:

NEEDS IMPROVEMENT

Then provide your suggestions.

Report:

{report}
"""

    return generate(prompt)