import logging
from task import Task, Priority
from storage import JSONStorage

logger = logging.getLogger("repository_logger")

class TodoRepository:
    def __init__(self, storage_backend: JSONStorage) -> None:
        """Starting repository and automaticly loading data."""
        self.storage: JSONStorage = storage_backend
        self._tasks: list[Task] = self._load()

    def _load(self) -> list[Task]:
        """Private helping method to load data from storage."""
        raw_data = self.storage.load()
        loaded_tasks: list[Task] = []
        
        for item in raw_data:
            if isinstance(item, dict):
                loaded_tasks.append(Task.from_dict(item))
            elif isinstance(item, str):
                loaded_tasks.append(Task(title=item))
                
        return loaded_tasks

    def get_all(self) -> list[Task]:
        """Returns full list of objects Task."""
        return self._tasks

    def save_all(self) -> None:
        """Serialization current state of the list and orders universal save to storage."""
        raw_data = [task.to_dict() for task in self._tasks]
        self.storage.save(raw_data)
        logger.info("Repozytorium zapisało stan wszystkich zadań.")

    def add(self, task: Task) -> None:
        """Adds finished object Task to data collection."""
        self._tasks.append(task)
        logger.info(f"Repozytorium dodało zadanie do pamięci: {task.title}")

    def remove(self, task: Task) -> None:
        """Removes chosen object Task from data collection."""
        if task in self._tasks:
            self._tasks.remove(task)
            logger.info(f"Repozytorium usunęło zadanie z pamięci: {task.title}")
        else:
            logger.warning(f"Próba usunięcia nieistniejącego obiektu Task: {task.title}")