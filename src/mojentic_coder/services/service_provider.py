
"""
Service provider for the Mojentic Coder application.

This module provides a service provider that manages service instances
and provides them to the UI components.
"""
from typing import Dict, Type, TypeVar, Optional, Any

from mojentic_coder.services.interfaces import AgentServiceInterface, MessageServiceInterface, EngineeringGoalServiceInterface
from mojentic_coder.services.agent_service import AgentService
from mojentic_coder.services.message_service import MessageService
from mojentic_coder.services.engineering_goal_service import EngineeringGoalService


T = TypeVar('T')


class ServiceProvider:
    """
    Service provider that manages service instances.

    This class follows the service locator pattern to provide
    access to service implementations.
    """

    _instance = None

    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(ServiceProvider, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the service provider."""
        self._services: Dict[Type, Any] = {}

        # Register default service implementations
        self.register(AgentServiceInterface, AgentService())
        self.register(MessageServiceInterface, MessageService())
        self.register(EngineeringGoalServiceInterface, EngineeringGoalService())

    def register(self, interface: Type[T], implementation: T) -> None:
        """
        Register a service implementation.

        Args:
            interface: The service interface
            implementation: The service implementation
        """
        self._services[interface] = implementation

    def get(self, interface: Type[T]) -> Optional[T]:
        """
        Get a service implementation.

        Args:
            interface: The service interface

        Returns:
            The service implementation, or None if not registered
        """
        return self._services.get(interface)

    @classmethod
    def get_agent_service(cls) -> AgentServiceInterface:
        """
        Get the agent service.

        Returns:
            The agent service implementation
        """
        return cls().get(AgentServiceInterface)

    @classmethod
    def get_message_service(cls) -> MessageServiceInterface:
        """
        Get the message service.

        Returns:
            The message service implementation
        """
        return cls().get(MessageServiceInterface)

    @classmethod
    def get_engineering_goal_service(cls) -> EngineeringGoalServiceInterface:
        """
        Get the engineering goal service.

        Returns:
            The engineering goal service implementation
        """
        return cls().get(EngineeringGoalServiceInterface)
