"""
Chat Session panel for the Mojentic Coder application.
"""
from typing import Optional, List, Callable, Dict, Any

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QLineEdit
)
from PySide6.QtCore import Qt, Signal

from mojentic.llm.gateways.models import MessageRole
from mojentic_coder.models.agent import Agent, AgentStatus
from mojentic_coder.config import AppConfig
from mojentic_coder.services.service_provider import ServiceProvider
from mojentic_coder.services.interfaces import AgentServiceInterface, MessageServiceInterface


class ChatSessionPanel(QWidget):
    """
    Panel for chat interactions with agents.

    This panel displays the chat history and allows sending messages to the current agent.
    """

    # Signals
    agent_status_changed = Signal(Agent, int)  # Emitted when an agent's status changes (agent, index)

    def __init__(self, app_config: AppConfig):
        """
        Initialize the chat session panel.

        Args:
            app_config: The application configuration
        """
        super().__init__()

        self.app_config = app_config

        # Get services from the service provider
        self.agent_service = ServiceProvider.get_agent_service()
        self.message_service = ServiceProvider.get_message_service()

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Chat Session"))

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Message input area
        message_widget = QWidget()
        message_layout = QHBoxLayout(message_widget)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        message_layout.addWidget(self.message_input)
        message_layout.addWidget(self.send_button)

        layout.addWidget(message_widget)

        # Disable chat until an agent is created
        self.message_input.setEnabled(False)
        self.send_button.setEnabled(False)


    def render_chat_messages(self, agent: Agent):
        """
        Render all messages from the agent's chat session.

        Args:
            agent: The agent whose chat session to render
        """
        if not agent:
            return

        self.chat_display.clear()
        self.chat_display.append(f"Chat session with agent: {agent.name}")

        # Get chat history from the message service
        chat_history = self.message_service.get_chat_history(agent)

        # Render each message
        for message in chat_history:
            if message['role'] == MessageRole.User.value:
                self.chat_display.append(f"You: {message['content']}")
            elif message['role'] == MessageRole.Assistant.value:
                self.chat_display.append(f"{agent.name}: {message['content']}")

    def set_current_agent(self, agent: Agent):
        """
        Set the current agent and update the UI.

        Args:
            agent: The agent to set as current
        """
        # Set the current agent in the service
        self.agent_service.set_current_agent(agent)

        # Enable chat
        self.message_input.setEnabled(True)
        self.send_button.setEnabled(True)

        # Render the chat messages
        self.render_chat_messages(agent)


    def send_message(self):
        """Send a message to the current agent."""
        current_agent = self.agent_service.get_current_agent()
        if not current_agent:
            return

        message_text = str(self.message_input.text())
        if not message_text:
            return

        # Update UI
        self.chat_display.append(f"You: {message_text}")
        self.message_input.clear()

        # Update agent status to Working
        current_agent.status = AgentStatus.WORKING

        # Find the agent index
        all_agents = self.agent_service.get_all_agents()
        agent_index = all_agents.index(current_agent)

        # Emit the agent_status_changed signal
        self.agent_status_changed.emit(current_agent, agent_index)

        # Use the MessageService to send the message asynchronously
        self.message_service.send_message(
            current_agent, 
            message_text,
            self.handle_message_response
        )

    def handle_message_response(self, agent: Agent, response_text: Optional[str], error: Optional[Exception]) -> None:
        """
        Handle the response from an asynchronous message send.

        Args:
            agent: The agent that sent the message
            response_text: The response text from the agent, or None if there was an error
            error: The exception that occurred, or None if the message was sent successfully
        """
        if not agent:
            return

        # Check if this agent is the current agent to update the UI
        current_agent = self.agent_service.get_current_agent()
        is_current_agent = (current_agent and agent.name == current_agent.name)

        if error:
            # Handle any errors
            error_message = f"Error getting response from agent: {str(error)}"
            print(error_message)
            if is_current_agent:
                self.chat_display.append(f"{agent.name}: Error: {error_message}")
        else:
            # Update UI with the response if this is the current agent
            if is_current_agent:
                self.chat_display.append(f"{agent.name}: {response_text}")

        # Update agent status to Idle
        agent.status = AgentStatus.IDLE

        # Find the agent index
        all_agents = self.agent_service.get_all_agents()
        agent_index = all_agents.index(agent)

        # Emit the agent_status_changed signal
        self.agent_status_changed.emit(agent, agent_index)

    def receive_agent_response(self, response_text: str):
        """
        Handle a response from the agent (legacy method, kept for backward compatibility).

        Args:
            response_text: The text response from the agent
        """
        current_agent = self.agent_service.get_current_agent()
        if not current_agent:
            return

        # Update UI
        self.chat_display.append(f"{current_agent.name}: {response_text}")
