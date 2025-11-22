from datetime import datetime, timedelta


class DuplicateVisitorError(Exception):
    def __init__(self, visitor_name):
        self.visitor_name = visitor_name
        super().__init__(f"Visitor '{visitor_name}' has already visited.")


class EarlyEntryError(Exception):
    def __init__(self):
        super().__init__("A 5-minute wait is required between different visitors.")


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
                return lines[-1].strip().split(" | ")[0]
            return None
    except Exception as e:
        print(f"Unexpected error while getting last visitor: {e}")
        return None


def get_last_visitor_timestamp():
    try:
        with open(FILENAME, "r") as f:
            lines = f.readlines()
            if lines:
                parts = lines[-1].strip().split(" | ")
                if len(parts) >= 2:
                    return parts[1]
            return None
    except Exception as e:
        print(f"Unexpected error while getting last visitor timestamp: {e}")
        return None


def add_visitor(visitor_name):
    try:
        last_visitor_name = get_last_visitor()
        last_visitor_timestamp = get_last_visitor_timestamp()

        # Check for duplicate
        if visitor_name == last_visitor_name:
            raise DuplicateVisitorError(visitor_name)

        # Check for 5-minute wait rule
        if last_visitor_timestamp:
            try:
                last_time = datetime.fromisoformat(last_visitor_timestamp)
                current_time = datetime.now()
                time_diff = current_time - last_time
                if time_diff < timedelta(minutes=5):
                    raise EarlyEntryError()
            except ValueError:
                pass

        # Add new entry with timestamp
        timestamp = datetime.now().isoformat()
        entry = f"{visitor_name} | {timestamp}\n"

        with open(FILENAME, "a") as f:
            f.write(entry)

        print(f"Successfully added '{visitor_name}' to the visitor log.")

    except DuplicateVisitorError as e:
        print(f"Error: {e}")
        raise
    except EarlyEntryError as e:
        print(f"Error: {e}")
        raise
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
