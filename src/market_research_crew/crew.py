from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MarketResearchCrew():
    """MarketResearchCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def market_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['market_analyst_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def customer_research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['customer_research_agent'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def competitive_intelligence_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['competitive_intelligence_agent'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def data_validation_research_integrity_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_validation_research_integrity_agent'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def insight_synthesizer_strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['insight_synthesizer_strategy_agent'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def domain_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['domain_expert_agent'], # type: ignore[index]
            verbose=True
        )
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def market_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_analysis_task'], # type: ignore[index]
        )

    @task
    def customer_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['customer_research_task'], # type: ignore[index]
        )
    
    @task
    def competitive_intelligence_task(self) -> Task:
        return Task(
            config=self.tasks_config['competitive_intelligence_task'], # type: ignore[index]
        )
    
    @task
    def data_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_validation_task'], # type: ignore[index]
        )

    @task
    def insight_synthesis_task(self) -> Task:
        return Task(
            config=self.tasks_config['insight_synthesis_task'], # type: ignore[index]
        )
    
    @task
    def domain_expert_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['domain_expert_review_task'], # type: ignore[index]
            output_file='reports/researches.md'
        )


    @crew
    def crew(self) -> Crew:
        """Creates the MarketResearchCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
