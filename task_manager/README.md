# Task Management API

## Project Overview
This is a Django REST Framework-based Task Management API with custom user authentication using mobile phone numbers.

## Features
- Custom user model with phone number authentication
- Task CRUD operations
- Task filtering by status and title
- Role-based permissions

## Prerequisites
- Docker
- Docker Compose
- Python 3.10+

## Setup and Installation

### Local Development
1. Clone the repository
2. Create a `.env` file with your configuration
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Start the server:
   ```
   python manage.py runserver
   ```

### Docker Deployment
1. Build and run the containers:
   ```
   docker-compose up --build
   ```

## API Endpoints
- `/api/tasks/`: CRUD operations for tasks
- `/api/users/register/`: User registration
- `/api/users/login/`: User login

## Testing
Run tests with:
```
python manage.py test
```

## Postman Collection
Import the Postman collection from `task_management_api.postman_collection.json`

## Authentication
Use phone number and password for authentication. 
Obtain JWT token via login endpoint.

Register a user via POST /api/users/register/
Login a user via POST /api/users/login/
Create tasks via POST /api/tasks/
List tasks via GET /api/tasks/
Filter tasks via GET /api/tasks/filter
