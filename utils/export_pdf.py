
import os
from xml.sax.saxutils import escape

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)


def _add_text(story, text, style):
    """Add escaped text to a ReportLab story."""
    safe_text = escape(str(text or ""))
    safe_text = safe_text.replace("\n", "<br/>")
    story.append(Paragraph(safe_text, style))


def create_pdf(topic, report, review):
    """Export a generated report and reviewer feedback."""

    os.makedirs("output", exist_ok=True)

    safe_topic = "".join(
        character if character.isalnum() or character in "-_ " else "_"
        for character in topic
    ).strip()

    filename = f"output/{safe_topic.replace(' ', '_')}_Report.pdf"

    doc = SimpleDocTemplate(
        filename,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()
    story = []

    _add_text(story, topic, styles["Title"])
    story.append(Spacer(1, 18))

    _add_text(story, "Generated Report", styles["Heading2"])
    _add_text(story, report, styles["BodyText"])
    story.append(Spacer(1, 18))

    _add_text(story, "Reviewer Feedback", styles["Heading2"])
    _add_text(story, review, styles["BodyText"])

    doc.build(story)
    return filename


def create_document_review_pdf(
    filename,
    original_name,
    review_results,
):
    """Export document-review findings to a PDF."""

    os.makedirs("output", exist_ok=True)

    safe_name = os.path.basename(filename)
    base_name = os.path.splitext(safe_name)[0]
    output_name = f"output/{base_name}_Review.pdf"

    doc = SimpleDocTemplate(
        output_name,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
    )

    styles = getSampleStyleSheet()
    story = []

    _add_text(
        story,
        "IntelliReport AI - Document Review",
        styles["Title"],
    )
    story.append(Spacer(1, 12))

    _add_text(
        story,
        f"Original document: {original_name}",
        styles["Normal"],
    )
    story.append(Spacer(1, 18))

    for result in review_results:
        _add_text(
            story,
            result.get("agent", "Agent"),
            styles["Heading2"],
        )
        _add_text(
            story,
            f"Status: {result.get('status', 'unknown').upper()}",
            styles["Normal"],
        )
        _add_text(
            story,
            f"Execution time: {result.get('duration', 0)} seconds",
            styles["Normal"],
        )

        if result.get("output"):
            story.append(Spacer(1, 6))
            _add_text(story, "Findings", styles["Heading3"])
            _add_text(story, result["output"], styles["BodyText"])

        if result.get("error"):
            story.append(Spacer(1, 6))
            _add_text(story, "Error", styles["Heading3"])
            _add_text(story, result["error"], styles["BodyText"])

        story.append(Spacer(1, 16))

    doc.build(story)
    return output_name
