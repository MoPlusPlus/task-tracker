import sys
import json
import os
from datetime import datetime

# File where tasks are stored
TASKS_FILE = "tasks.json"

def load_tasks():
    """
    Loads tasks from the tasks.json file.
    If the file does not exist, returns an empty list.
    """
    # Check if the JSON file exists before trying to open it
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        # Open the file in read mode
        with open(TASKS_FILE, 'r') as f:
            # Parse the JSON content into a Python list
            return json.load(f)
    except json.JSONDecodeError:
        # Handle cases where the file exists but contains invalid JSON
        print("Error: Could not decode tasks.json. File might be corrupted.")
        return []

def save_tasks(tasks):
    """
    Saves the list of tasks to the tasks.json file.
    Uses indentation for readability.
    """
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def get_next_id(tasks):
    """
    Generates the next unique ID for a task.
    Finds the maximum ID in the current tasks and increments it.
    """
    # If there are no tasks, the first ID should be 1
    if not tasks:
        return 1
    # Use max() to find the largest ID currently in use, then add 1
    return max(task['id'] for task in tasks) + 1

def add_task(description):
    """
    Adds a new task to the list with the given description.
    Initial status is set to 'todo'.
    """
    # 1. Load the existing tasks from the storage file
    tasks = load_tasks()
    
    # 2. Create the new task dictionary object
    new_task = {
        "id": get_next_id(tasks),          # Auto-increment ID
        "description": description,        # User description
        "status": "todo",                 # Default status
        "createdAt": datetime.now().isoformat(),  # Current timestamp
        "updatedAt": datetime.now().isoformat()   # Current timestamp
    }
    
    # 3. Add the new task to our list
    tasks.append(new_task)
    
    # 4. Save the updated list back to tasks.json
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

def update_task(task_id, description):
    """
    Updates the description of an existing task by its ID.
    Updates the 'updatedAt' timestamp.
    """
    tasks = load_tasks()
    # Iterate through the tasks to find the one with the matching ID
    for task in tasks:
        if task['id'] == task_id:
            # Update the description and the timestamp
            task['description'] = description
            task['updatedAt'] = datetime.now().isoformat()
            # Save all tasks back to the file
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    # If the loop finishes without returning, the ID wasn't found
    print(f"Error: Task with ID {task_id} not found.")

def delete_task(task_id):
    """
    Removes a task from the list by its ID.
    """
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    if len(tasks) < original_count:
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Error: Task with ID {task_id} not found.")

def update_status(task_id, status):
    """
    Updates the status of a task (e.g., 'in-progress' or 'done').
    Updates the 'updatedAt' timestamp.
    """
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Error: Task with ID {task_id} not found.")

def list_tasks(status_filter=None):
    """
    Lists tasks, optionally filtering by status.
    If no tasks exist or none match the filter, prints a friendly message.
    """
    tasks = load_tasks()
    if status_filter:
        tasks = [task for task in tasks if task['status'] == status_filter]
        title = f"Tasks ({status_filter})"
    else:
        title = "All Tasks"

    if not tasks:
        print("No tasks found.")
        return

    print(f"\n{title}:")
    print("-" * 40)
    for task in tasks:
        print(f"ID: {task['id']} | [{task['status']}] | {task['description']}")
    print("-" * 40)

def print_usage():
    """
    Prints the usage manual for the CLI application.
    """
    print("Usage: python task_cli.py [command] [arguments]")
    print("\nCommands:")
    print("  add [description]             Add a new task")
    print("  update [id] [description]      Update a task description")
    print("  delete [id]                    Delete a task")
    print("  mark-in-progress [id]          Mark task as in-progress")
    print("  mark-done [id]                 Mark task as done")
    print("  list                           List all tasks")
    print("  list [status]                  List tasks by status (todo, in-progress, done)")

def main():
    """
    Main entry point for the CLI. Handles parsing sys.argv and routing to functions.
    Includes basic error handling for missing arguments.
    """
    # Check if the user provided at least one command
    if len(sys.argv) < 2:
        print_usage()
        return

    # Extract the command (first argument after the script name)
    command = sys.argv[1].lower()

    try:
        # Route the command to the appropriate function
        if command == "add":
            if len(sys.argv) < 3:
                print("Error: Missing task description.")
            else:
                add_task(sys.argv[2])

        elif command == "update":
            if len(sys.argv) < 4:
                print("Error: Usage: update [id] [description]")
            else:
                # Convert the ID argument to an integer
                update_task(int(sys.argv[2]), sys.argv[3])

        elif command == "delete":
            if len(sys.argv) < 3:
                print("Error: Usage: delete [id]")
            else:
                # Convert the ID argument to an integer
                delete_task(int(sys.argv[2]))

        elif command == "mark-in-progress":
            if len(sys.argv) < 3:
                print("Error: Usage: mark-in-progress [id]")
            else:
                update_status(int(sys.argv[2]), "in-progress")

        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("Error: Usage: mark-done [id]")
            else:
                update_status(int(sys.argv[2]), "done")

        elif command == "list":
            status_filter = sys.argv[2].lower() if len(sys.argv) > 2 else None
            list_tasks(status_filter)

        else:
            print(f"Error: Unknown command '{command}'")
            print_usage()

    except ValueError:
        print("Error: Invalid ID. Please provide a numeric ID.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
