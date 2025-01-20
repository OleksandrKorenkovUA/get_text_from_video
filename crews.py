from crewai.project import CrewBase, agent, crew, task
from crewai import Agent, Crew, Task, Process
from pydantic import BaseModel, Field
from crewai.llm import LLM
import os
os.environ["OTEL_SDK_DISABLED"] = "true"


llm = LLM(
    model="llama3.2:3b",
    base_url="http://localhost:11434"
)


class Texted(BaseModel):
    """Description of the text"""
    body: str = Field(..., description="Body of the text")


@CrewBase
class TranslationCrew():
    """Translation crew"""
    agents_config = 'agents.yaml'
    tasks_config = 'tasks.yaml'
    
    @agent
    def translator(self) -> Agent:
        return Agent(
            config=self.agents_config['translator'],
            verbose=True,
            memory=False,
            llm=llm
        )

    @task
    def translation_task(self) -> Task:
        return Task(
            config=self.tasks_config['translation_task'],
            agent=self.translator(),
            expected_output='string',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Translation crew"""
        return Crew(
            agents=[self.translator()],
            tasks=[self.translation_task()],
            process=Process.sequential,
            verbose=True,
        )

@CrewBase
class SummarizationCrew():
    """Summarization crew"""
    agents_config = 'agents.yaml'
    tasks_config = 'tasks.yaml'
    
    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            verbose=True,
            memory=False,
            llm=llm
        )

    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config['summary_task'],
            agent=self.analyst(),
            expected_output='string',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Summarization crew"""
        return Crew(
            agents=[self.analyst()],
            tasks=[self.summary_task()],
            process=Process.sequential,
            verbose=True,
        )

@CrewBase
class CorrectionCrew():
    """Correction crew"""
    agents_config = 'agents.yaml'
    tasks_config = 'tasks.yaml'
    
    @agent
    def corrector(self) -> Agent:
        return Agent(
            config=self.agents_config['corrector'],
            verbose=True,
            memory=False,
            llm=llm
        )

    @task
    def correction_task(self) -> Task:
        return Task(
            config=self.tasks_config['correction_task'],
            agent=self.corrector(),
            expected_output='string',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Correction crew"""
        return Crew(
            agents=[self.corrector()],
            tasks=[self.correction_task()],
            process=Process.sequential,
            verbose=True,
        )
