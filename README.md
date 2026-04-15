# Task Tracker CLI

A lightweight, terminal-based task management application built with native Python. This tool allows users to manage their tasks efficiently using a simple command-line interface.

## Features

- **Add Tasks**: Create new tasks with a description.
- **Update Tasks**: Modify existing task descriptions or statuses.
- **Delete Tasks**: Remove tasks from your list.
- **Mark Status**: Transition tasks between `todo`, `in-progress`, and `done`.
- **List Tasks**: Filter and view tasks by their current status.
- **Persistence**: Tasks are automatically saved to a `tasks.json` file.
- **No Dependencies**: Built entirely with Python's standard library.

## Installation

No external dependencies are required. Just ensure you have Python 3.x installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/MoPlusPlus/task-tracker.git
   cd task-tracker
   ```

2. (Optional) Run tests to ensure everything is working correctly:
   ```bash
   python test_task_cli.py
   ```

## Usage

Run the `task_cli.py` script with the following commands:

### Adding a new task
```bash
python task_cli.py add "Buy groceries"
# Output: Task added successfully (ID: 1)
```

### Updating a task
```bash
python task_cli.py update 1 "Buy groceries and cook dinner"
```

### Deleting a task
```bash
python task_cli.py delete 1
```

### Marking a task as in progress or done
```bash
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 1
```

### Listing all tasks
```bash
python task_cli.py list
```

### Listing tasks by status
```bash
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
