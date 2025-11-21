from datetime import datetime
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass
    pass

def get_last_visitor():
    with open(FILENAME, "r") as f:
        lines = f.readlines()

    if not lines:
        return None, None

    last_line = lines[-1].strip()
    parts = last_line.split(" | ")

    last_name = parts[0]
    last_time = datetime.fromisoformat(parts[1])

    return last_name, last_time
    pass

def add_visitor(visitor_name):
    last_name, last_time = get_last_visitor()

    if last_name == visitor_name:
        raise DuplicateVisitorError(f"Duplicate visitor: {visitor_name}")

    now = datetime.now()
    timestamp = now.isoformat(" ")

    if last_time is not None:
        time_difference = (now - last_time).total_seconds()
        if time_difference < 300:
            raise EarlyEntryError("You must wait 5 minutes before next visitor.")

    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} | {timestamp}\n")

    pass

def main():
    ensure_file()
    name = input("Enter visitor's name: ")
    try:
        add_visitor(name)
        print("Visitor added successfully!")
    except Exception as e:
        print("Error:", e)
        
if __name__ == "main":
    main()