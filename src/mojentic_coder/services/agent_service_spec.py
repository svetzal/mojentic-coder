"""
Tests for the AgentService.

This module demonstrates how to test the AgentService by mocking the mojentic framework.
"""
import pytest
from pytest import fixture

from mojentic_coder.models.agent import Agent, GatewayType
from mojentic_coder.services.agent_service import AgentService


@fixture
def agent_service():
    return AgentService()


def test_should_create_agent_with_ollama_gateway(agent_service, mocker):
    # Set up mocks
    mock_ollama_gateway = mocker.MagicMock()
    mock_ollama_gateway_class = mocker.patch('mojentic_coder.services.agent_service.OllamaGateway', return_value=mock_ollama_gateway)

    mock_llm_broker = mocker.MagicMock()
    mock_llm_broker_class = mocker.patch('mojentic_coder.services.agent_service.LLMBroker', return_value=mock_llm_broker)

    mock_chat_session = mocker.MagicMock()
    mock_chat_session_class = mocker.patch('mojentic_coder.services.agent_service.ChatSession', return_value=mock_chat_session)

    # Mock the tracer service and tracer system
    mock_tracer_system = mocker.MagicMock()
    mock_tracer_service = mocker.MagicMock()
    mock_tracer_service.get_tracer_system.return_value = mock_tracer_system

    # Mock the ServiceProvider.get method to return our mock tracer service
    mock_get = mocker.patch('mojentic_coder.services.service_provider.ServiceProvider.get', return_value=mock_tracer_service)

    # Call the method
    agent, index = agent_service.create_agent(
        name="Test Agent",
        gateway_type=GatewayType.OLLAMA,
        model="llama2",
        system_prompt="You are a test agent"
    )

    # Check the result
    assert agent.name == "Test Agent"
    assert agent.gateway == GatewayType.OLLAMA
    assert agent.model == "llama2"
    assert agent.system_prompt == "You are a test agent"
    assert agent.llm_gateway == mock_ollama_gateway
    assert agent.llm_broker == mock_llm_broker
    assert agent.chat_session == mock_chat_session
    assert index == 0

    # Check that the agent was added to the list
    assert len(agent_service.agents) == 1
    assert agent_service.agents[0] == agent

    # Check that the agent was set as current
    assert agent_service.current_agent == agent

    # Check that the mocks were called correctly
    mock_ollama_gateway_class.assert_called_once()
    mock_llm_broker_class.assert_called_once_with(model="llama2", gateway=mock_ollama_gateway, tracer=mock_tracer_system)
    mock_chat_session_class.assert_called_once_with(mock_llm_broker, system_prompt="You are a test agent")


def test_should_get_agent_by_index(agent_service):
    # Create a test agent
    agent = Agent(
        name="Test Agent",
        gateway=GatewayType.OLLAMA,
        model="llama2",
        system_prompt="You are a test agent"
    )
    agent_service.agents.append(agent)

    # Call the method
    result = agent_service.get_agent(0)

    # Check the result
    assert result == agent

    # Test with invalid index
    assert agent_service.get_agent(1) is None


def test_should_get_all_agents(agent_service):
    # Create test agents
    agent1 = Agent(
        name="Test Agent 1",
        gateway=GatewayType.OLLAMA,
        model="llama2",
        system_prompt="You are test agent 1"
    )
    agent2 = Agent(
        name="Test Agent 2",
        gateway=GatewayType.OLLAMA,
        model="llama2",
        system_prompt="You are test agent 2"
    )
    agent_service.agents = [agent1, agent2]

    # Call the method
    result = agent_service.get_all_agents()

    # Check the result
    assert len(result) == 2
    assert result[0] == agent1
    assert result[1] == agent2

    # Check that it's a copy, not the original list
    assert result is not agent_service.agents


def test_should_set_current_agent(agent_service, mocker):
    # Create a test agent
    agent = Agent(
        name="Test Agent",
        gateway=GatewayType.OLLAMA,
        model="llama2",
        system_prompt="You are a test agent",
        llm_broker=mocker.MagicMock()
    )

    # Create a mock ChatSession
    mock_chat_session = mocker.MagicMock()
    mock_chat_session_class = mocker.patch('mojentic_coder.services.agent_service.ChatSession', return_value=mock_chat_session)

    # Call the method
    agent_service.set_current_agent(agent)

    # Check the result
    assert agent_service.current_agent == agent

    # Check that a chat session was created
    mock_chat_session_class.assert_called_once_with(
        agent.llm_broker,
        system_prompt=agent.system_prompt
    )
    assert agent.chat_session == mock_chat_session
