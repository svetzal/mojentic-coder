"""
Tests for the MessageService.

This module demonstrates how to test the MessageService by mocking the mojentic framework.
"""
import pytest
from pytest import fixture

from mojentic.llm.gateways.models import LLMMessage, MessageRole

from mojentic_coder.models.agent import Agent, GatewayType
from mojentic_coder.services.message_service import MessageService


@fixture
def mock_chat_session(mocker):
    mock_session = mocker.MagicMock()
    mock_session.messages = [
        LLMMessage(role=MessageRole.System, content="System prompt"),
        LLMMessage(role=MessageRole.User, content="User message"),
        LLMMessage(role=MessageRole.Assistant, content="Assistant response")
    ]
    mock_session.send.return_value = "Mock response"
    return mock_session


@fixture
def test_agent(mock_chat_session, mocker):
    return Agent(
        name="Test Agent",
        gateway=GatewayType.OLLAMA,
        model="llama2",
        system_prompt="You are a test agent",
        llm_gateway=mocker.MagicMock(),
        llm_broker=mocker.MagicMock(),
        chat_session=mock_chat_session
    )


@fixture
def message_service():
    return MessageService()


def test_should_get_chat_history(message_service, test_agent):
    # Call the method
    history = message_service.get_chat_history(test_agent)

    # Check the result
    assert len(history) == 2  # Should skip the system prompt
    assert history[0]['role'] == MessageRole.User.value
    assert history[0]['content'] == "User message"
    assert history[1]['role'] == MessageRole.Assistant.value
    assert history[1]['content'] == "Assistant response"


def test_should_send_message_successfully(message_service, test_agent, mocker):
    # Create a mock callback
    callback = mocker.MagicMock()

    # Use a synchronous approach instead of threading for testing
    # Patch the _send_message_thread method to call it directly
    mocker.patch.object(
        message_service, 
        '_send_message_thread',
        side_effect=lambda agent, message, cb: cb(agent, "Mock response", None)
    )

    # Call the method
    message_service.send_message(test_agent, "Test message", callback)

    # Check that the callback was called with the agent and response
    callback.assert_called_once_with(test_agent, "Mock response", None)


def test_should_handle_send_message_error(message_service, test_agent, mocker):
    # Create a mock callback
    callback = mocker.MagicMock()

    # Use a synchronous approach instead of threading for testing
    # Patch the _send_message_thread method to call it directly with an error
    test_error = Exception("Test error")
    mocker.patch.object(
        message_service, 
        '_send_message_thread',
        side_effect=lambda agent, message, cb: cb(agent, None, test_error)
    )

    # Call the method
    message_service.send_message(test_agent, "Test message", callback)

    # Check that the callback was called with the agent and error
    callback.assert_called_once_with(test_agent, None, test_error)


def test_should_handle_message_thread_success(message_service, test_agent, mock_chat_session, mocker):
    # Create a mock callback
    callback = lambda agent, response, error: None
    callback = mocker.Mock(side_effect=callback)

    # Call the method directly
    message_service._send_message_thread(test_agent, "Test message", callback)

    # Check that the chat session's send method was called
    mock_chat_session.send.assert_called_once_with("Test message")

    # Check that the callback was called with the agent and response
    callback.assert_called_once_with(test_agent, "Mock response", None)


def test_should_handle_message_thread_error(message_service, test_agent, mock_chat_session, mocker):
    # Make the chat session's send method raise an exception
    test_error = Exception("Test error")
    mock_chat_session.send.side_effect = test_error

    # Create a mock callback
    callback = lambda agent, response, error: None
    callback = mocker.Mock(side_effect=callback)

    # Call the method directly
    message_service._send_message_thread(test_agent, "Test message", callback)

    # Check that the callback was called with the agent and error
    callback.assert_called_once_with(test_agent, None, test_error)
