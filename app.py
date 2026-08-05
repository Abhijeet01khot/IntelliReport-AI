import time
from PIL import Image
import streamlit as st

from graph.workflow import workflow
from utils.export_pdf import create_pdf
from utils.export_docx import create_docx

# ======================================
# LOAD LOGO
# ======================================

logo = Image.open("assets/logo.jpg")

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="IntelliReport AI",
    page_icon=logo,
    layout="wide"
)

# ======================================
# SIDEBAR
# ======================================

with st.sidebar:

    st.image(logo, width=90)

    st.title("IntelliReport AI")

    st.markdown("---")

    st.subheader("📌 Project")
    st.write("Multi-Agent AI Report Generator")

    st.markdown("---")

    st.subheader("⚙ Workflow")

    st.markdown("""
        🔍 **Research Agent**

                ⬇

        📝 **Outline Agent**

                ⬇

        ✍ **Writer Agent**

                ⬇

        📝 **Grammar Agent**

                ⬇

        ✔ **Fact Checker Agent**

                ⬇

        📚 **Citation Agent**

                ⬇

        🧐 **Reviewer Agent**
    """)

    st.markdown("---")

    st.subheader("🛠 Tech Stack")

    st.write("✅ Python")
    st.write("✅ Streamlit")
    st.write("✅ LangGraph")
    st.write("✅ Gemini AI")

    st.markdown("---")

    st.success("Version 2.0")

# ======================================
# HEADER
# ======================================

col1, col2 = st.columns([1, 6])

with col1:
    st.image(logo, width=70)

with col2:
    st.title("IntelliReport AI")
    st.caption("AI-Powered Multi-Agent Report Generation Platform")

st.divider()

# ======================================
# ABOUT PROJECT
# ======================================

with st.expander(" About IntelliReport AI", expanded=False):

    st.write(
        """
        **IntelliReport AI** is a Multi-Agent AI platform that automates the complete report generation process.

            The application consists of seven specialized AI agents:

            🔍 Research Agent

            📝 Outline Agent

            ✍ Writer Agent

            📝 Grammar Agent

            ✔ Fact Checker Agent

            📚 Citation Agent

            🧐 Reviewer Agent

        Features:
        - Generate detailed AI-powered reports
        - Automated report review
        - Export reports to PDF and DOCX
        - Interactive analytics dashboard
        - Multi-Agent workflow execution
        """
    )


# ======================================
# INPUT
# ======================================

topic = st.text_input(
    "📌 Enter Report Topic",
    placeholder="Example: Artificial Intelligence"
)

generate = st.button(
    "🚀 Generate Report",
    use_container_width=True
)

# ======================================
# MAIN WORKFLOW
# ======================================

if generate:

    if topic.strip() == "":
        st.warning("Please enter a topic.")
        st.stop()

    start = time.time()

    progress = st.progress(0)
    status = st.empty()

    status.info("🔍 Research Agent Running...")
    progress.progress(10)

    status.info("📝 Outline Agent Running...")
    progress.progress(25)

    status.info("✍ Writer Agent Running...")
    progress.progress(45)

    status.info("📝 Grammar Agent Running...")
    progress.progress(60)

    status.info("✔ Fact Checker Agent Running...")
    progress.progress(75)

    status.info("📚 Citation Agent Running...")
    progress.progress(90)

    # Run the complete workflow
    result = workflow.invoke(
        {
            "topic": topic
        }
    )
    

    progress.progress(100)

    status.success("✅ All 7 Agents Completed Successfully")

    end = time.time()

    execution = round(end - start, 2)
    words = len(result["report"].split())

    st.success("🎉 Report Generated Successfully!")

    st.divider()

    # ======================================
    # ANALYTICS
    # ======================================

    st.subheader("📊 Analytics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Execution Time",
            f"{execution} sec"
        )

    with col2:
        st.metric(
            "Word Count",
            words
        )

    with col3:
        st.metric(
            "Agents Used",
            "7"
        )

    st.divider()

    # ======================================
    # AGENT OUTPUTS
    # ======================================

    st.subheader("🤖 Agent Outputs")

    with st.expander("🔍 Research Agent"):
        st.write(result["research"])

    with st.expander("📝 Outline Agent"):
        st.write(result["outline"])

    with st.expander("📝 Grammar Agent"):
        st.write(result["grammar"])

    with st.expander("✔ Fact Checker Agent"):
        st.write(result["fact_checker"])

    with st.expander("📚 Citation Agent"):
        st.write(result["citations"])

    with st.expander("🧐 Reviewer Feedback"):
        st.write(result["review"])

    st.divider()

    # ======================================
    # REPORT
    # ======================================

    tab1, tab2 = st.tabs(
        [
            "📄 Final Report",
            "📝 AI Review"
        ]
    )

    with tab1:
        st.markdown(result["report"])

    with tab2:
        st.markdown(result["review"])

    st.divider()

    # ======================================
    # DOWNLOADS
    # ======================================

    st.subheader("📥 Download Report")

    pdf_path = create_pdf(
        topic,
        result["report"],
        result["review"]
    )

    with open(pdf_path, "rb") as pdf:
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf,
            file_name=f"{topic}_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    docx_path = create_docx(
        topic,
        result["report"],
        result["review"]
    )

    with open(docx_path, "rb") as docx:
        st.download_button(
            label="📝 Download Word Report",
            data=docx,
            file_name=f"{topic}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

st.divider()

st.caption(
    "IntelliReport AI © 2026 | Developed by Abhijeet Khot & Nivedita Deshpande | MIT-WPU"
)