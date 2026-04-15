import subprocess
import os
import json
import unittest

# Name of the test script and the temporary storage file
CLI_SCRIPT = "task_cli.py"
TEST_JSON = "test_tasks.json"

class TestTaskCLI(unittest.TestCase):
    """
    Test suite for the Task Tracker CLI.
    Uses a temporary JSON file to avoid affecting real data.
    """

    def setUp(self):
        """
        Run before each test: remove the test JSON if it exists.
        We also need to tell the CLI to use this test file.
        Since the CLI has TASKS_FILE hardcoded, we will temporarily 
        modify it or just use a backup/restore strategy.
        Better yet, we can monkeypatch the file if we import it, 
        but since we are testing it as a CLI, we'll use a trick:
        Environment variables or just modifying the file temporarily.
        For simplicity, we'll backup tasks.json, run tests, and restore.
        """
        self.backup_exists = os.path.exists("tasks.json")
        if self.backup_exists:
            os.rename("tasks.json", "tasks.json.backup")
        
        # Ensure we start with a fresh state
        if os.path.exists("tasks.json"):
            os.remove("tasks.json")

    def tearDown(self):
        """
        Run after each test: restore the original tasks.json.
        """
        if os.path.exists("tasks.json"):
            os.remove("tasks.json")
        
        if self.backup_exists:
            os.rename("tasks.json.backup", "tasks.json")

    def run_cli(self, *args):
        """
        Helper to run the CLI script with arguments.
        Returns the stdout and stderr.
        """
        result = subprocess.run(
            ["python", CLI_SCRIPT] + list(args),
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr

    def test_add_task(self):
        """Test adding a task."""
        stdout, _ = self.run_cli("add", "Test Task")
        self.assertIn("Task added successfully", stdout)
        
        # Verify file creation and content
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["description"], "Test Task")

    def test_list_tasks(self):
        """Test listing tasks."""
        self.run_cli("add", "Task 1")
        self.run_cli("add", "Task 2")
        stdout, _ = self.run_cli("list")
        self.assertIn("Task 1", stdout)
        self.assertIn("Task 2", stdout)

    def test_update_task(self):
        """Test updating a task description."""
        self.run_cli("add", "Old Description")
        self.run_cli("update", "1", "New Description")
        
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            self.assertEqual(tasks[0]["description"], "New Description")

    def test_delete_task(self):
        """Test deleting a task."""
        self.run_cli("add", "To be deleted")
        self.run_cli("delete", "1")
        
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            self.assertEqual(len(tasks), 0)

    def test_mark_status(self):
        """Test marking tasks as in-progress and done."""
        self.run_cli("add", "Progress Task")
        
        # Mark in-progress
        self.run_cli("mark-in-progress", "1")
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            self.assertEqual(tasks[0]["status"], "in-progress")
            
        # Mark done
        self.run_cli("mark-done", "1")
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
            self.assertEqual(tasks[0]["status"], "done")

    def test_filter_list(self):
        """Test listing tasks filtered by status."""
        self.run_cli("add", "Todo Task")
        self.run_cli("add", "Doing Task")
        self.run_cli("mark-in-progress", "2")
        
        # Filter by todo
        stdout, _ = self.run_cli("list", "todo")
        self.assertIn("Todo Task", stdout)
        self.assertNotIn("Doing Task", stdout)
        
        # Filter by in-progress
        stdout, _ = self.run_cli("list", "in-progress")
        self.assertIn("Doing Task", stdout)
        self.assertNotIn("Todo Task", stdout)

if __name__ == "__main__":
    unittest.main()
