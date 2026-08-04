import unittest
from task import Task, Priority

class FakeTodoStorage:
    def load(self) -> list:
        return []
    def save(self, data: list) -> None:
        pass

class TestTodoManager(unittest.TestCase):

    def test_task_creation(self) -> None:
        """Test 1: Testing creation of Task object and default data."""
        task = Task(title="Zdać projekt")
        
        self.assertEqual(task.title, "Zdać projekt")
        self.assertFalse(task.completed)  # Domyślnie powinno być False
        self.assertEqual(task.priority, Priority.NORMAL)  # Domyślnie NORMAL

    def test_marking_task_as_completed(self) -> None:
        """Test 2: Marking task as completed."""
        task = Task(title="Umyć auto")
        
        task.completed = True
        
        self.assertTrue(task.completed)

    def test_task_serialization_and_deserialization(self) -> None:
        """Test 3: Testing cycle: Task -> save -> load -> Task."""
        original_task = Task(title="Kupić kawę", completed=False, priority=Priority.HIGH)

        serialized_data = original_task.to_dict()

        restored_task = Task.from_dict(serialized_data)

        self.assertEqual(restored_task.title, original_task.title)
        self.assertEqual(restored_task.completed, original_task.completed)
        self.assertEqual(restored_task.priority, original_task.priority)


if __name__ == "__main__":
    unittest.main()