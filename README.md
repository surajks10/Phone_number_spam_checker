# Flask REST API Application

This is a Flask-based REST API that allows users to manage contacts, identify spam numbers, and search for users by name or phone number.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Managing Migrations](#managing-migrations)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)

## Features
- User registration and login with JWT authentication.
- Contact management.
- Mark phone numbers as spam.
- Search users by name or phone number.
- View details of users.

## Requirements
- Python 3.8 or later
- pip (Python package installer)

## Setup


1. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Database Setup

1. **SQLite Configuration:**
    - By default, this app is configured to use SQLite, which stores data in a file. The database file will be created in the project directory.

    - The default SQLite database URI is already set in the `config.py` file:
    ```python
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    ```

2. **Initialize the database and create tables:**
    - Run the following command to create the tables:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

    - This will create an `app.db` file in your project directory, which contains your database.

## Running the Application

1. **Start the Flask development server:**
    ```bash
    flask run
    ```
   - The application will be available at `http://127.0.0.1:5000`.

## Managing Migrations

1. **Create a new migration when models are updated:**
    ```bash
    flask db migrate -m "Description of changes"
    ```

2. **Apply the migration:**
    ```bash
    flask db upgrade
    ```

3. **Roll back the last migration:**
    ```bash
    flask db downgrade
    ```

## Running Tests

1. **Run the test suite:**
    ```bash
    python -m unittest discover -s tests
    ```

## API Endpoints

### **User Registration**
- **Endpoint**: `/register`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "name": "John Doe",
        "phone_number": "1234567890",
        "password": "password123",
        "email": "john@example.com"
    }
    ```

### **User Login**
- **Endpoint**: `/login`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "phone_number": "1234567890",
        "password": "password123"
    }
    ```

### **Mark Number as Spam**
- **Endpoint**: `/spam`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <your_jwt_token>`
- **Request Body**:
    ```json
    {
        "phone_number": "0987654321"
    }
    ```

### **Search by Name**
- **Endpoint**: `/search?name=<name>`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <your_jwt_token>`

### **Search by Phone Number**
- **Endpoint**: `/search?phone_number=<phone_number>`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <your_jwt_token>`
