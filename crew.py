"""
Entry point for the YouTube Blog Creator crew.

Orchestrates a sequential CrewAI workflow: research from a YouTube channel,
then write a markdown blog post to new-blog-post.md.
"""

import sys
import time

from crewai import Crew, Process
from agents import blog_researcher, blog_writer
from tasks import research_task, write_task

# Sequential process: research_task runs first, then write_task uses its context.
crew = Crew(
    agents=[blog_researcher, blog_writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    memory=False,
    cache=False,
    max_rpm=100,
    share_crew=False,
)

if __name__ == "__main__":
    # Change "topic" to generate blogs on different subjects.
    result = crew.kickoff(inputs={"topic": "Why Oracle Laid Off 30k Employees Despite Strong Revenue Growth"})
    print(result)
    sys.stdout.flush()
    sys.stderr.flush()
    # Chroma / CrewAI background threads can touch stdio during shutdown; brief pause avoids
    # "could not acquire lock for <stdin>" abort on some Linux setups.
    time.sleep(0.75)
