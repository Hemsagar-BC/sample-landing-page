# FocusFlow API Backend

A simple FastAPI backend for the FocusFlow landing page with user authentication.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
uvicorn main:app --reload --port 8001
```

The API will be available at: `http://localhost:8001`

## API Documentation

Interactive API docs available at: `http://localhost:8001/docs`

## Endpoints

### Authentication

#### Signup
- **POST** `/auth/signup`
- **Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123"
}
```
- **Response:** User object with token

#### Login
- **POST** `/auth/login`
- **Body:**
```json
{
  "username": "john_doe",
  "password": "password123"
}
```
- **Response:** User object with token

#### Logout
- **POST** `/auth/logout?token=YOUR_TOKEN`
- **Response:** Success message

### User Profile

#### Get Profile
- **GET** `/user/profile?token=YOUR_TOKEN`
- **Response:** User profile data

#### Update Profile
- **PUT** `/user/profile?token=YOUR_TOKEN&email=newemail@example.com`
- **Response:** Updated user profile

### Health Check
- **GET** `/health`
- **Response:** API status

## Features

✅ User Registration (Signup)
✅ User Login
✅ User Logout
✅ Get User Profile
✅ Update User Email
✅ Token-based Authentication
✅ In-memory Storage (no database needed)
✅ CORS enabled for frontend integration
✅ Interactive API documentation (Swagger UI)

## Notes

- Passwords are stored in plain text for demo purposes. In production, use hashing (bcrypt, argon2)
- User data is stored in memory and will be lost when the server restarts
- For production, use a real database (PostgreSQL, MongoDB, etc.)
