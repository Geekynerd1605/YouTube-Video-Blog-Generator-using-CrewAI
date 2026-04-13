from crewai import Agent, LLM
from tools import yt_tool
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(model="gpt-4o-mini")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
# os.environ['OPENAI_MODEL_NAME']='GPT-4o mini'

## Create a Senior Blog Content Researcher

blog_researcher=Agent(
    role='Blog Researcher from Youtube Videos',
    goal='get the relevant video content for the topic{topic} from the Yt channel',
    verbose=True,
    memory=False,
    max_iter=40,
    backstory=(
        "Expert in understanding videos in AI Data Science, Machine Learning and Gen AI and providing suggestions"
    ),
    tools=[yt_tool],
    llm=llm,
    allow_delegation=False,
)

## Creating a Senior Blog writer agent with YT Tool

blog_writer=Agent(
    role="Blog Writer",
    goal='Narrate compelling tech stories about the video {topic} from YT channel',
    verbose=True,
    memory=False,
    backstory=(
        "With a flair for simplifying complex topics, you craft engaging narratives that captivate and educate, bringing new"
        "discoveries to light in an accessible manner."
    ),
    tools=[yt_tool],
    llm=llm,
    allow_delegation=False
)