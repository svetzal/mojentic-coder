"""
Engineering Goal service implementation for the Mojentic Coder application.

This module provides the implementation of the EngineeringGoalServiceInterface,
handling the creation and management of engineering goals and tasks.
"""
from typing import List, Optional, Tuple

from mojentic_coder.models.engineering_goal import EngineeringGoal, Task
from mojentic_coder.services.interfaces import EngineeringGoalServiceInterface


class EngineeringGoalService(EngineeringGoalServiceInterface):
    """
    Implementation of the EngineeringGoalServiceInterface.
    
    This service handles the creation, retrieval, and management of engineering goals and tasks.
    """
    
    def __init__(self):
        """Initialize the engineering goal service."""
        self.goals: List[EngineeringGoal] = []
        
    def create_goal(self, title: str, description: str = "") -> tuple[EngineeringGoal, int]:
        """
        Create a new engineering goal.
        
        Args:
            title: The title of the goal
            description: The description of the goal
            
        Returns:
            A tuple containing the created goal and its index
        """
        goal = EngineeringGoal(title=title, description=description)
        self.goals.append(goal)
        goal_index = len(self.goals) - 1
        return goal, goal_index
    
    def get_goal(self, index: int) -> Optional[EngineeringGoal]:
        """
        Get a goal by index.
        
        Args:
            index: The index of the goal to get
            
        Returns:
            The goal at the specified index, or None if the index is invalid
        """
        if 0 <= index < len(self.goals):
            return self.goals[index]
        return None
    
    def get_all_goals(self) -> List[EngineeringGoal]:
        """
        Get all goals.
        
        Returns:
            A list of all goals
        """
        return self.goals.copy()
    
    def add_task(self, goal_index: int, title: str, description: str = "") -> tuple[Task, int]:
        """
        Add a task to a goal.
        
        Args:
            goal_index: The index of the goal to add the task to
            title: The title of the task
            description: The description of the task
            
        Returns:
            A tuple containing the created task and its index within the goal
        """
        goal = self.get_goal(goal_index)
        if not goal:
            raise ValueError(f"Goal with index {goal_index} not found")
            
        task = Task(title=title, description=description)
        goal.tasks.append(task)
        task_index = len(goal.tasks) - 1
        return task, task_index
    
    def update_task_status(self, goal_index: int, task_index: int, completed: bool) -> bool:
        """
        Update the status of a task.
        
        Args:
            goal_index: The index of the goal containing the task
            task_index: The index of the task to update
            completed: The new completed status
            
        Returns:
            True if the task was updated, False otherwise
        """
        goal = self.get_goal(goal_index)
        if not goal:
            return False
            
        if 0 <= task_index < len(goal.tasks):
            goal.tasks[task_index].completed = completed
            return True
            
        return False