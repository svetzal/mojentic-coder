"""
Engineering Goals and Tasks data models for the Mojentic Coder application.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    """
    Task model representing a specific task to be completed for an engineering goal.

    Attributes:
        title: Short title describing the task
        description: Detailed description of the task
        completed: Whether the task has been completed
    """
    title: str = Field(..., description="Short title describing the task")
    description: str = Field(default="", description="Detailed description of the task")
    completed: bool = Field(default=False, description="Whether the task has been completed")


class EngineeringGoal(BaseModel):
    """
    Engineering Goal model representing a technical objective of the system.

    Attributes:
        title: Short title describing the goal
        description: Detailed description of the goal
        tasks: List of tasks associated with this goal
    """
    title: str = Field(..., description="Short title describing the goal")
    description: str = Field(default="", description="Detailed description of the goal")
    tasks: List[Task] = Field(default_factory=list, description="List of tasks associated with this goal")