from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer

## Research Task
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

## Writing task with language model configuration

write_task=Task(
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