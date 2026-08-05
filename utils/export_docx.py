from docx import Document
from docx.shared import Pt
import os


def create_docx(topic, report, review):

    if not os.path.exists("output"):
        os.makedirs("output")

    filename = f"output/{topic.replace(' ','_')}.docx"

    doc = Document()

    title = doc.add_heading(topic, level=1)

    title.runs[0].font.size = Pt(20)

    doc.add_heading("Generated Report", level=2)

    doc.add_paragraph(report)

    doc.add_page_break()

    doc.add_heading("Reviewer Feedback", level=2)

    doc.add_paragraph(review)

    doc.save(filename)

    return filename