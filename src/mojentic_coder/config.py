"""
Global application configuration for the Mojentic Coder application.
"""
from typing import List, Optional

from mojentic_coder.models.agent import Agent


class AppConfig:
    """
    Global application configuration class.

    This class holds application-wide state and configuration,
    such as the list of available agents and the currently selected agent.
    """

    def __init__(self):
        """Initialize the application configuration."""
        self.agents: List[Agent] = []
        self.current_agent: Optional[Agent] = None
        self.project_folder: str = ""

    def add_agent(self, agent: Agent) -> int:
        """
        Add an agent to the configuration.

        Args:
            agent: The agent to add

        Returns:
            The index of the added agent
        """
        self.agents.append(agent)
        return len(self.agents) - 1

    def get_agent(self, index: int) -> Optional[Agent]:
        """
        Get an agent by index.

        Args:
            index: The index of the agent to get

        Returns:
            The agent at the specified index, or None if the index is invalid
        """
        if 0 <= index < len(self.agents):
            return self.agents[index]
        return None

    def set_current_agent(self, agent: Agent) -> None:
        """
        Set the current agent.

        Args:
            agent: The agent to set as current
        """
        self.current_agent = agent
