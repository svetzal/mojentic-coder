"""
Engineering Goals panel for the Mojentic Coder application.

This panel displays and manages engineering goals and tasks.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTextEdit, QTreeWidget, QTreeWidgetItem, 
    QCheckBox, QDialog, QFormLayout, QDialogButtonBox
)
from PySide6.QtCore import Qt, Signal

from mojentic_coder.config import AppConfig
from mojentic_coder.models.engineering_goal import EngineeringGoal, Task
from mojentic_coder.services.service_provider import ServiceProvider


class AddGoalDialog(QDialog):
    """Dialog for adding a new engineering goal."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Engineering Goal")
        self.setMinimumWidth(400)

        # Create form layout
        layout = QFormLayout(self)

        # Add title field
        self.title_edit = QLineEdit()
        layout.addRow("Title:", self.title_edit)

        # Add description field
        self.description_edit = QTextEdit()
        self.description_edit.setMinimumHeight(100)
        layout.addRow("Description:", self.description_edit)

        # Add buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def get_goal_data(self):
        """Get the goal data from the dialog."""
        return {
            "title": self.title_edit.text(),
            "description": self.description_edit.toPlainText()
        }


class AddTaskDialog(QDialog):
    """Dialog for adding a new task to a goal."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Task")
        self.setMinimumWidth(400)

        # Create form layout
        layout = QFormLayout(self)

        # Add title field
        self.title_edit = QLineEdit()
        layout.addRow("Title:", self.title_edit)

        # Add description field
        self.description_edit = QTextEdit()
        self.description_edit.setMinimumHeight(100)
        layout.addRow("Description:", self.description_edit)

        # Add buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def get_task_data(self):
        """Get the task data from the dialog."""
        return {
            "title": self.title_edit.text(),
            "description": self.description_edit.toPlainText()
        }


class EngineeringGoalsPanel(QWidget):
    """
    Panel for displaying and managing engineering goals and tasks.
    """

    def __init__(self, app_config: AppConfig):
        """
        Initialize the engineering goals panel.

        Args:
            app_config: The application configuration
        """
        super().__init__()

        self.app_config = app_config
        self.goal_service = ServiceProvider.get_engineering_goal_service()
        self.goal_items = {}  # Dictionary to map goal indices to tree items

        # Set up the layout
        layout = QVBoxLayout(self)

        # Create tree widget for goals and tasks
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Engineering Goals and Tasks"])
        self.tree_widget.setExpandsOnDoubleClick(True)
        self.tree_widget.setIndentation(20)
        self.tree_widget.setColumnCount(1)
        layout.addWidget(self.tree_widget)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Add goal button
        self.add_goal_button = QPushButton("Add Goal")
        self.add_goal_button.clicked.connect(self.on_add_goal_clicked)
        buttons_layout.addWidget(self.add_goal_button)

        # Add task button
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.on_add_task_clicked)
        self.add_task_button.setEnabled(False)  # Disabled until a goal is selected
        buttons_layout.addWidget(self.add_task_button)

        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)

        # Connect tree item selection signal
        self.tree_widget.itemSelectionChanged.connect(self.on_tree_selection_changed)

        # Update the tree with goals and tasks
        self.update_tree()

    def update_tree(self):
        """Update the tree with goals and tasks."""
        # Save the currently selected item's data before clearing the tree
        selected_items = self.tree_widget.selectedItems()
        selected_data = None
        if selected_items:
            selected_item = selected_items[0]
            try:
                selected_data = selected_item.data(0, Qt.UserRole)
            except RuntimeError:
                # Handle case where item might have been deleted
                selected_data = None

        # Save the expanded state of goals
        expanded_goals = []
        for i, goal_item in self.goal_items.items():
            if goal_item.isExpanded():
                expanded_goals.append(i)

        # Clear the tree and the goal items dictionary
        self.tree_widget.clear()
        self.goal_items = {}

        # Add goals and their tasks to the tree
        for i, goal in enumerate(self.goal_service.get_all_goals()):
            # Create goal item
            goal_item = QTreeWidgetItem(self.tree_widget)
            goal_item.setText(0, goal.title)
            goal_item.setToolTip(0, goal.description)
            goal_item.setData(0, Qt.UserRole, {"type": "goal", "index": i})
            goal_item.setFlags(goal_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            # Store the goal item in the dictionary
            self.goal_items[i] = goal_item

            # Add tasks as child items
            for j, task in enumerate(goal.tasks):
                task_item = QTreeWidgetItem(goal_item)

                # Create a widget for the task item to include a checkbox
                task_widget = QWidget()
                task_layout = QHBoxLayout(task_widget)
                task_layout.setContentsMargins(4, 4, 4, 4)

                # Add checkbox
                checkbox = QCheckBox()
                checkbox.setChecked(task.completed)
                checkbox.stateChanged.connect(lambda state, g_idx=i, t_idx=j: self.on_task_state_changed(g_idx, t_idx, state))
                task_layout.addWidget(checkbox)

                # Add task title
                task_label = QLabel(task.title)
                if task.completed:
                    task_label.setStyleSheet("text-decoration: line-through;")
                task_layout.addWidget(task_label, 1)

                # Set the task text and data
                task_item.setText(0, "")  # Text will be shown in the widget
                task_item.setData(0, Qt.UserRole, {"type": "task", "goal_index": i, "task_index": j})

                # Set the widget as the item widget
                self.tree_widget.setItemWidget(task_item, 0, task_widget)

        # Restore expanded state
        for goal_index in expanded_goals:
            if goal_index in self.goal_items:
                self.goal_items[goal_index].setExpanded(True)

        # Restore selection if possible
        if selected_data:
            if selected_data["type"] == "goal" and selected_data["index"] in self.goal_items:
                # If a goal was selected, restore that selection
                self.tree_widget.setCurrentItem(self.goal_items[selected_data["index"]])
            elif selected_data["type"] == "task" and selected_data["goal_index"] in self.goal_items:
                # If a task was selected, select its parent goal instead
                # This allows adding multiple tasks to the same goal without reselecting
                self.tree_widget.setCurrentItem(self.goal_items[selected_data["goal_index"]])

    def on_tree_selection_changed(self):
        """Handle tree item selection changes."""
        selected_items = self.tree_widget.selectedItems()

        if selected_items:
            item = selected_items[0]
            try:
                data = item.data(0, Qt.UserRole)

                if data:
                    if data["type"] == "goal":
                        # A goal is selected, enable the add task button
                        self.add_task_button.setEnabled(True)
                    else:
                        # A task is selected, get its parent goal
                        parent_item = item.parent()
                        if parent_item:
                            try:
                                parent_data = parent_item.data(0, Qt.UserRole)
                                if parent_data and parent_data["type"] == "goal":
                                    # Enable the add task button for the parent goal
                                    self.add_task_button.setEnabled(True)
                            except RuntimeError:
                                # Handle case where parent item might have been deleted
                                self.add_task_button.setEnabled(False)
            except RuntimeError:
                # Handle case where item might have been deleted
                self.add_task_button.setEnabled(False)
        else:
            # No selection, disable the add task button
            self.add_task_button.setEnabled(False)

    def on_add_goal_clicked(self):
        """Handle add goal button click."""
        dialog = AddGoalDialog(self)
        if dialog.exec():
            goal_data = dialog.get_goal_data()
            goal, goal_index = self.goal_service.create_goal(
                title=goal_data["title"],
                description=goal_data["description"]
            )
            self.update_tree()

            # Select the newly added goal and expand it
            if goal_index in self.goal_items:
                self.tree_widget.setCurrentItem(self.goal_items[goal_index])
                self.goal_items[goal_index].setExpanded(True)

    def on_add_task_clicked(self):
        """Handle add task button click."""
        selected_items = self.tree_widget.selectedItems()
        if not selected_items:
            return

        # Get the goal index from the selected item
        item = selected_items[0]
        goal_index = None

        try:
            data = item.data(0, Qt.UserRole)
            if data and data["type"] == "goal":
                goal_index = data["index"]
            elif data and data["type"] == "task":
                # If a task is selected, get its parent goal
                goal_index = data["goal_index"]
        except RuntimeError:
            # Handle case where item might have been deleted
            return

        if goal_index is not None:
            dialog = AddTaskDialog(self)
            if dialog.exec():
                task_data = dialog.get_task_data()
                task, task_index = self.goal_service.add_task(
                    goal_index=goal_index,
                    title=task_data["title"],
                    description=task_data["description"]
                )

                # Store the goal index to use after update_tree()
                # instead of accessing potentially deleted items
                stored_goal_index = goal_index

                # Update the tree without trying to access the old items
                self.update_tree()

                # After update_tree(), ensure the goal is expanded
                if stored_goal_index in self.goal_items:
                    self.goal_items[stored_goal_index].setExpanded(True)

    def on_task_state_changed(self, goal_index, task_index, state):
        """
        Handle task state change.

        Args:
            goal_index: The index of the goal
            task_index: The index of the task
            state: The new state of the checkbox
        """
        self.goal_service.update_task_status(
            goal_index=goal_index,
            task_index=task_index,
            completed=(state == Qt.Checked)
        )
        self.update_tree()
