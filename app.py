
import os
import re
import time
from pathlib import Path

from PIL import Image
import streamlit as st

from database.database import init_db
from graph.workflow import workflow
from graph.document_review_workflow import review_document
from ui.auth_ui import initialize_session, show_auth_page, logout
from utils.document_review import extract_document_text
from utils.export_pdf import create_pdf, create_document_review_pdf
from utils.export_docx import create_docx, create_document_review_docx


# ======================================
# PAGE CONFIG
# ======================================

logo = Image.open("assets/logo.jpg")

st.set_page_config(
    page_title="IntelliReport AI",
    page_icon=logo,
    layout="wide",
)


# ======================================
# INITIALIZATION AND AUTHENTICATION
# ======================================

init_db()
initialize_session()

if not st.session_state["authenticated"]:
    show_auth_page()
    st.stop()


# ======================================
# HELPERS
# ======================================

def safe_filename(value: str) -> str:
    """Create a safe filename component."""
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    cleaned = cleaned.strip(" ._")
    return cleaned[:100] or "document"


def show_agent_results(results: list[dict]) -> None:
    """Display compact controls for individual agent results."""
    st.subheader("Agent Activity")
    st.caption(
        "Select an agent to inspect its status, findings, duration, "
        "and any error."
    )

    for result in results:
        agent = result.get("agent", "Agent")
        status = result.get("status", "unknown")
        duration = result.get("duration", 0)

        if status == "success":
            icon = "✅"
        elif status == "error":
            icon = "❌"
        else:
            icon = "⏭️"

        with st.expander(
            f"{icon} {agent} · {status.upper()} · {duration:.2f}s",
            expanded=False,
        ):
            st.write(f"**Status:** {status}")
            st.write(f"**Execution time:** {duration:.2f} seconds")

            if result.get("output"):
                st.markdown("**Output**")
                st.markdown(result["output"])
            else:
                st.info("This agent produced no output.")

            if result.get("error"):
                st.error(result["error"])


def review_results_as_list(result: dict) -> list[dict]:
    """Return review-agent results in workflow order."""
    keys = [
        "research_result",
        "outline_result",
        "writer_result",
        "grammar_result",
        "fact_checker_result",
        "citation_result",
        "reviewer_result",
    ]

    return [
        result[key]
        for key in keys
        if isinstance(result.get(key), dict) and result[key]
    ]


# ======================================
# SIDEBAR
# ======================================

with st.sidebar:
    st.image(logo, width=90)
    st.title("IntelliReport AI")
    st.markdown("---")

    st.subheader("👤 Account")
    st.write(st.session_state["user_name"])
    st.caption(st.session_state["user_email"])

    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()

    st.markdown("---")
    st.subheader("📌 Project")
    st.write("Multi-Agent Report Generation and Document Review")

    st.markdown("---")
    st.subheader("⚙️ Seven-Agent Workflow")
    st.markdown(
        """
        1. 🔍 Research
        2. 📝 Outline
        3. ✍️ Writer
        4. 📝 Grammar
        5. ✔️ Fact Checker
        6. 📚 Citation
        7. 🧐 Reviewer
        """
    )


# ======================================
# HEADER
# ======================================

col1, col2 = st.columns([1, 6])

with col1:
    st.image(logo, width=70)

with col2:
    st.title("IntelliReport AI")
    st.caption(
        "AI-powered report generation and document review"
    )

st.divider()


with st.expander("ℹ️ About IntelliReport AI", expanded=False):
    st.write(
        """
        IntelliReport AI uses seven specialized AI agents to generate
        reports or review existing documents.

        **Generate Report**
        - Research and outline a topic
        - Draft and review a report
        - Export the generated report to PDF or Word

        **Review Existing Document**
        - Upload a PDF or DOCX file
        - Inspect structure, writing, citations, and claims
        - Review each agent's findings and errors
        - Export the review results

        AI review findings are suggestions, not guaranteed verification
        of factual accuracy. The current review workflow does not
        independently search the web for evidence.
        """
    )


# ======================================
# MODE SELECTOR
# ======================================

mode = st.radio(
    "Choose a task",
    ["Generate Report", "Review Existing Document"],
    horizontal=True,
    key="intellireport_mode",
)

st.divider()


# ======================================
# MODE 1: GENERATE REPORT
# ======================================

if mode == "Generate Report":
    st.subheader("🚀 Generate a Report")

    topic = st.text_input(
        "📌 Enter Report Topic",
        placeholder="Example: Artificial Intelligence",
        key="report_topic",
    )

    if st.button(
        "🚀 Generate Report",
        use_container_width=True,
        key="generate_report_button",
    ):
        if not topic.strip():
            st.warning("Please enter a topic.")
            st.stop()

        started = time.perf_counter()
        progress = st.progress(0)
        status = st.empty()

        try:
            status.info("Running the seven-agent report workflow...")
            progress.progress(10)

            result = workflow.invoke({"topic": topic.strip()})

            progress.progress(100)
            status.success("Report workflow completed.")

        except RuntimeError as error:
            progress.empty()
            status.empty()
            st.error("Report generation is temporarily unavailable.")
            st.warning(str(error))
            st.info("Please wait and try again.")
            st.stop()

        except Exception as error:
            progress.empty()
            status.empty()
            st.error("An unexpected error occurred.")
            with st.expander("Technical details"):
                st.code(str(error))
            st.stop()

        execution = round(time.perf_counter() - started, 2)
        report_text = result.get("report", "")
        review_text = result.get("review", "")

        st.success("🎉 Report generated successfully!")
        st.divider()
        st.subheader("📊 Analytics")

        col1, col2, col3 = st.columns(3)
        col1.metric("Execution Time", f"{execution} sec")
        col2.metric("Word Count", len(report_text.split()))
        col3.metric("Agents Used", 7)

        tab1, tab2, tab3 = st.tabs(
            ["📄 Final Report", "📝 AI Review", "🤖 Agent Activity"]
        )

        with tab1:
            st.markdown(report_text)

        with tab2:
            st.markdown(review_text)

        with tab3:
            report_agent_mapping = [
                ("Research Agent", "research"),
                ("Outline Agent", "outline"),
                ("Writer Agent", "report"),
                ("Grammar Agent", "grammar"),
                ("Fact Checker Agent", "fact_checker"),
                ("Citation Agent", "citations"),
                ("Reviewer Agent", "review"),
            ]

            report_agent_results = [
                {
                    "agent": name,
                    "status": (
                        "success"
                        if result.get(key)
                        else "error"
                    ),
                    "output": result.get(key, ""),
                    "duration": 0.0,
                    "error": (
                        ""
                        if result.get(key)
                        else "No output was returned for this agent."
                    ),
                }
                for name, key in report_agent_mapping
            ]

            show_agent_results(report_agent_results)

        st.divider()
        st.subheader("📥 Download Report")

        try:
            pdf_path = create_pdf(topic, report_text, review_text)

            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    "📄 Download PDF Report",
                    data=pdf_file,
                    file_name=f"{safe_filename(topic)}_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_report_pdf",
                )

            docx_path = create_docx(topic, report_text, review_text)

            with open(docx_path, "rb") as docx_file:
                st.download_button(
                    "📝 Download Word Report",
                    data=docx_file,
                    file_name=f"{safe_filename(topic)}_Report.docx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),
                    use_container_width=True,
                    key="download_report_docx",
                )

        except Exception as error:
            st.error("Could not prepare the report downloads.")
            with st.expander("Export details"):
                st.code(str(error))


# ======================================
# MODE 2: REVIEW EXISTING DOCUMENT
# ======================================

else:
    st.subheader("📄 Review an Existing Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF or Word document",
        type=["pdf", "docx"],
        help="Maximum file size: 10 MB. Scanned PDFs may require OCR.",
        key="document_review_upload",
    )

    if uploaded_file is not None:
        st.write(f"**Selected file:** {uploaded_file.name}")
        st.write(
            f"**File size:** {uploaded_file.size / (1024 * 1024):.2f} MB"
        )

    if st.button(
        "🔎 Review Document",
        use_container_width=True,
        key="review_document_button",
    ):
        if uploaded_file is None:
            st.warning("Please upload a PDF or DOCX file first.")
            st.stop()

        try:
            document_text = extract_document_text(
                uploaded_file.name,
                uploaded_file.getvalue(),
            )
        except ValueError as error:
            st.error(str(error))
            st.stop()
        except Exception as error:
            st.error("Could not read the uploaded document.")
            with st.expander("Technical details"):
                st.code(str(error))
            st.stop()

        started = time.perf_counter()
        progress = st.progress(10)
        status = st.empty()

        try:
            status.info("Running document-review agents...")
            progress.progress(20)

            result = review_document(document_text)

            progress.progress(100)
            status.success("Document-review workflow finished.")

        except Exception as error:
            progress.empty()
            status.empty()
            st.error("The document-review workflow could not finish.")
            with st.expander("Technical details"):
                st.code(str(error))
            st.stop()

        execution = round(time.perf_counter() - started, 2)
        agent_results = review_results_as_list(result)

        st.session_state["last_document_review"] = {
            "filename": uploaded_file.name,
            "results": agent_results,
            "execution": execution,
            "word_count": len(document_text.split()),
        }

    saved_review = st.session_state.get("last_document_review")

    if saved_review:
        st.divider()
        st.subheader("📊 Review Summary")

        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Execution Time",
            f"{saved_review['execution']} sec",
        )
        col2.metric("Document Words", saved_review["word_count"])
        col3.metric("Agents Recorded", len(saved_review["results"]))

        st.caption(
            f"Review results for: {saved_review['filename']}"
        )

        agent_results = saved_review["results"]

        reviewer_result = next(
            (
                item for item in agent_results
                if item.get("agent") == "Reviewer Agent"
            ),
            None,
        )

        if reviewer_result and reviewer_result.get("output"):
            st.subheader("📝 Overall Review")
            st.markdown(reviewer_result["output"])

        show_agent_results(agent_results)

        st.divider()
        st.subheader("📥 Download Review")

        try:
            pdf_path = create_document_review_pdf(
                saved_review["filename"],
                saved_review["filename"],
                agent_results,
            )

            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    "📄 Download Review PDF",
                    data=pdf_file,
                    file_name=(
                        f"{safe_filename(saved_review['filename'])}_Review.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True,
                    key="download_review_pdf",
                )

            docx_path = create_document_review_docx(
                saved_review["filename"],
                saved_review["filename"],
                agent_results,
            )

            with open(docx_path, "rb") as docx_file:
                st.download_button(
                    "📝 Download Review Word Document",
                    data=docx_file,
                    file_name=(
                        f"{safe_filename(saved_review['filename'])}_Review.docx"
                    ),
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),
                    use_container_width=True,
                    key="download_review_docx",
                )

        except Exception as error:
            st.error("Could not prepare the review downloads.")
            with st.expander("Export details"):
                st.code(str(error))


# ======================================
# FOOTER
# ======================================

st.divider()
st.caption(
    "IntelliReport AI © 2026 | "
    "Developed by Abhijeet Khot & Nivedita Deshpande | MIT-WPU"
)
