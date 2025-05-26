
"""
Service interfaces for the Mojentic Coder application.

This module defines the interfaces for the application's services,
establishing a clear contract between the UI and the application logic.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Callable, Dict, Any

from mojentic.tracer import TracerSystem
from mojentic.tracer.tracer_events import TracerEvent

from mojentic_coder.models.agent import Agent, GatewayType
from mojentic_coder.models.engineering_goal import EngineeringGoal, Task


class AgentServiceInterface(ABC):
    """
    Interface for agent management services.

    This service handles the creation, retrieval, and management of agents.
    """

    @abstractmethod
    def create_agent(self, name: str, gateway_type: GatewayType, model: str, system_prompt: str) -> tuple[Agent, int]:
        """
        Create a new agent.

        Args:
            name: The name of the agent
            gateway_type: The type of LLM gateway to use
            model: The LLM model to use
            system_prompt: The system prompt that defines the agent's behavior

        Returns:
            A tuple containing the created agent and its index
        """
        pass

    @abstractmethod
    def get_agent(self, index: int) -> Optional[Agent]:
        """
        Get an agent by index.

        Args:
            index: The index of the agent to get

        Returns:
            The agent at the specified index, or None if the index is invalid
        """
        pass

    @abstractmethod
    def get_all_agents(self) -> List[Agent]:
        """
        Get all agents.

        Returns:
            A list of all agents
        """
        pass

    @abstractmethod
    def set_current_agent(self, agent: Agent) -> None:
        """
        Set the current agent.

        Args:
            agent: The agent to set as current
        """
        pass

    @abstractmethod
    def get_current_agent(self) -> Optional[Agent]:
        """
        Get the current agent.

        Returns:
            The current agent, or None if no agent is selected
        """
        pass

    @abstractmethod
    def get_available_models(self, gateway_type: GatewayType) -> List[str]:
        """
        Get the available models for a gateway type.

        Args:
            gateway_type: The gateway type to get models for

        Returns:
            A list of available model names
        """
        pass


class MessageServiceInterface(ABC):
    """
    Interface for message handling services.

    This service handles sending messages to agents and receiving responses asynchronously.
    """

    @abstractmethod
    def send_message(self, agent: Agent, message: str, callback: Callable[[Agent, str, Optional[Exception]], None]) -> None:
        """
        Send a message to an agent asynchronously.

        Args:
            agent: The agent to send the message to
            message: The message text to send
            callback: A callback function that will be called when the response is received
                     The callback takes three parameters: the agent, the response text, and an exception (if any)
        """
        pass

    @abstractmethod
    def get_chat_history(self, agent: Agent) -> List[Dict[str, Any]]:
        """
        Get the chat history for an agent.

        Args:
            agent: The agent to get the chat history for

        Returns:
            A list of message dictionaries with 'role' and 'content' keys
        """
        pass


class EngineeringGoalServiceInterface(ABC):
    """
    Interface for engineering goal management services.

    This service handles the creation, retrieval, and management of engineering goals and tasks.
    """

    @abstractmethod
    def create_goal(self, title: str, description: str = "") -> tuple[EngineeringGoal, int]:
        """
        Create a new engineering goal.

        Args:
            title: The title of the goal
            description: The description of the goal

        Returns:
            A tuple containing the created goal and its index
        """
        pass

    @abstractmethod
    def get_goal(self, index: int) -> Optional[EngineeringGoal]:
        """
        Get a goal by index.

        Args:
            index: The index of the goal to get

        Returns:
            The goal at the specified index, or None if the index is invalid
        """
        pass

    @abstractmethod
    def get_all_goals(self) -> List[EngineeringGoal]:
        """
        Get all goals.

        Returns:
            A list of all goals
        """
        pass

    @abstractmethod
    def add_task(self, goal_index: int, title: str, description: str = "") -> tuple[Task, int]:
        """
        Add a task to a goal.

        Args:
            goal_index: The index of the goal to add the task to
            title: The title of the task
            description: The description of the task

        Returns:
            A tuple containing the created task and its index within the goal
        """
        pass

    @abstractmethod
    def update_task_status(self, goal_index: int, task_index: int, completed: bool) -> bool:
        """
        Update the status of a task.

        Args:
            goal_index: The index of the goal containing the task
            task_index: The index of the task to update
            completed: The new completed status

        Returns:
            True if the task was updated, False otherwise
        """
        pass


class TracerServiceInterface(ABC):
    """
    Interface for tracer services.

    This service provides a TracerSystem with an observable EventStore for tracing
    LLM interactions and tool usage.
    """

    @abstractmethod
    def get_tracer_system(self) -> TracerSystem:
        """
        Get the tracer system.

        Returns:
            The tracer system
        """
        pass

    @abstractmethod
    def register_callback(self, callback: Callable[[TracerEvent], None]) -> None:
        """
        Register a callback function to be called when a new event is stored.

        Args:
            callback: The callback function to register
        """
        pass

    @abstractmethod
    def get_events(self) -> List[TracerEvent]:
        """
        Get all events from the tracer system.

        Returns:
            A list of all tracer events
        """
        pass
