from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os


def create_pdf(topic, report, review):

    if not os.path.exists("output"):
        os.makedirs("output")

    filename = f"output/{topic.replace(' ','_')}_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph(f"<b>{topic}</b>", styles["Title"]))

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    story.append(Paragraph("<b>Generated Report</b>", styles["Heading2"]))

    story.append(Paragraph(report.replace("\n", "<br/>"), styles["BodyText"]))

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    story.append(Paragraph("<b>Reviewer Feedback</b>", styles["Heading2"]))

    story.append(Paragraph(review.replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(story)

    return filename