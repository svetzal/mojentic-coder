"""
Project Context panel for the Mojentic Coder application.
"""
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame

from mojentic_coder.config import AppConfig
from mojentic_coder.panels.engineering_goals_panel import EngineeringGoalsPanel


class ProjectContextPanel(QWidget):
    """
    Panel for displaying project context information.

    This panel is currently a placeholder for future functionality.
    """

    def __init__(self, app_config: AppConfig):
        """
        Initialize the project context panel.

        Args:
            app_config: The application configuration
        """
        super().__init__()

        self.app_config = app_config

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Project Context</b>"))

        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Add project folder section
        layout.addWidget(QLabel("Project Folder:"))
        self.folder_label = QLabel()
        self.folder_label.setWordWrap(True)
        layout.addWidget(self.folder_label)

        # Update the project folder display
        self.update_project_folder()

        # Add a separator line for engineering goals section
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator2)

        # Add engineering goals section label
        layout.addWidget(QLabel("<b>Engineering Goals</b>"))

        # Create and add the engineering goals panel directly to the layout
        self.engineering_goals_panel = EngineeringGoalsPanel(app_config)
        layout.addWidget(self.engineering_goals_panel)

        # Add stretch to push widgets to the top
        layout.addStretch()

    def update_project_folder(self):
        """Update the displayed project folder."""
        if self.app_config.project_folder:
            self.folder_label.setText(self.app_config.project_folder)
        else:
            self.folder_label.setText("No project folder selected")
