from datetime import datetime
import os

class DuplicateVisitorError(Exception):
    pass

class EarlyEntryError(Exception):
    pass

FILENAME = "visitors.txt"

def ensure_file():
    """Create visitors file if it does not exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass  # empty file


def get_last_visitor():
    """Return (name, datetime object) of last visitor, or (None, None) if file empty."""
    if not os.path.exists(FILENAME):
        return None, None

    with open(FILENAME, "r") as f:
        lines = f.read().strip().split("\n")

    if not lines or lines == ['']:
        return None, None

    last_line = lines[-1]
    name, timestamp_str = last_line.split(" | ")

    last_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return name, last_time


def add_visitor(visitor_name):
    """Add visitor if rules allow:
       - No duplicate consecutive names
       - At least 5 minutes between different visitors
    """
    ensure_file()
    last_name, last_time = get_last_visitor()
    now = datetime.now()

    # Rule 1: Duplicate consecutive visitor
    if last_name == visitor_name:
        raise DuplicateVisitorError("Duplicate consecutive visitor not allowed.")

    # Rule 2: 5-minute waiting rule (only applies if file not empty)
    if last_time is not None:
        difference = (now - last_time).total_seconds() / 60  # minutes
        if difference < 5:
            raise EarlyEntryError("Must wait 5 minutes between different visitors.")

    # If allowed → append to file
    with open(FILENAME, "a") as f:
        f.write(f"{visitor_name} | {now.strftime('%Y-%m-%d %H:%M:%S')}\n")


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
