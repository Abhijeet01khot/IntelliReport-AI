import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5,
)

def generate(prompt):
    response = llm.invoke(prompt)

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