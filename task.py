from dataclasses import dataclass
from enum import Enum, auto

class Priority(Enum):
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()

@dataclass
class Task:
    """Class representing a single task in the organizer."""
    title: str
    completed: bool = False
    priority: Priority = Priority.NORMAL

    def to_dict(self) -> dict:
        """SERIALIZATION: changes object TASK to normal dictionary in Python"""
        return {
            "title": self.title,
            "completed": self.completed,
            "priority": self.priority.name
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """DESERIALIZATION: Creates new object Task on the base of dictionary."""
        return cls(
            title=data["title"],
            completed=data["completed"],
            priority=Priority[data["priority"]]
        )