"""
CrewAI task definitions for research and blog writing.

Both tasks use the YouTube channel search tool. Placeholders like {topic}
are filled from crew.kickoff(inputs={"topic": "..."}) in crew.py.
"""

from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer

# Step 1: Search the channel and produce a research report (no fabricated video URLs).
research_task = Task(
    description=(
        "Search the configured YouTube channel for content about {topic} using the "
        "channel search tool. Pass only a natural-language search_query (the topic or "
        "keywords). Do not invent or guess video URLs or video IDs."
    ),
    expected_output='A comprehensive 3 paragraphs long report based on the {topic} of video content.',
    tools=[yt_tool],
    agent=blog_researcher
)

# Step 2: Write the blog and save to new-blog-post.md (output_file on the task).
write_task = Task(
    description=(
        "Using the channel search tool, gather information about {topic}. "
        "Use search_query only; do not use made-up youtube.com/watch links."
    ),
    expected_output='Summarize the info from the youtube channel video on the topic {topic} and create the content for the blog.',
    tools=[yt_tool],
    agent=blog_writer,
    async_execution=False,
    output_file='new-blog-post.md'
)
