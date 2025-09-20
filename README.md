# FastAPI Notes App - Backend

This is the backend API for the Notes Application, built using **FastAPI** and **MongoDB**.  
It provides authentication, user management, and CRUD operations for notes.

---

## Features

- User registration and login
- JWT-based authentication
- Protected routes for authenticated users
- CRUD operations for notes
- Async operations with MongoDB
- Proper error handling with HTTP status codes

---

## Base URL

```text
http://localhost:8000


Authentication Routes (/auth)
1. Sign Up

POST /auth/signup

Request Body:

{
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "password": "strongpassword"
}

Response

{
  "user_id": "uuid",
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "created_on": "2025-09-20T12:00:00Z",
  "last_update": "2025-09-20T12:00:00Z"
}

2. Login

POST /auth/login

Request Body:
{
  "user_email": "john@example.com",
  "password": "strongpassword"
}
Response
{
  "access_token": "jwt-token",
  "expires_in": 3600
}

3. Get Current User

GET /auth/me
Headers: Authorization: Bearer <token>
Response
{
  "user_id": "uuid",
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "created_on": "2025-09-20T12:00:00Z",
  "last_update": "2025-09-20T12:00:00Z"
}

1. Create Note

POST /notes/

Request Body:

{
  "note_title": "My Note",
  "note_content": "This is the note content"
}
Response
{
  "note_id": "uuid",
  "user_id": "uuid",
  "note_title": "My Note",
  "note_content": "This is the note content",
  "created_on": "2025-09-20T12:00:00Z",
  "last_update": "2025-09-20T12:00:00Z"
}

2. List Notes

GET /notes/

3. Get Single Note

GET /notes/{note_id}


4. Update Note

PUT /notes/{note_id}

5. Delete Note

DELETE /notes/{note_id}

Response: 204 No Content



## Installation & Run

Follow these steps to set up and run the FastAPI backend locally.

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-backend-folder>


