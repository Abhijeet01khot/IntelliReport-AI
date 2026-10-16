
from typing import TypedDict

from langgraph.graph import StateGraph, END

from utils.llm import generate
from utils.document_review import run_agent_with_status


class DocumentReviewState(TypedDict):
    document_text: str
    research_result: dict
    outline_result: dict
    writer_result: dict
    grammar_result: dict
    fact_checker_result: dict
    citation_result: dict
    reviewer_result: dict


def _run_review_agent(agent_name: str, prompt: str) -> dict:
    """Run an agent and capture its status, output, duration, or error."""
    return run_agent_with_status(
        agent_name,
        lambda: generate(prompt),
    )


def research_review_node(state: DocumentReviewState) -> dict:
    prompt = f"""
You are the Research Agent in a document review system.

Analyze the document and identify:
- Claims that require external verification
- Technical statements that may be outdated
- Areas that need stronger evidence
- Questions a researcher should investigate

Do not claim that you searched the web or verified sources.
Do not invent sources or references.
Distinguish potentially verifiable claims from unverified claims.

Return structured review findings, not a rewritten document.

DOCUMENT:
{state["document_text"]}
"""
    return {
        "research_result": _run_review_agent("Research Agent", prompt)
    }


def outline_review_node(state: DocumentReviewState) -> dict:
    prompt = f"""
You are the Outline Agent reviewing an existing document.

Assess its organization, logical flow, headings, and section coverage.
Identify missing sections, duplicated ideas, and ordering problems.
Suggest a better outline only if useful.

Do not rewrite the document.

DOCUMENT:
{state["document_text"]}
"""
    return {
        "outline_result": _run_review_agent("Outline Agent", prompt)
    }


def writer_review_node(state: DocumentReviewState) -> dict:
    prompt = f"""
You are the Writer Agent providing editorial recommendations.

Suggest concrete improvements to clarity, explanations, examples,
transitions, depth, and professional writing style.

For each recommendation, explain what could be improved and why.
Provide short example sentences only when helpful.

Do NOT rewrite the entire document.
Do NOT return a replacement document.
The user must remain in control of all edits.

DOCUMENT:
{state["document_text"]}
"""
    return {
        "writer_result": _run_review_agent("Writer Agent", prompt)
    }


def grammar_review_node(state: DocumentReviewState) -> dict:
    prompt = f"""
You are the Grammar Agent reviewing an existing document.

Identify grammar, spelling, punctuation, sentence structure,
and readability issues.

Provide problematic wording when practical and suggest corrections.
Do not silently rewrite the document.
Do not claim to have changed the original file.

DOCUMENT:
{state["document_text"]}
"""
    return {
        "grammar_result": _run_review_agent("Grammar Agent", prompt)
    }


def fact_checker_review_node(state: DocumentReviewState) -> dict:
    prompt = f"""
You are the Fact Checker Agent reviewing a document.

Identify claims that may be incorrect, misleading, ambiguous,
or unsupported.

For each significant claim, classify it as:
- Potentially incorrect
- Needs external verification
- Insufficient context
- No obvious issue identified

Explain your reasoning and what evidence would be needed.
Do not claim definitive verification without reliable evidence.
You do not have a web-search tool in this task.
Do not invent facts or citations.
Do not rewrite the document.

DOCUMENT:
{state["document_text"]}
"""
    return {
        "fact_checker_result": _run_review_agent(
            "Fact Checker Agent", prompt
        )
    }


def citation_review_node(state: DocumentReviewState) -> dict:
    prompt = f"""
You are the Citation Agent reviewing an existing document.

Identify claims that need citations, missing attribution,
incomplete references, and places where evidence should be supplied.

Do not invent references, URLs, authors, titles, or publication dates.
Label citation suggestions as suggestions, not verified sources.
Do not rewrite the document.

DOCUMENT:
{state["document_text"]}
"""
    return {
        "citation_result": _run_review_agent("Citation Agent", prompt)
    }


def reviewer_review_node(state: DocumentReviewState) -> dict:
    agent_results = {
        "Research Agent": state["research_result"],
        "Outline Agent": state["outline_result"],
        "Writer Agent": state["writer_result"],
        "Grammar Agent": state["grammar_result"],
        "Fact Checker Agent": state["fact_checker_result"],
        "Citation Agent": state["citation_result"],
    }

    findings = []

    for agent_name, result in agent_results.items():
        findings.append(
            f"{agent_name}\n"
            f"Status: {result.get('status', 'unknown')}\n"
            f"Output: {result.get('output') or 'No output available'}\n"
            f"Error: {result.get('error') or 'None'}"
        )

    agent_findings = "\n\n".join(findings)

    prompt = f"""
You are the senior Reviewer Agent.

Prepare a final review summary using the document and agent findings.

Include:
1. Overall assessment
2. Most important issues
3. Prioritized recommendations
4. Claims requiring external verification
5. Agent failures that limit this assessment

Do not claim the document is factually verified.
Do not rewrite the original document.
If important agents failed, explicitly state that the review is incomplete.

DOCUMENT:
{state["document_text"]}

AGENT FINDINGS:
{agent_findings}
"""
    return {
        "reviewer_result": _run_review_agent("Reviewer Agent", prompt)
    }


# ----------------------------------------
# Build the document-review graph
# ----------------------------------------

builder = StateGraph(DocumentReviewState)

builder.add_node("Research", research_review_node)
builder.add_node("Outline", outline_review_node)
builder.add_node("Writer", writer_review_node)
builder.add_node("Grammar", grammar_review_node)
builder.add_node("FactChecker", fact_checker_review_node)
builder.add_node("Citation", citation_review_node)
builder.add_node("Reviewer", reviewer_review_node)

builder.set_entry_point("Research")

builder.add_edge("Research", "Outline")
builder.add_edge("Outline", "Writer")
builder.add_edge("Writer", "Grammar")
builder.add_edge("Grammar", "FactChecker")
builder.add_edge("FactChecker", "Citation")
builder.add_edge("Citation", "Reviewer")
builder.add_edge("Reviewer", END)

document_review_workflow = builder.compile()


def review_document(document_text: str) -> dict:
    """Run the review workflow against extracted document text."""
    if not isinstance(document_text, str) or not document_text.strip():
        raise ValueError("Document text cannot be empty.")

    initial_state = {
        "document_text": document_text,
        "research_result": {},
        "outline_result": {},
        "writer_result": {},
        "grammar_result": {},
        "fact_checker_result": {},
        "citation_result": {},
        "reviewer_result": {},
    }

    return document_review_workflow.invoke(initial_state)
