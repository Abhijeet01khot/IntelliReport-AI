
from io import BytesIO
from pathlib import Path
from time import perf_counter

from docx import Document
from pypdf import PdfReader


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def extract_document_text(filename: str, file_bytes: bytes) -> str:
    """Extract text from a PDF or DOCX uploaded as bytes."""

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported file type. Upload a PDF or DOCX file.")

    if not file_bytes:
        raise ValueError("The uploaded document is empty.")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError("File exceeds the 10 MB upload limit.")

    try:
        if extension == ".pdf":
            reader = PdfReader(BytesIO(file_bytes))

            if reader.is_encrypted:
                raise ValueError(
                    "Password-protected PDFs are not supported."
                )

            text = "\n".join(
                page.extract_text() or "" for page in reader.pages
            )

        else:
            document = Document(BytesIO(file_bytes))
            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]
            text = "\n".join(paragraphs)

    except ValueError:
        raise
    except Exception as error:
        raise ValueError(
            "Could not read this document. Check that it is a valid PDF or DOCX."
        ) from error

    text = text.strip()

    if not text:
        raise ValueError(
            "No readable text was found. Scanned PDFs may require OCR."
        )

    return text


def make_agent_result(
    agent: str,
    status: str,
    output: str,
    duration: float,
    error: str = "",
) -> dict:
    """Create a consistent result record for an individual agent."""

    if status not in {"success", "error", "skipped"}:
        raise ValueError("Invalid agent status.")

    return {
        "agent": agent,
        "status": status,
        "output": output,
        "duration": round(max(0.0, duration), 3),
        "error": error,
    }


def run_agent_with_status(agent_name: str, agent_function, *args) -> dict:
    """Run one agent and capture its output, duration, or error."""

    start = perf_counter()

    try:
        output = agent_function(*args)

        if not isinstance(output, str) or not output.strip():
            raise ValueError("The agent returned empty output.")

        return make_agent_result(
            agent=agent_name,
            status="success",
            output=output,
            duration=perf_counter() - start,
        )

    except Exception as error:
        return make_agent_result(
            agent=agent_name,
            status="error",
            output="",
            duration=perf_counter() - start,
            error=str(error),
        )
