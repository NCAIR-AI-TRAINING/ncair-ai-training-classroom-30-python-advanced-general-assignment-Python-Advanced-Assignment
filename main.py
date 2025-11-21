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

def add_visitor(visitor_name):     #checks if last visitor is same as current one and raise customer error if duplicate
    last_name, last_time = get_last_visitor()

    # Check duplicate consecutive visitor FIRST
    if last_name == visitor_name:
        raise DuplicateVisitorError(f"{visitor_name} tried to visit twice in a row!")

    # Check 5-minute wait rule SECOND
    if last_time:
        now = datetime.now()
        elapsed = now - last_time
        if elapsed < timedelta(minutes=5):
            remaining = timedelta(minutes=5) - elapsed
            raise EarlyEntryError(f"{visitor_name} must wait {int(remaining.total_seconds())} more seconds before visiting again.")

    # Log visitor
    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    pass

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
