from crewai.project import CrewBase, agent, crew, task
from crewai import Agent, Crew, Task, Process
from pydantic import BaseModel, Field
from crewai.llm import LLM
import os
os.environ["OTEL_SDK_DISABLED"] = "true"
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))


#Для використання безкоштовних opensource моделей з ollama 
llm = LLM(
    model="ollama/llama3.1:latest",
    base_url="http://localhost:11434"
)

#Для використання OpenAI API 
'''llm = LLM(model="gpt-4")'''

class Texted(BaseModel):
    body: str = Field(..., description="Текст")


@CrewBase
class TranslationCrew():
    """Команда для перекладу"""
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
        return Crew(
            agents=[self.translator()],
            tasks=[self.translation_task()],
            process=Process.sequential,
            verbose=True,
        )

@CrewBase
class SummarizationCrew():
    """Команда для аналізу"""
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
        return Crew(
            agents=[self.analyst()],
            tasks=[self.summary_task()],
            process=Process.sequential,
            verbose=True,
        )

@CrewBase
class CorrectionCrew():
    """Команда для виправлення тексту"""
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
        return Crew(
            agents=[self.corrector()],
            tasks=[self.correction_task()],
            process=Process.sequential,
            verbose=True,
        )
