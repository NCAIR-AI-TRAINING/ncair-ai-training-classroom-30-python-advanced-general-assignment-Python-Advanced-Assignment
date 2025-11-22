from datetime import datetime, timedelta
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    if not os.path.exists(FILENAME):       #ensures 'vivitors.txt' exists
        with open(FILENAME, "w") as f:
            pass   #just create an empty file

def get_last_visitor():
    """Return last visitor name and timestamp, or (None, None) if empty."""
    if not os.path.exists(FILENAME):
        return None, None  # file doesn’t exist yet

    with open(FILENAME, "r") as f:
        lines = f.readlines()
        if not lines:
            return None, None  # file is empty
        last_line = lines[-1].strip()
        # Expected format: "name|YYYY-MM-DD HH:MM:SS"
        try:
            name, timestamp_str = last_line.split("|")
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return name, timestamp
        except ValueError:
            # fallback if timestamp missing (older main branch entries)
            return last_line, None

def add_visitor(name):     #checks if last visitor is same as current one and raise customer error if duplicate
    visitors = []

    #Read previous visitors
    try:
        with open("visitors.txt") as f:
            for line in f:
                if " | " in line:
                    visitor_name, timestamp = line.strip().split(" | ")
                    visitors.append((visitor_name, timestamp))
    except FileNotFoundError:
        pass

    #Check for duplicate visitor
    for visitor_name, timestamp in visitors:
        if visitor_name == name:
            raise DuplicateVisitorError()

    #Check the wait time (needs at least 5 minutes)
    if visitors:
        last_name, last_timestamp = visitors[-1]
        last_time = datetime.fromisoformat(last_timestamp)
        if datetime.now() - last_time < timedelta(minutes=5):
            raise Exception("Must wait 5 minutes before next visitor.")

    #Add new visitor with ISO timestamp
    timestamp = datetime.now().isoformat()
    with open("visitors.txt", "a") as f:
        f.write(f"{name} | {timestamp}\n")

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
