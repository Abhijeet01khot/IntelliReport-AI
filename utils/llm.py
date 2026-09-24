import os
import time

from dotenv import load_dotenv
from google.genai.errors import ServerError
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is not configured. "
        "Please check your .env file."
    )


# Stable model for the main workload.
PRIMARY_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)

# Fallback model if the primary model is temporarily unavailable.
FALLBACK_MODEL = os.getenv(
    "GEMINI_FALLBACK_MODEL",
    "gemini-3.8-flash"
)


llm = ChatGoogleGenerativeAI(
    model=PRIMARY_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=0.5,
)


fallback_llm = ChatGoogleGenerativeAI(
    model=FALLBACK_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=0.5,
)


def _extract_content(response):
    """
    Extract text from a LangChain Gemini response.
    """

    if hasattr(response, "content"):
        content = response.content

        if isinstance(content, list):
            text = ""

            for item in content:
                if isinstance(item, dict):
                    text += item.get("text", "")
                else:
                    text += str(item)

            return text

        return content

    return str(response)


def _invoke_with_retry(model, prompt, model_name):
    """
    Invoke Gemini with exponential backoff for temporary
    server availability errors.
    """

    max_retries = 3
    base_delay = 3

    for attempt in range(max_retries):
        try:
            response = model.invoke(prompt)
            return _extract_content(response)

        except ServerError as error:

            if attempt == max_retries - 1:
                raise error

            delay = base_delay * (2 ** attempt)

            print(
                f"Gemini model '{model_name}' is temporarily "
                f"unavailable. Retrying in {delay} seconds..."
            )

            time.sleep(delay)


def generate(prompt):
    """
    Generate content using Gemini.

    Primary model:
        GEMINI_MODEL

    If the primary model repeatedly returns a 503,
    the fallback model is attempted.
    """

    try:
        return _invoke_with_retry(
            llm,
            prompt,
            PRIMARY_MODEL
        )

    except ServerError as primary_error:

        print(
            f"Primary Gemini model '{PRIMARY_MODEL}' "
            f"remained unavailable."
        )

        print(
            f"Trying fallback model '{FALLBACK_MODEL}'..."
        )

        try:
            return _invoke_with_retry(
                fallback_llm,
                prompt,
                FALLBACK_MODEL
            )

        except ServerError:
            # Preserve the original failure context.
            raise RuntimeError(
                "Gemini is temporarily unavailable. "
                f"Both '{PRIMARY_MODEL}' and "
                f"'{FALLBACK_MODEL}' failed. "
                "Please try generating the report again "
                "after a short wait."
            ) from primary_error