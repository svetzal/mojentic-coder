"""
Main entry point for the Mojentic Coder application.
"""
import sys
import os
import argparse
from typing import Optional

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFileDialog, QMenuBar, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Slot

from mojentic_coder.config import AppConfig
from mojentic_coder.panels.agent_management import AgentManagementPanel
from mojentic_coder.panels.chat_session import ChatSessionPanel
from mojentic_coder.panels.project_context import ProjectContextPanel
from mojentic_coder.models.agent import Agent
from mojentic_coder.services.service_provider import ServiceProvider


class MainWindow(QMainWindow):
    """Main window for the Mojentic Coder application."""

    def __init__(self, project_folder=None):
        super().__init__()

        self.setWindowTitle("Mojentic Coder")
        self.resize(1200, 800)

        # Initialize the application configuration
        self.app_config = AppConfig()

        # Set the project folder
        if project_folder:
            self.app_config.project_folder = project_folder
        else:
            self.app_config.project_folder = os.getcwd()

        # Create menu bar
        self.create_menu_bar()

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Create panels
        self.agent_management_panel = AgentManagementPanel(self.app_config)
        self.chat_session_panel = ChatSessionPanel(self.app_config)
        self.project_context_panel = ProjectContextPanel(self.app_config)

        # Connect signals
        self.agent_management_panel.agent_selected.connect(self.on_agent_selected)
        self.agent_management_panel.agent_created.connect(self.on_agent_created)
        self.chat_session_panel.agent_status_changed.connect(self.on_agent_status_changed)

        # Add panels to main layout
        main_layout.addWidget(self.agent_management_panel, 1)
        main_layout.addWidget(self.chat_session_panel, 2)
        main_layout.addWidget(self.project_context_panel, 1)

        self.setCentralWidget(main_widget)

    @Slot(Agent)
    def on_agent_selected(self, agent: Agent):
        """
        Handle agent selection from the agent management panel.

        Args:
            agent: The selected agent
        """
        # Update the chat session panel with the selected agent
        self.chat_session_panel.set_current_agent(agent)

    @Slot(Agent, int)
    def on_agent_created(self, agent: Agent, index: int):
        """
        Handle agent creation from the agent management panel.

        Args:
            agent: The created agent
            index: The index of the agent in the app_config
        """
        # The agent is now selected directly from the agent management panel
        # No need to add it to a dropdown in the chat session panel

    @Slot(Agent, int)
    def on_agent_status_changed(self, agent: Agent, index: int):
        """
        Handle agent status changes from the chat session panel.

        Args:
            agent: The agent whose status changed
            index: The index of the agent in the agent service
        """
        # Update the agent status in the agent management panel
        self.agent_management_panel.update_agent_status(agent, index)

    def create_menu_bar(self):
        """Create the application menu bar."""
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("&File")

        # Open folder action
        open_action = QAction("&Open Folder...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open a project folder")
        open_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_action)

    def open_folder(self):
        """Open a folder dialog and set the selected folder as the project folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder", self.app_config.project_folder)
        if folder:
            self.app_config.project_folder = folder
            # Update the project context panel
            self.project_context_panel.update_project_folder()


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Mojentic Coder")
    parser.add_argument("--project-folder", "-p", help="Path to the project folder")
    args, remaining = parser.parse_known_args()

    # Update sys.argv to remove our custom arguments
    sys.argv = [sys.argv[0]] + remaining

    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("Mojentic Coder")
    app.setApplicationDisplayName("Mojentic Coder")

    window = MainWindow(project_folder=args.project_folder)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
