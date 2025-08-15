# This code implements a simple contact management system that allows users to add, view, and delete contacts.

import json
import os

# File where contacts will be stored
CONTACTS_FILE = "contacts.json"


def load_contacts():
    """
    Load contacts from the JSON file.
    If the file does not exist, return an empty list.
    """
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_contacts(contacts):
    """
    Save the list of contacts to the JSON file.
    """
    with open(CONTACTS_FILE, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)


def add_contact():
    """
    Add a new contact with name, phone, and email.
    """
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    email = input("Enter email: ").strip()

    contacts = load_contacts()

    # Check if contact already exists by name
    for contact in contacts:
        if contact["name"].lower() == name.lower():
            print("Contact already exists.")
            return

    # Add the new contact
    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts(contacts)
    print("Contact added successfully.")


def view_contacts():
    """
    Display all saved contacts.
    """
    contacts = load_contacts()
    if not contacts:
        print("No contacts found.")
        return

    for idx, contact in enumerate(contacts, start=1):
        print(f"{idx}. {contact['name']} - {contact['phone']} - {contact['email']}")


def delete_contact():
    """
    Delete a contact by name.
    """
    name = input("Enter the name of the contact to delete: ").strip()
    contacts = load_contacts()

    updated_contacts = [c for c in contacts if c["name"].lower() != name.lower()]

    if len(updated_contacts) == len(contacts):
        print("Contact not found.")
        return

    save_contacts(updated_contacts)
    print("Contact deleted successfully.")


def main():
    """
    Main menu for the Contact Agenda.
    """
    while True:
        print("\n=== Contact Agenda ===")
        print("1. Add contact")
        print("2. View contacts")
        print("3. Delete contact")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()

