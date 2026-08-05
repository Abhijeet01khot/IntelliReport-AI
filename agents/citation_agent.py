from utils.llm import generate


def citation_agent(report: str):

    prompt = f"""
You are a technical documentation assistant.

Review the report below.

Tasks:

- Add proper references section at the end.
- Add citation placeholders where appropriate.
- Do NOT rewrite the report.
- Preserve formatting.
- Return the updated report only.

Example References:

References

1. Google AI Documentation
2. LangGraph Documentation
3. LangChain Documentation
4. Streamlit Documentation

Report:

{report}
"""

    return generate(prompt)