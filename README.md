Task Management API

This is a simple Task Management API built using Flask, which allows users to perform CRUD (Create, Read, Update, Delete) operations on their tasks. The API uses JSON files (tasks.json and users.json) for storage and supports user authentication.

Features
- User Authentication
- Task Management (Create, Read, Edit, Delete)
- Task Filters (Retrieve tasks based on specific criteria)

Endpoints

1. Add Task
URL: /task
Method: POST
Description: Adds a new task for the authenticated user.
Request Body:
{
  "add_task": true,
  "task_details": {
    "name": "Complete Assignment",
    "priority": "High",
    "due_date": "2024-11-30",
    "description": "Finish the project for CS101."
  },
  "user_details": {
    "username": "user123",
    "password": "password123"
  }
}
Response:
{
  "status": "success",
  "notification": "Task added successfully."
}
If authentication fails, the response will be:
{
  "status": "failure",
  "notification": "Invalid credentials."
}

2. Edit Task
URL: /task
Method: POST
Description: Edits an existing task for the authenticated user.
Request Body:
{
  "edit_task": true,
  "task_name": "Complete Assignment",
  "updated_task_details": {
    "priority": "Medium",
    "due_date": "2024-12-05",
    "description": "Finish the project and submit it."
  },
  "user_details": {
    "username": "user123",
    "password": "password123"
  }
}
Response:
{
  "status": "success",
  "notification": "Task updated successfully."
}
If task is not found:
{
  "status": "failure",
  "notification": "Task not found."
}

3. Remove Task
URL: /task
Method: POST
Description: Removes a task for the authenticated user.
Request Body:
{
  "remove_task": true,
  "task_name": "Complete Assignment",
  "user_details": {
    "username": "user123",
    "password": "password123"
  }
}
Response:
{
  "status": "success",
  "notification": "Task removed successfully."
}
If task is not found:
{
  "status": "failure",
  "notification": "Task not found."
}

4. Get Tasks
URL: /task
Method: POST
Description: Retrieves all tasks for the authenticated user, with optional filtering.
Request Body:
{
  "get_tasks": true,
  "user_details": {
    "username": "user123",
    "password": "password123"
  },
  "filters": {
    "priority": "High"
  }
}
Response:
{
  "status": "success",
  "tasks": [
    {
      "name": "Complete Assignment",
      "priority": "High",
      "due_date": "2024-11-30",
      "description": "Finish the project for CS101.",
      "timestamp": "2024-11-18 15:00:00"
    }
  ]
}
If no tasks are found:
{
  "status": "failure",
  "notification": "No tasks found for this user."
}

File Structure
- tasks.json: Stores the tasks data for all users.
- users.json: Stores the user credentials (username and password).

Authentication
- Users must provide a valid username and password in their request.
- The password is stored in plain text, but in a production environment, it's recommended to store hashed passwords.

Error Handling
- The API returns appropriate status codes and messages for errors like invalid credentials, missing tasks, or other issues.

Example Requests
1. Add Task: To add a task, send a POST request to /task with add_task set to true and the relevant task details in the body.

2. Get Tasks: To get tasks, send a POST request with get_tasks set to true. Optionally, include a filters object to filter tasks based on criteria like priority or due date.

3. Edit Task: To update a task, send a POST request with edit_task set to true along with the task_name and updated details.

4. Remove Task: To remove a task, send a POST request with remove_task set to true and the task_name to be deleted.

Running the Application
To run the Flask application locally, follow these steps:

1. Install dependencies:
   pip install Flask

2. Run the application:
   python app.py

The app will be running at http://127.0.0.1:5000.

UML Image
![uml_diagram](https://github.com/user-attachments/assets/d477e70a-c556-429b-854b-2c0a90996f17)

