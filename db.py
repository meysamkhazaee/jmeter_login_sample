# db.py
import sqlite3
import os
import argparse

class Database:
    def __init__(self, db_file='user_database.db'):
        """Initialize the connection to the specified SQLite database file."""
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.create_table()  # Ensure the users table exists when initializing

    def create_table(self):
        """Create the users table if it does not exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_user(self, username, password):
        """Insert a new user into the database."""
        self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()

    def update_password(self, username, new_password):
        """Update a user's password."""
        self.cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
        self.conn.commit()

    def delete_user(self, username):
        """Delete a user from the database."""
        self.cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        self.conn.commit()

    def get_user(self, username):
        """Retrieve a user's information."""
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()

    def list_users(self):
        """List all users in the database."""
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()

class DatabaseCLI:
    def __init__(self, db_file="user_database.db"):
        """Initialize with an existing or new database file."""
        self.db_file = db_file
        self.connect_to_db(db_file)
        self.show_usage()

    def connect_to_db(self, db_file):
        """Connect to a specified database file."""
        # Close any existing connection first
        if hasattr(self, 'db') and self.db is not None:
            self.db.close_connection()
        
        # Load the database or create a new one if it doesn't exist
        if os.path.exists(db_file):
            print(f"Loading existing database '{db_file}'.")
        else:
            print(f"Database '{db_file}' not found. Creating a new database.")

        # Initialize Database connection with the specified file
        self.db = Database(db_file=db_file)
        self.db_file = db_file  # Update the db_file reference

    def show_usage(self):
        """Display the usage instructions."""
        print("\nCommands:")
        print("  insert <username> <password>     - Insert a new user")
        print("  update <username> <new_password> - Update a user's password")
        print("  delete <username>                - Delete a user")
        print("  get <username>                   - Get a user's info")
        print("  list                             - List all users")
        print("  load <new_db_file>               - Load a different .db file")
        print("  help                             - Show this usage message")
        print("  exit                             - Exit the application\n")

    def insert_user(self, username, password):
        """Insert a new user."""
        self.db.insert_user(username, password)
        print(f"User '{username}' inserted successfully.")

    def update_password(self, username, new_password):
        """Update an existing user's password."""
        self.db.update_password(username, new_password)
        print(f"Password for '{username}' updated successfully.")

    def delete_user(self, username):
        """Delete a user."""
        self.db.delete_user(username)
        print(f"User '{username}' deleted successfully.")

    def get_user_info(self, username):
        """Retrieve a user's information."""
        user = self.db.get_user(username)
        if user:
            print(f"User found: {user}")
        else:
            print(f"User '{username}' not found.")

    def list_users(self):
        """List all users in the database."""
        users = self.db.list_users()
        if users:
            print("List of all users:")
            for user in users:
                print(user)
        else:
            print("No users found.")

    def load_database(self, new_db_file):
        """Load a new .db file and reinitialize the connection."""
        print(f"Loading new database '{new_db_file}'...")
        self.connect_to_db(new_db_file)

    def run_cli(self):
        """Main CLI loop to interact with the user."""
        while True:
            try:
                user_input = input("db-cli> ").strip()
                if not user_input:
                    continue

                args = user_input.split()
                command = args[0].lower()

                if command == "insert" and len(args) == 3:
                    self.insert_user(args[1], args[2])
                elif command == "update" and len(args) == 3:
                    self.update_password(args[1], args[2])
                elif command == "delete" and len(args) == 2:
                    self.delete_user(args[1])
                elif command == "get" and len(args) == 2:
                    self.get_user_info(args[1])
                elif command == "list" and len(args) == 1:
                    self.list_users()
                elif command == "load" and len(args) == 2:
                    self.load_database(args[1])
                elif command == "help":
                    self.show_usage()
                elif command == "exit":
                    print("Exiting the application.")
                    break
                else:
                    print("Invalid command or arguments. Type 'help' for usage information.")
            except Exception as e:
                print(f"An error occurred: {e}")

        self.db.close_connection()  # Close the database connection

def main():
    parser = argparse.ArgumentParser(description="Database management script for user operations.")
    parser.add_argument("-d", "--database", help="Path to the SQLite .db file", default="user_database.db")
    args = parser.parse_args()

    # Initialize and run the DatabaseCLI with the specified database file
    cli = DatabaseCLI(db_file=args.database)
    cli.run_cli()

if __name__ == "__main__":
    main()
