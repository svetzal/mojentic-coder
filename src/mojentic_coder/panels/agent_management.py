"""
Agent Management panel for the Mojentic Coder application.
"""
from typing import Callable, Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QDialog, QFormLayout, QLineEdit, QTextEdit, QComboBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

from mojentic_coder.models.agent import Agent, GatewayType, AgentStatus
from mojentic_coder.config import AppConfig
from mojentic_coder.services.service_provider import ServiceProvider
from mojentic_coder.services.interfaces import AgentServiceInterface


class AgentManagementPanel(QWidget):
    """
    Panel for managing agents in the application.

    This panel allows users to create, select, and manage agents.
    """

    # Signals
    agent_selected = Signal(Agent)  # Emitted when an agent is selected
    agent_created = Signal(Agent, int)  # Emitted when a new agent is created (agent, index)

    def __init__(self, app_config: AppConfig):
        """
        Initialize the agent management panel.

        Args:
            app_config: The application configuration
        """
        super().__init__()

        self.app_config = app_config

        # Get services from the service provider
        self.agent_service = ServiceProvider.get_agent_service()

        # Set up the layout
        layout = QVBoxLayout(self)

        # Button bar at the top
        button_bar = QWidget()
        button_bar_layout = QHBoxLayout(button_bar)
        button_bar_layout.setContentsMargins(0, 0, 0, 0)

        # Label for the panel
        button_bar_layout.addWidget(QLabel("Agent Management"))
        button_bar_layout.addStretch()

        # Create Agent button (+ sign)
        self.create_agent_button = QPushButton("+")
        self.create_agent_button.clicked.connect(self.show_create_agent_dialog)
        button_bar_layout.addWidget(self.create_agent_button)

        layout.addWidget(button_bar)

        # List of agents (spans full height)
        self.agent_list = QListWidget()
        self.agent_list.itemClicked.connect(self.select_agent)
        layout.addWidget(self.agent_list)

        # Populate the agent list with existing agents
        self.populate_agent_list()

        # Initialize agent form widgets (will be used in the dialog)
        self.agent_name_input = QLineEdit()
        self.gateway_combo = QComboBox()
        self.gateway_combo.addItem("Choose...")
        self.gateway_combo.addItems([gt.value for gt in GatewayType])
        self.gateway_combo.currentIndexChanged.connect(self.update_models)

        self.model_combo = QComboBox()
        # Initialize model combo box with "Choose..." entry
        self.model_combo.addItem("Choose...")

        self.system_prompt_input = QTextEdit()
        self.system_prompt_input.setPlaceholderText("Enter system prompt that defines the agent's character and behavior...")

    def show_create_agent_dialog(self):
        """Show the modal dialog for creating a new agent."""
        # Create the dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Agent")
        dialog.setMinimumWidth(400)

        # Create the form layout
        form_layout = QFormLayout(dialog)

        # Reset form fields
        self.agent_name_input.clear()
        self.gateway_combo.setCurrentIndex(0)
        self.model_combo.clear()
        self.model_combo.addItem("Choose...")
        self.system_prompt_input.clear()

        # Add form fields to the dialog
        form_layout.addRow("Name:", self.agent_name_input)
        form_layout.addRow("Gateway:", self.gateway_combo)
        form_layout.addRow("Model:", self.model_combo)
        form_layout.addRow("System Prompt:", self.system_prompt_input)

        # Add buttons
        button_layout = QHBoxLayout()
        create_button = QPushButton("Create")
        cancel_button = QPushButton("Cancel")

        button_layout.addWidget(create_button)
        button_layout.addWidget(cancel_button)
        form_layout.addRow("", button_layout)

        # Connect buttons
        create_button.clicked.connect(lambda: self.create_agent(dialog))
        cancel_button.clicked.connect(dialog.reject)

        # Show the dialog
        dialog.exec()

    def create_agent(self, dialog: Optional[QDialog] = None):
        """
        Create a new agent from the form inputs.

        Args:
            dialog: The dialog to close after creating the agent
        """
        name = self.agent_name_input.text()
        gateway_text = self.gateway_combo.currentText()
        model = self.model_combo.currentText()
        system_prompt = self.system_prompt_input.toPlainText()

        # Validate that a valid gateway and model are selected (not the "Choose..." entry)
        if not all([name, system_prompt]) or gateway_text == "Choose..." or model == "Choose...":
            # TODO: Show error message
            return

        try:
            gateway_type = GatewayType(gateway_text)
        except ValueError:
            # TODO: Show error message
            return

        try:
            # Create the agent using the agent service
            agent, agent_index = self.agent_service.create_agent(
                name=name,
                gateway_type=gateway_type,
                model=model,
                system_prompt=system_prompt
            )

            # Add the agent to the list widget
            self.add_agent_to_list(agent, agent_index)

            # Emit signals
            self.agent_created.emit(agent, agent_index)
            self.agent_selected.emit(agent)

            # Close the dialog if it was provided
            if dialog:
                dialog.accept()

        except Exception as e:
            # TODO: Show error message
            print(f"Error creating agent: {e}")
            return

    def select_agent(self, item: QListWidgetItem):
        """
        Handle selection of an agent from the list.

        Args:
            item: The selected list item
        """
        # Get the agent index from the item data
        agent_index = item.data(Qt.UserRole)

        # Get the agent from the agent service
        agent = self.agent_service.get_agent(agent_index)

        if agent:
            # Set as current agent in the agent service
            self.agent_service.set_current_agent(agent)

            # Emit the agent_selected signal
            self.agent_selected.emit(agent)

    def populate_agent_list(self):
        """
        Populate the agent list with existing agents.
        """
        # Clear the list first
        self.agent_list.clear()

        # Get all agents from the agent service
        agents = self.agent_service.get_all_agents()

        # Add each agent to the list
        for i, agent in enumerate(agents):
            self.add_agent_to_list(agent, i)

    def add_agent_to_list(self, agent: Agent, agent_index: int):
        """
        Add an agent to the list widget with its status displayed.

        Args:
            agent: The agent to add
            agent_index: The index of the agent in the agent service
        """
        # Create a list item
        item = QListWidgetItem()
        item.setData(Qt.UserRole, agent_index)  # Store the index of the agent in the list

        # Create a widget to hold the agent name and status
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

        # Add the agent name
        name_label = QLabel(agent.name)
        name_font = name_label.font()
        name_font.setPointSize(name_font.pointSize() + 1)
        name_label.setFont(name_font)
        layout.addWidget(name_label)

        # Add the agent status
        status_label = QLabel(agent.status.value)
        status_label.setStyleSheet("color: gray;")
        layout.addWidget(status_label)

        # Set the widget as the item's widget
        item.setSizeHint(widget.sizeHint())
        self.agent_list.addItem(item)
        self.agent_list.setItemWidget(item, widget)

    def update_agent_status(self, agent: Agent, agent_index: int):
        """
        Update the status display for an agent in the list.

        Args:
            agent: The agent to update
            agent_index: The index of the agent in the agent service
        """
        # Find the item for this agent
        for i in range(self.agent_list.count()):
            item = self.agent_list.item(i)
            if item.data(Qt.UserRole) == agent_index:
                # Get the widget
                widget = self.agent_list.itemWidget(item)
                if widget:
                    # Update the status label (second label in the layout)
                    status_label = widget.layout().itemAt(1).widget()
                    if status_label:
                        status_label.setText(agent.status.value)
                break

    def update_models(self, index: Optional[int] = None):
        """
        Update the model combo box based on the selected gateway.

        Args:
            index: The index of the selected gateway (not used, but required for signal connection)
        """
        self.model_combo.clear()

        # Add a "Choose..." entry as the first item
        self.model_combo.addItem("Choose...")

        # Get the current gateway
        gateway_text = self.gateway_combo.currentText()

        # If no gateway is selected or it's the "Choose..." entry, just show the "Choose..." entry
        if not gateway_text or gateway_text == "Choose...":
            return

        # Convert the gateway text to a GatewayType enum
        try:
            gateway_type = GatewayType(gateway_text)
        except ValueError:
            return

        try:
            # Get available models from the agent service
            models = self.agent_service.get_available_models(gateway_type)

            if models:
                self.model_combo.addItems(models)
        except Exception as e:
            print(f"Error getting available models: {e}")
