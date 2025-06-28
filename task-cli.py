import sys
import json
import os
from datetime import datetime

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def get_current_time():
    return datetime.now().isoformat()

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1


def add_task(description):
    tasks = load_tasks()
    task = {
        "id": get_next_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": get_current_time(),
        "updatedAt": get_current_time()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task['id']})")

def list_tasks(status_filter=None):
    tasks = load_tasks()

    if status_filter:
        tasks = [t for t in tasks if t["status"] == status_filter]

    if not tasks:
        print("No tasks found.")
        return
    
    for task in tasks:
        print(f"[{task['id']}] {task['description']} - {task['status']}")

def update_task(task_id, new_description):
    tasks = load_tasks()

    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = get_current_time()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
        
    print(f"No task found with ID: {task_id}")

def delete_task(task_id):
    tasks = load_tasks()

    new_tasks = [task for task in tasks if task['id'] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"No task found with ID: {task_id}")
        return
    
    save_tasks(new_tasks)
    print(f"Task {task_id} deleted successfully.")

def mark_status(task_id, new_status):
    tasks = load_tasks()

    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            task['updatedAt'] = get_current_time()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {new_status}")
            return
        
    print(f"No task found with ID: {task_id}")




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a command.")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a description for the task.")
            sys.exit(1)
        description = sys.argv[2]
        add_task(description)

    elif command == "list":
        if len(sys.argv) == 3:
            status_filter = sys.argv[2]
            if status_filter not in ["todo", "done", "in-progress"]:
                print("Invalid status filter. Use 'todo', 'done', or 'in-progress'.")
                sys.exit(1)
            list_tasks(status_filter)
        else:
            list_tasks()
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: python task-cli.py update <id> <new description>")
            sys.exit(1)

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be a number.")
            sys.exit(1)

        new_description = " ".join(sys.argv[3:])
        update_task(task_id, new_description)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python task-cli.py delete <id>")
            sys.exit(1)

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be a number.")
            sys.exit(1)

        delete_task(task_id)

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Usage: python task-cli.py mark-in-progress <id>")
            sys.exit(1)
        
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be a number.")
            sys.exit(1)

        mark_status(task_id, "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Usage: python task-cli.py mark-done <id>")
            sys.exit(1)
        
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be a number.")
            sys.exit(1)

        mark_status(task_id, "done")

    else:
        print("Unknown command.")