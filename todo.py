from storage import JSONStorage
from enum import Enum, auto
import logging
from task import Task, Priority

logger = logging.getLogger("todo_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler('todo.log', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

class MenuOption(Enum):
    ADD_TASK = auto()
    REMOVE_TASK = auto()
    SHOW_MENU = auto()
    COMPLETE_TASK = auto()
    EXIT = auto()

class TodoManager:
    def __init__(self, storage_backend: JSONStorage) -> None:
        """Initialize the TodoManager and load tasks from storage."""
        self.storage = storage_backend

        raw_json_data = self.storage.load()
        self.to_do_list: list[Task] = []

        for item in raw_json_data:
            if isinstance(item,dict):
                self.to_do_list.append(Task.from_dict(item))
            elif isinstance(item, str):
                self.to_do_list.append(Task(title=item))
                
        logger.info("Aplikacja została uruchomiona.")

    def save(self) -> None:
        """Method that takes care of saving logic in app"""
        raw_data = [task.to_dict() for task in self.to_do_list]
        self.storage.save(raw_data)
        logger.info("Zadanie zapisane.")

    def add_task(self) -> None:
        """Method adds tasks to list"""
        task_title = input("Podaj zadanie do wykonania: ")
        if not task_title.strip():
            print("Nie można dodać pustego zadania!\n")
            logger.warning("Próba dodania pustego zadania nieudana.")
            return

        print("Wybierz priorytet (1 - LOW, 2 - NORMAL, 3 - HIGH): ")
        p_choice = input("Wybór: ")

        match p_choice:
            case "1": priority = Priority.LOW
            case "3": priority = Priority.HIGH
            case _: priority = Priority.NORMAL

        new_task = Task(title=task_title, priority=priority)
        self.to_do_list.append(new_task)

        print("Zadanie dodane! \n")
        logger.info(f"Zadanie '{task_title}' dodane pomyślnie jako obiekt Task.")

            

    def remove_task(self) -> None:
        """Method remove tasks from list"""
        task_title = input("Podaj nazwę zadanie do usunięcia: ")

        task_to_remove = None
        for task in self.to_do_list:
            if task.title == task_title:
                task_to_remove = task
                break

        if task_to_remove:
            self.to_do_list.remove(task_to_remove)
            print("Zadanie usunięte! \n")
            logger.info(f"Zadanie '{task_title}' usunięte pomyślnie.")
        else: 
            print("Nie ma takiego zadania! \n")
            logger.warning("Próba usunięcia nieistniejącego zadania.")

    def complete_task(self) -> None:
        """Method to mark a specific task as completed."""
        if not self.to_do_list:
            print("Lista zadań jest pusta! Nie ma czego oznaczyć jako wykonane.\n")
            return

        self.show()

        try:
            choice = input("Podaj numer zadania, które wykonałeś: ")
            index = int(choice) - 1

            if 0 <= index < len(self.to_do_list):
                selected_task = self.to_do_list[index]
                selected_task.completed = True

                print(f"Zadanie '{selected_task.title}' zostało oznaczone jako wykonane! ✅\n")
                logger.info(f"Status zadania '{selected_task.title}' zmieniony na completed=True.")
            else:
                print("Nie ma zadania o takim numerze!\n")
                logger.warning(f"Próba oznaczenia zadania poza zakresem indeksu: {choice}")
                
        except ValueError:
            print("Musisz podać poprawną liczbę!\n")
            logger.warning(f"Niepoprawny format numeru zadania: '{choice}'")

    def show(self) -> None:
        """Method will display list of tasks in console"""
        if not self.to_do_list:
            print("Lista zadań jest pusta! \n")
        else:
            for index, task in enumerate(self.to_do_list, start=1):
                status = "✅" if task.completed else "❌"
                print(f"{index}. [{status}] {task.title} (Priorytet: {task.priority.name})")
            print("---------------------------------\n")
            logger.info("Wyświetlenie pełnej listy zadań.")

    def show_menu(self) -> None:
        """Method that displays menu of the app"""
        print("======LISTA ZADAŃ DO ZROBIENIA======")
        print("1. Dodaj zadanie")
        print("2. Usuń zadanie")
        print("3. Pokaż listę zadań")
        print("4. Wykonanie wybranego zadania")
        print("5. Zakończ")

    def run(self) -> None:
        """Method that controls flow of the app"""
        while True:
            self.show_menu()
            choice = input("Podaj numer opcji, którą wybierasz. ")
            
            try:
                chosen_option = MenuOption(int(choice))
            except ValueError:
                print("Błędny wybór! Wybierz ponownie!\n")
                logger.warning(f"Użytkownik wprowadził niepoprawną opcję menu: '{choice}'")
                continue

            match chosen_option:
                case MenuOption.ADD_TASK:
                    self.add_task()
                    self.save()
                case MenuOption.REMOVE_TASK:
                    self.remove_task()
                    self.save()
                case MenuOption.SHOW_MENU:
                    self.show()
                case MenuOption.COMPLETE_TASK:
                    self.complete_task()
                    self.save()
                case MenuOption.EXIT:
                    logger.info("Aplikacja została bezpiecznie zamknięta przez użytkownika.")
                    break                    
