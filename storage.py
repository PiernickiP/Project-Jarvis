import json
import logging

logger = logging.getLogger("storage_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler('storage.log', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

class JSONStorage:
    def __init__(self, file_name: str) -> None:
        """Initialize storage for a given JSON file."""
        self.file_path: str = f"data/{file_name}"

    def save(self, data: list[str]) -> None:
        """Universal method to save data. Doesn't need file_name as argument."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logger.info(f"Pomyślnie zapisano dane do pliku {self.file_path}")
        except Exception as e:
            print(f"Wystąpił błąd podczas zapisu: {e}")
            logger.error(f"Błąd zapisu do pliku {self.file_path}: {e}")


    def load(self) -> list:
        """Universal method to load data. Returns list of data"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                new_list = json.load(file)
                logger.info(f"Pomyślnie wczytano dane z pliku {self.file_path}")
                return new_list
        except FileNotFoundError:
            print("Nie ma takiego pliku!")
            logger.warning(f"Plik {self.file_path} nie istnieje podczas próby odczytu.")
            return []
        except json.JSONDecodeError:
            print(f"Plik {self.file_path} jest uszkodzony lub pusty. Resetuję listę.")
            logger.error(f"Plik {self.file_path} zawiera uszkodzony JSON.")
            return []
