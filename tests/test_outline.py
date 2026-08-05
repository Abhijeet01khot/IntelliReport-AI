from agents.research_agent import research_agent
from agents.outline_agent import outline_agent

topic = input("Enter Topic: ")

research = research_agent(topic)

outline = outline_agent(research)

print(outline)