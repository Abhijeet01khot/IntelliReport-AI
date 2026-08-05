from agents.research_agent import research_agent
from agents.outline_agent import outline_agent
from agents.writer_agent import writer_agent
from agents.reviewer_agent import reviewer_agent

topic = input("Enter Topic: ")

print("Researching...")
research = research_agent(topic)

print("Creating Outline...")
outline = outline_agent(research)

print("Writing Report...")
report = writer_agent(research, outline)

print("Reviewing Report...")
review = reviewer_agent(report)

print("\n===== REVIEW =====\n")
print(review)