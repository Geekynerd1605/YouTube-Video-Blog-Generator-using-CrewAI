"""
CrewAI agent definitions for the YouTube blog pipeline.

Loads OpenAI credentials from .env, configures the shared LLM, and defines
the researcher (gather video context) and writer (produce the blog post).
"""

from crewai import Agent, LLM
from tools import yt_tool
import os
from dotenv import load_dotenv

load_dotenv()

# Shared language model for both agents (OpenAI via CrewAI LLM wrapper).
llm = LLM(model="gpt-4o-mini")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# --- Research agent: searches the configured YouTube channel for {topic} ---
blog_researcher = Agent(
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

# --- Writer agent: turns research into a narrative blog post for {topic} ---
blog_writer = Agent(
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
