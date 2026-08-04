import unittest
from shopping import ShoppingManager

class FakeShoppingStorage:
    def load(self) -> list:
        return []
    def save(self, data: list) -> None:
        pass

class TestShoppingManager(unittest.TestCase):

    def setUp(self) -> None:
        """Method starts automaticly before every test."""
        self.fake_storage = FakeShoppingStorage()
        self.manager = ShoppingManager(storage_backend= self.fake_storage)

    def test_add_item_increases_list_length(self) -> None:
        """Test 1: Add item to list -> List is 1 in length"""
        self.manager.shopping_list.append("mleko")

        length_of_list = len(self.manager.shopping_list)
        self.assertEqual(length_of_list, 1)

        self.assertTrue("mleko" in self.manager.shopping_list)

    def test_remove_item_leaves_list_empty(self) -> None:
        """Test 2: Remove item -> List is empty"""
        self.manager.shopping_list.append("Nakarmić kota")

        self.manager.shopping_list.remove("Nakarmić kota")

        self.assertEqual(len(self.manager.shopping_list), 0)

        self.assertFalse("Nakarmić kota" in self.manager.shopping_list)

if __name__ == "__main__":
    unittest.main()