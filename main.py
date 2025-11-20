from datetime import datetime
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    try:
        with open(FILENAME, "r") as f:
            pass
    except FileNotFoundError:
        print(f"File '{FILENAME}' not found. Creating the file now.")
        with open(FILENAME, "w") as f:
            pass
    except PermissionError:
        print(f"Error: Permission denied to access '{FILENAME}'.")
        return
    except Exception as e:
        print(f"Unexpected error while checking file: {e}")
        return

def get_last_visitor():
    try:
        with open(FILENAME, "r") as f:
            lines = f.readlines()
            if lines:
                return lines[-1].strip()
            return None
    except Exception as e:
        print(f"Unexpected error while getting last visitor: {e}")
        return None

def add_visitor(visitor_name):
    try:
        last_visitor_name = get_last_visitor()

        # Check for duplicate
        if visitor_name == last_visitor_name:
            raise DuplicateVisitorError(visitor_name)

        # Add new entry
        entry = f"{visitor_name}\n"

        with open(FILENAME, "a") as f:
            f.write(entry)

        print(f"Successfully added '{visitor_name}' to the visitor log.")

    except DuplicateVisitorError as e:
        print(f"Error: {e}")
    except PermissionError:
        print(f"Error: Permission denied to write to '{FILENAME}'.")
    except IOError as e:
        print(f"Error: Unable to read/write file '{FILENAME}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
