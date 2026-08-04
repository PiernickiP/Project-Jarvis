import unittest
import os
import json
from storage import JSONStorage

class TestJSONStorage(unittest.TestCase):

    def setUp(self) -> None:
        """Prepare environment before every test."""
        self.test_filename = "test_data.json"
        self.storage = JSONStorage(self.test_filename)
        
        self.expected_path = f"data/{self.test_filename}"
        
        os.makedirs("data", exist_ok=True)

    def tearDown(self) -> None:
        """Cleaning after every test – removing test file if it was created"""
        if os.path.exists(self.expected_path):
            os.remove(self.expected_path)

    def test_save_and_load_success(self) -> None:
        """Test 1: Saving and loading correct data"""
        test_data = ["Kupić chleb", "Umyć auto"]

        self.storage.save(test_data)
        loaded_data = self.storage.load()

        self.assertEqual(loaded_data, test_data)
        self.assertEqual(len(loaded_data), 2)

    def test_load_file_not_found(self) -> None:
        """Test 2: File not found -> returns empty list."""
        if os.path.exists(self.expected_path):
            os.remove(self.expected_path)

        loaded_data = self.storage.load()

        self.assertEqual(loaded_data, [])

    def test_load_invalid_json(self) -> None:
        """Test 3: File is damaged/corrupted -> returns empty list"""
        with open(self.expected_path, "w", encoding="utf-8") as file:
            file.write("To nie jest poprawny format JSON { ... ")

        loaded_data = self.storage.load()

        self.assertEqual(loaded_data, [])

if __name__ == "__main__":
    unittest.main()