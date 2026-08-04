from storage import JSONStorage
from enum import Enum, auto
import logging

logger = logging.getLogger("shopping_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler('shopping.log', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

class MenuOption(Enum):
    ADD_PRODUCT = auto()
    REMOVE_PRODUCT = auto()
    SHOW_MENU = auto()
    EXIT = auto()

class ShoppingManager:
    def __init__(self, storage_backend: JSONStorage) -> None:
        """Initialize the ShoppingManager and load tasks from storage."""
        self.storage = storage_backend

        self.shopping_list = self.storage.load()
        logger.info("Aplikacja została uruchomiona.")

    def save(self) -> None:
        """Method that takes care of saving logic in app"""
        self.storage.save(self.shopping_list)
        logger.info("Produkt zapisany.")

    def add_product(self) -> None:
        """Method adds tasks to list"""
        product = input("Podaj produkt do dodania: ")
        if product.strip():
            self.shopping_list.append(product)
            print("Produkt dodany! \n")
            logger.info(f"Produkt '{product}' dodany pomyślnie.")
        else:
            print("Nie można dodać pustego pola! \n")
            logger.warning("Próba dodania pustego zadania nieudana.")

    def remove_product(self) -> None:
        """Method remove tasks from list"""
        product = input("Podaj produkt do usunięcia: ")
        if product in self.shopping_list:
            self.shopping_list.remove(product)
            logger.info(f"Produkt '{product}' usunięty pomyślnie.")
        else:
            print("Podanego produktu nie ma na liście!\n")
            logger.warning("Próba usunięcia nieistniejącego produktu.")

    def show(self) -> None:
        """Method will display list of tasks in console"""
        if not self.shopping_list:
            print("Lista jest pusta!\n")
        else:
            for index, item in enumerate(self.shopping_list, start=1):
                print(f"{index}. {item}")
            print("---------------------------------\n")
            logger.info("Wyświetlenie pełnej listy zakupów.")
            

    def show_menu(self) -> None:
        """Method that displays menu of the app"""
        print("================Shopping List================")
        print("1.Dodaj produkt")
        print("2.Usuń produkt")
        print("3.Pokaż listę")
        print("4.Zakończ")

    def run(self) -> None:
        """Method that controls flow of the app"""
        while True:
            self.show_menu()
            choice = input("Podaj numer wybranej opcji ")

            try:
                chosen_option = MenuOption(int(choice))
            except ValueError:
                print("Błędny wybór! Wybierz ponownie!\n")
                logger.warning(f"Użytkownik wprowadził niepoprawną opcję menu: '{choice}'")
                continue

            match chosen_option:
                case MenuOption.ADD_PRODUCT:
                    self.add_product()
                    self.save()
                case MenuOption.REMOVE_PRODUCT:
                    self.remove_product()
                    self.save()
                case MenuOption.SHOW_MENU:
                    self.show()
                case MenuOption.EXIT:
                    print("Zamykanie programu.\n")
                    logger.info("Aplikacja została bezpiecznie zamknięta przez użytkownika.")
                    break

