
"""
Message service implementation for the Mojentic Coder application.

This module provides the implementation of the MessageServiceInterface,
handling asynchronous message sending and chat history retrieval.
"""
import threading
from typing import List, Optional, Dict, Any, Callable

from mojentic.llm.gateways.models import MessageRole

from mojentic_coder.models.agent import Agent
from mojentic_coder.services.interfaces import MessageServiceInterface


class MessageService(MessageServiceInterface):
    """
    Implementation of the MessageServiceInterface.

    This service handles sending messages to agents and receiving responses asynchronously.
    """

    def send_message(self, agent: Agent, message: str, callback: Callable[[Agent, str, Optional[Exception]], None]) -> None:
        """
        Send a message to an agent asynchronously.

        Args:
            agent: The agent to send the message to
            message: The message text to send
            callback: A callback function that will be called when the response is received
                     The callback takes three parameters: the agent, the response text, and an exception (if any)
        """
        if not agent or not agent.chat_session:
            callback(agent, None, ValueError("Agent or chat session not available"))
            return

        # Create a thread to send the message and get the response
        thread = threading.Thread(
            target=self._send_message_thread,
            args=(agent, message, callback)
        )
        thread.daemon = True  # Thread will exit when the main program exits
        thread.start()

    def _send_message_thread(self, agent: Agent, message: str, callback: Callable[[Agent, str, Optional[Exception]], None]) -> None:
        """
        Thread function to send a message and get a response.

        Args:
            agent: The agent to send the message to
            message: The message text to send
            callback: A callback function that will be called when the response is received
        """
        try:
            # Send the message and get the response
            response_text = agent.chat_session.send(message)

            # Call the callback with the agent and response
            callback(agent, response_text, None)
        except Exception as e:
            # Call the callback with the agent and exception
            callback(agent, None, e)

    def get_chat_history(self, agent: Agent) -> List[Dict[str, Any]]:
        """
        Get the chat history for an agent.

        Args:
            agent: The agent to get the chat history for

        Returns:
            A list of message dictionaries with 'role' and 'content' keys
        """
        if not agent or not agent.chat_session:
            return []

        # Convert the chat session messages to a list of dictionaries
        history = []

        # Skip the first message (system prompt)
        for message in agent.chat_session.messages[1:]:
            history.append({
                'role': message.role.value,
                'content': message.content
            })

        return history
