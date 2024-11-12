import argparse
from db import Database
import sys

def show_usage():
    print("\nCommands:")
    print("  insert <username> <password>   - Insert a new user")
    print("  update <username> <new_password> - Update a user's password")
    print("  delete <username>               - Delete a user")
    print("  get <username>                  - Get a user's info")
    print("  list                            - List all users")
    print("  help                            - Show this usage message")
    print("  exit                            - Exit the application\n")

def insert_user(db, username, password):
    db.insert_user(username, password)
    print(f"User '{username}' inserted successfully.")

def update_password(db, username, new_password):
    db.update_password(username, new_password)
    print(f"Password for '{username}' updated successfully.")

def delete_user(db, username):
    db.delete_user(username)
    print(f"User '{username}' deleted successfully.")

def get_user_info(db, username):
    user = db.get_user(username)
    if user:
        print(f"User found: {user}")
    else:
        print(f"User '{username}' not found.")

def list_users(db):
    users = db.list_users()
    if users:
        print("List of all users:")
        for user in users:
            print(user)
    else:
        print("No users found.")

def main():
    db = Database()
    show_usage()

    while True:
        try:
            user_input = input("db-cli> ").strip()
            if not user_input:
                continue

            args = user_input.split()
            command = args[0].lower()

            if command == "insert" and len(args) == 3:
                insert_user(db, args[1], args[2])
            elif command == "update" and len(args) == 3:
                update_password(db, args[1], args[2])
            elif command == "delete" and len(args) == 2:
                delete_user(db, args[1])
            elif command == "get" and len(args) == 2:
                get_user_info(db, args[1])
            elif command == "list" and len(args) == 1:
                list_users(db)
            elif command == "help":
                show_usage()
            elif command == "exit":
                print("Exiting the application.")
                break
            else:
                print("Invalid command or arguments. Type 'help' for usage information.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
    
    db.close_connection()  # Close the database connection

if __name__ == "__main__":
    main()
