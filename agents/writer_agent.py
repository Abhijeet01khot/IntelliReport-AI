from utils.llm import generate


def writer_agent(research_notes: str, outline: str):
    prompt = f"""
You are an expert technical report writer.

Using the research notes and outline below, write a professional report.

Research Notes:
{research_notes}

Outline:
{outline}

Instructions:
- Follow the outline.
- Explain every section clearly.
- Use professional language.
- Use headings and subheadings.
- Write around 1200-1500 words.
"""

    return generate(prompt)