import shopping
import todo
from storage import JSONStorage

def show_menu():
    print("=======================================\n")
    print("Personal Organizer\n")
    print("=======================================\n\n")
    print("1.TODO\n")
    print("2. Shopping List\n")
    print("3. Exit\n")

def main():
    todo_storage = JSONStorage("todo.json")
    shopping_storage = JSONStorage("shopping.json")

    todo_manager = todo.TodoManager(storage_backend= todo_storage)
    shopping_manager = shopping.ShoppingManager(storage_backend= shopping_storage)
    
    while True:
        show_menu()

        choice = input("Wprowadź opcję, którą chcesz uruchomić! ")

        match choice:
            case "1":
                todo_manager.run()
            case "2":
                shopping_manager.run()
            case "3":
                print("Zamykanie programu! \n")
                break


if __name__ == "__main__":
    main()