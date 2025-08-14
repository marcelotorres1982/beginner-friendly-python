# Shopping List
shopping_list = []

# Function to add items to the shopping list
def add_item():
    item = input("Enter item to add: ").strip()
    # Adds an item to the shopping list if it's not already present.
    if item not in shopping_list:
        shopping_list.append(item)
        return "Item added successfully."
    return "Item already exists in the shopping list."

# Function to remove item from the shopping list
def remove_item():
    item = input("Enter item to remove: ").strip()
    if item in shopping_list:
        shopping_list.remove(item)
        return "Item removed successfully."
    return "Item not found in the shopping list."

# Function to view the shopping list
def view_list():
    if not shopping_list:
        return "Shopping list is empty."
    return "Shopping list:\n" + "\n".join(f"- {item}" for item in shopping_list)

# Main loop
while True:
    print("\nOptions:")
    print("1. Add item")
    print("2. Remove item")
    print("3. View list")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ").strip()
    if choice == "1":
        print(add_item())
    elif choice == "2":
        print(remove_item())
    elif choice == "3":
        print(view_list())
    elif choice == "4":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
