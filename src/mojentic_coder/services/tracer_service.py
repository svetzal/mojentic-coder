"""
Tracer service implementation for the Mojentic Coder application.

This module provides a service for tracing LLM interactions and tool usage.
"""
from typing import Optional, List, Callable

from mojentic.tracer import TracerSystem
from mojentic.tracer.event_store import EventStore
from mojentic.tracer.tracer_events import TracerEvent

from mojentic_coder.services.interfaces import TracerServiceInterface


class TracerService(TracerServiceInterface):
    """
    Implementation of the TracerServiceInterface.

    This service provides a TracerSystem with an observable EventStore for tracing
    LLM interactions and tool usage.
    """

    def __init__(self):
        """Initialize the tracer service."""
        # Create an EventStore (callbacks will be added later)
        self.event_store = EventStore()
        self.callbacks = []

        # Create a TracerSystem with the EventStore
        self.tracer_system = TracerSystem(event_store=self.event_store)

    def get_tracer_system(self) -> TracerSystem:
        """
        Get the tracer system.

        Returns:
            The tracer system
        """
        return self.tracer_system

    def register_callback(self, callback: Callable[[TracerEvent], None]) -> None:
        """
        Register a callback function to be called when a new event is stored.

        Args:
            callback: The callback function to register
        """
        # Store the callback
        self.callbacks.append(callback)

        # Create a new event store with all callbacks
        def combined_callback(event: TracerEvent) -> None:
            for cb in self.callbacks:
                cb(event)

        # Replace the event store with a new one that has the combined callback
        old_events = self.event_store.get_events()
        self.event_store = EventStore(on_store_callback=combined_callback)

        # Add the old events to the new event store
        for event in old_events:
            self.event_store.store_event(event)

        # Update the tracer system with the new event store
        self.tracer_system = TracerSystem(event_store=self.event_store)

    def get_events(self) -> List[TracerEvent]:
        """
        Get all events from the tracer system.

        Returns:
            A list of all tracer events
        """
        return self.tracer_system.get_events()
