from agents.research_agent import research_agent
from agents.outline_agent import outline_agent
from agents.writer_agent import writer_agent

topic = input("Enter Topic: ")

print("\nResearching...\n")
research = research_agent(topic)

print("\nCreating Outline...\n")
outline = outline_agent(research)

print("\nWriting Report...\n")
report = writer_agent(research, outline)

print(report)
