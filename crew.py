import sys
import time

from crewai import Crew, Process
from agents import blog_researcher, blog_writer
from tasks import research_task, write_task

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
    result = crew.kickoff(inputs={"topic": "Why Oracle Laid Off 30k Employees Despite Strong Revenue Growth"})
    print(result)
    sys.stdout.flush()
    sys.stderr.flush()
    # Chroma / CrewAI background threads can touch stdio during shutdown; brief pause avoids
    # "could not acquire lock for <stdin>" abort on some Linux setups.
    time.sleep(0.75)