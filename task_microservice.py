from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# File paths for storage
TASKS_FILE = "tasks.json"
USERS_FILE = "users.json"

# Load data from files
def load_data(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save data to files
def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Authentication
def authenticate(user_details):
    users = load_data(USERS_FILE)
    username = user_details.get("username")
    password = user_details.get("password")
    
    # Ensure the user exists and password matches
    if username in users and users[username] == password:
        return True
    return False

# Add Task
def add_task(task_details, user_details):
    if not authenticate(user_details):
        return {"status": "failure", "notification": "Invalid credentials."}
    
    tasks = load_data(TASKS_FILE)
    username = user_details["username"]
    
    # Initialize tasks for user if they don't exist
    if username not in tasks:
        tasks[username] = []
    
    # Add timestamp and append to the user's task list
    task_details["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks[username].append(task_details)
    save_data(TASKS_FILE, tasks)
    
    return {"status": "success", "notification": "Task added successfully."}

# Edit Task
def edit_task(task_name, updated_task_details, user_details):
    if not authenticate(user_details):
        return {"status": "failure", "notification": "Invalid credentials."}
    
    tasks = load_data(TASKS_FILE)
    username = user_details["username"]
    
    if username not in tasks or not tasks[username]:
        return {"status": "failure", "notification": "No tasks found for this user."}
    
    for task in tasks[username]:
        if task["name"] == task_name:
            task.update(updated_task_details)
            save_data(TASKS_FILE, tasks)
            return {"status": "success", "notification": "Task updated successfully."}
    
    return {"status": "failure", "notification": "Task not found."}

# Remove Task
def remove_task(task_name, user_details):
    if not authenticate(user_details):
        return {"status": "failure", "notification": "Invalid credentials."}
    
    tasks = load_data(TASKS_FILE)
    username = user_details["username"]
    
    if username not in tasks or not tasks[username]:
        return {"status": "failure", "notification": "No tasks found for this user."}
    
    for task in tasks[username]:
        if task["name"] == task_name:
            tasks[username].remove(task)
            save_data(TASKS_FILE, tasks)
            return {"status": "success", "notification": "Task removed successfully."}
    
    return {"status": "failure", "notification": "Task not found."}

# Retrieve Tasks
def get_tasks(user_details):
    if not authenticate(user_details):
        return {"status": "failure", "notification": "Invalid credentials."}
    
    tasks = load_data(TASKS_FILE)
    username = user_details["username"]
    user_tasks = tasks.get(username, [])
    
    return {"status": "success", "tasks": user_tasks}

@app.route("/task", methods=["POST"])
def task_handler():
    data = request.json

    # Check for action key in the request and process accordingly
    if data.get("add_task"):
        return jsonify(add_task(data.get("task_details"), data.get("user_details")))
    
    elif data.get("edit_task"):
        return jsonify(
            edit_task(
                data.get("task_name"),
                data.get("updated_task_details"),
                data.get("user_details"),
            )
        )
    
    elif data.get("remove_task"):
        return jsonify(remove_task(data.get("task_name"), data.get("user_details")))
    
    elif data.get("get_tasks"):
        return jsonify(get_tasks(data.get("user_details")))
    
    else:
        return jsonify({"status": "failure", "notification": "Invalid request."})

if __name__ == "__main__":
    app.run(debug=True)
