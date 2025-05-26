"""
Agent data model for the Mojentic Coder application.
"""
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field

from mojentic.llm import ChatSession


class GatewayType(str, Enum):
    """Type of LLM gateway."""
    OPENAI = "OpenAI"
    OLLAMA = "Ollama"


class AgentStatus(str, Enum):
    """Status of an agent."""
    IDLE = "Idle"
    WORKING = "Working"


class Agent(BaseModel):
    """
    Agent model representing an AI assistant in the system.

    Attributes:
        name: Unique name for the agent
        gateway: The LLM gateway type (OpenAI or Ollama)
        model: The specific LLM model to use
        system_prompt: Instructions that define the agent's character and behavior
        status: Current status of the agent (Idle or Working)
        llm_gateway: The LLM gateway instance
        llm_broker: The LLM broker instance
        chat_session: The chat session for this agent
    """
    model_config = {"arbitrary_types_allowed": True}
    name: str = Field(..., description="Unique name for the agent")
    gateway: GatewayType = Field(..., description="LLM gateway type")
    model: str = Field(..., description="LLM model name")
    system_prompt: str = Field(..., description="Instructions that define the agent's character and behavior")
    status: AgentStatus = Field(default=AgentStatus.IDLE, description="Current status of the agent")
    llm_gateway: Optional[Any] = Field(None, description="LLM gateway instance")
    llm_broker: Optional[Any] = Field(None, description="LLM broker instance")
    chat_session: Optional[Any] = Field(None, description="Chat session for this agent")
