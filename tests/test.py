from utils.llm import llm

response = llm.invoke("Say Hello from Gemini")

print(response.content)
