"""
Tracer panel for the Mojentic Coder application.

This panel displays tracer events from the TracerSystem.
"""
from typing import Optional, List, Callable

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal

from mojentic.tracer import TracerSystem
from mojentic.tracer.tracer_events import TracerEvent


class TracerPanel(QWidget):
    """
    Panel for displaying tracer events.

    This panel shows a list of tracer events captured by the TracerSystem.
    """

    def __init__(self, tracer_system: TracerSystem):
        """
        Initialize the tracer panel.

        Args:
            tracer_system: The tracer system to display events from
        """
        super().__init__()

        self.tracer_system = tracer_system

        # Set up the layout
        layout = QVBoxLayout(self)

        # Label for the panel
        layout.addWidget(QLabel("Tracer Events"))

        # List of tracer events
        self.event_list = QListWidget()
        layout.addWidget(self.event_list)

        # We need to get the tracer service to register our callback
        from mojentic_coder.services.service_provider import ServiceProvider
        from mojentic_coder.services.interfaces import TracerServiceInterface

        tracer_service = ServiceProvider.get_tracer_service()
        tracer_service.register_callback(self.on_event_stored)

        # Populate the list with existing events
        self.populate_event_list()

    def on_event_stored(self, event: TracerEvent):
        """
        Callback function for when a new event is stored in the tracer system.

        Args:
            event: The tracer event that was stored
        """
        # Add the event to the list
        self.add_event_to_list(event)

        # Scroll to the bottom to show the latest event
        self.event_list.scrollToBottom()

    def populate_event_list(self):
        """
        Populate the event list with existing events from the tracer system.
        """
        # Clear the list first
        self.event_list.clear()

        # Get all events from the tracer system
        events = self.tracer_system.get_events()

        # Add each event to the list
        for event in events:
            self.add_event_to_list(event)

    def add_event_to_list(self, event: TracerEvent):
        """
        Add a tracer event to the list widget.

        Args:
            event: The tracer event to add
        """
        # Create a list item with the event summary
        item = QListWidgetItem(event.printable_summary())

        # Add the item to the list
        self.event_list.addItem(item)
