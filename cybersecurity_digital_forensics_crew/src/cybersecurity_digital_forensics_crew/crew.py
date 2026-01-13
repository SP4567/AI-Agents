from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class CybersecurityDigitalForensicsCrew:
    """
    Cybersecurity & Digital Forensics Crew
    -------------------------------------
    SOC analysis, malware analysis, forensic timeline reconstruction,
    and incident decision-making with human-in-the-loop design.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ------------------------------------------------------------------
    # AGENTS
    # ------------------------------------------------------------------

    @agent
    def soc_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["soc_analyst"],  # agents.yaml
            verbose=True
        )

    @agent
    def malware_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["malware_analyst"],
            verbose=True
        )

    @agent
    def forensics_examiner(self) -> Agent:
        return Agent(
            config=self.agents_config["forensics_examiner"],
            verbose=True
        )

    @agent
    def incident_commander(self) -> Agent:
        return Agent(
            config=self.agents_config["incident_commander"],
            verbose=True
        )

    # ------------------------------------------------------------------
    # TASKS
    # ------------------------------------------------------------------

    @task
    def soc_log_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["soc_log_analysis"]
        )

    @task
    def malware_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["malware_analysis"]
        )

    @task
    def forensic_timeline_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["forensic_timeline_analysis"]
        )

    @task
    def incident_correlation_and_decision(self) -> Task:
        return Task(
            config=self.tasks_config["incident_correlation_and_decision"],
            output_file="reports/case_summary.md"
        )

    # ------------------------------------------------------------------
    # CREW
    # ------------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        """
        Creates the Cybersecurity & Digital Forensics crew
        """

        return Crew(
            agents=self.agents,   # auto-built via @agent
            tasks=self.tasks,     # auto-built via @task
            process=Process.sequential,
            verbose=True
        )