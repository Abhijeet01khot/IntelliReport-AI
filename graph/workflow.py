from langgraph.graph import StateGraph, END

from graph.state import ReportState

from agents.research_agent import research_agent
from agents.outline_agent import outline_agent
from agents.writer_agent import writer_agent
from agents.grammar_agent import grammar_agent
from agents.fact_checker_agent import fact_checker_agent
from agents.citation_agent import citation_agent
from agents.reviewer_agent import reviewer_agent


# -----------------------------------
# Research
# -----------------------------------

def research_node(state: ReportState):

    research = research_agent(
        state["topic"]
    )

    return {
        "research": research
    }


# -----------------------------------
# Outline
# -----------------------------------

def outline_node(state: ReportState):

    outline = outline_agent(
        state["research"]
    )

    return {
        "outline": outline
    }


# -----------------------------------
# Writer
# -----------------------------------

def writer_node(state: ReportState):

    report = writer_agent(
        state["research"],
        state["outline"]
    )

    return {
        "report": report
    }


# -----------------------------------
# Grammar Agent 
# -----------------------------------

def grammar_node(state: ReportState):

    grammar = grammar_agent(
        state["report"]
    )

    return {
        "grammar": grammar
    }


# -----------------------------------
# Fact Checker
# -----------------------------------

def fact_checker_node(state: ReportState):

    checked_report = fact_checker_agent(
        state["grammar"]
    )

    return {
        "fact_checker": checked_report
    }


# -----------------------------------
# Citation Agent
# -----------------------------------

def citation_node(state: ReportState):

    cited_report = citation_agent(
        state["fact_checker"]
    )

    return {
        "citations": cited_report
    }


# -----------------------------------
# Reviewer
# -----------------------------------

def reviewer_node(state: ReportState):

    review = reviewer_agent(
        state["citations"]
    )

    return {
        "review": review
    }


# ===================================
# GRAPH
# ===================================

builder = StateGraph(ReportState)

builder.add_node("Research", research_node)
builder.add_node("Outline", outline_node)
builder.add_node("Writer", writer_node)
builder.add_node("Grammar", grammar_node)
builder.add_node("FactChecker", fact_checker_node)
builder.add_node("Citation", citation_node)
builder.add_node("Reviewer", reviewer_node)

builder.set_entry_point("Research")

builder.add_edge("Research", "Outline")
builder.add_edge("Outline", "Writer")
builder.add_edge("Writer", "Grammar")
builder.add_edge("Grammar", "FactChecker")
builder.add_edge("FactChecker", "Citation")
builder.add_edge("Citation", "Reviewer")
builder.add_edge("Reviewer", END)

workflow = builder.compile()