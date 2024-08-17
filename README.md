# FastAPI TodoApp

The **FastAPI Todo App** is a robust task management application built with the FastAPI framework. It is designed to help users efficiently organize and track their tasks with a clean and intuitive interface. The app supports user authentication, task management, and secure access to user-specific tasks.

## Key Features:
- **User Authentication:**
  - **Signup:** Users can create new accounts.
  - **Login:** Users can log in to access their tasks.
  - **JWT Authorization:** Secure access to user-specific tasks using JSON Web Tokens (JWT).

- **Task Management:**
  - **Task Creation:** Easily add new tasks with descriptions and deadlines.
  - **Task Update:** Edit task details and update their status.
  - **Task Deletion:** Remove tasks that are no longer needed.
  - **Mark as Done:** Track completed tasks.

- **User-Specific Todos:**
  - Users can view and manage only their own tasks.
  - Each user’s tasks are securely stored and managed.

- **Responsive Web Interface:**
  - A user-friendly web interface for managing tasks.
  - **Home Page:** View tasks, create new tasks, and manage existing ones.
  - **Signup Page:** Create a new user account.
  - **Login Page:** Access your account.
  - **About Page:** Learn more about the application.
  - **404 Page:** Custom error page for non-existent routes.

- **Automatic Timestamps:** 
  - Track when each task was created and completed.

- **Persistent Storage:**
  - All tasks and user information are stored in an SQLite database, ensuring data persistence between sessions.

## Technology Stack:
- **FastAPI:** A modern, high-performance web framework for building APIs with Python 3.7+.
- **SQLite:** A lightweight, file-based database for persistent storage of todos and user data.
- **SQLAlchemy:** An ORM (Object-Relational Mapping) library for handling database operations.
- **Pydantic:** Used for data validation and serialization.
- **HTML/CSS:** Provides the basic web frontend for interacting with the app.

## Getting Started:
The FastAPI Todo App is perfect for developers looking to explore FastAPI while building a practical application. Whether you’re managing your personal tasks or collaborating on a small project, this app provides a straightforward solution for staying organized.
