
"""
Agent service implementation for the Mojentic Coder application.

This module provides the implementation of the AgentServiceInterface,
handling the creation and management of agents.
"""
import os
from typing import List, Optional, Dict, Any

from mojentic.llm.gateways.openai import OpenAIGateway
from mojentic.llm.gateways.ollama import OllamaGateway
from mojentic.llm import LLMBroker, ChatSession
from mojentic.tracer import TracerSystem

from mojentic_coder.models.agent import Agent, GatewayType
from mojentic_coder.services.interfaces import AgentServiceInterface
from mojentic_coder.services.service_provider import ServiceProvider


class AgentService(AgentServiceInterface):
    """
    Implementation of the AgentServiceInterface.

    This service handles the creation, retrieval, and management of agents.
    """

    def __init__(self):
        """Initialize the agent service."""
        self.agents: List[Agent] = []
        self.current_agent: Optional[Agent] = None
        # We'll get the tracer service when needed to avoid circular imports
        self._tracer_service = None

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
        # Create the LLM gateway instance based on the gateway type
        llm_gateway = None
        if gateway_type == GatewayType.OPENAI:
            api_key = os.environ.get("OPENAI_API_KEY", "")
            if not api_key:
                raise ValueError("OpenAI API key not found in environment variables")
            llm_gateway = OpenAIGateway(api_key)
        elif gateway_type == GatewayType.OLLAMA:
            llm_gateway = OllamaGateway()

        if not llm_gateway:
            raise ValueError(f"Failed to create gateway for type: {gateway_type}")

        # Get the tracer system from the tracer service
        if self._tracer_service is None:
            from mojentic_coder.services.interfaces import TracerServiceInterface
            self._tracer_service = ServiceProvider().get(TracerServiceInterface)

        tracer_system = self._tracer_service.get_tracer_system()

        # Create an LLM broker with the gateway and tracer
        llm_broker = LLMBroker(model=model, gateway=llm_gateway, tracer=tracer_system)

        # Create a chat session with the LLM broker and system message
        chat_session = ChatSession(
            llm_broker,
            system_prompt=system_prompt
        )

        # Create the agent
        agent = Agent(
            name=name,
            gateway=gateway_type,
            model=model,
            system_prompt=system_prompt,
            llm_gateway=llm_gateway,
            llm_broker=llm_broker,
            chat_session=chat_session
        )

        # Add the agent to the list
        self.agents.append(agent)
        agent_index = len(self.agents) - 1

        # Set as current agent if it's the first one
        if len(self.agents) == 1:
            self.current_agent = agent

        return agent, agent_index

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

    def get_all_agents(self) -> List[Agent]:
        """
        Get all agents.

        Returns:
            A list of all agents
        """
        return self.agents.copy()

    def set_current_agent(self, agent: Agent) -> None:
        """
        Set the current agent.

        Args:
            agent: The agent to set as current
        """
        self.current_agent = agent

        # Ensure the agent has a chat session
        if not agent.chat_session:
            agent.chat_session = ChatSession(
                agent.llm_broker,
                system_prompt=agent.system_prompt
            )

    def get_current_agent(self) -> Optional[Agent]:
        """
        Get the current agent.

        Returns:
            The current agent, or None if no agent is selected
        """
        return self.current_agent

    def get_available_models(self, gateway_type: GatewayType) -> List[str]:
        """
        Get the available models for a gateway type.

        Args:
            gateway_type: The gateway type to get models for

        Returns:
            A list of available model names
        """
        models = []

        if gateway_type == GatewayType.OPENAI:
            api_key = os.environ.get("OPENAI_API_KEY", "")
            if api_key:
                try:
                    gateway = OpenAIGateway(api_key)
                    models = gateway.get_available_models()
                except Exception as e:
                    print(f"Error initializing OpenAI gateway: {e}")

        elif gateway_type == GatewayType.OLLAMA:
            try:
                gateway = OllamaGateway()
                models = gateway.get_available_models()
            except Exception as e:
                print(f"Error initializing Ollama gateway: {e}")

        return models
