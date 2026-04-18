# Data Security - Login Management System

## Project Description
This is a Flask-based user authentication system with login, password reset, and role-based access control (admin and user roles).

## What This Project Does

This project is a **secure login management system** that provides:

1. **User Authentication** - Allows users to securely log in with username and password
2. **Password Security** - Uses SHA-256 hashing to securely store passwords in SQLite database
3. **Role-Based Access Control** - Different access levels for Admin and User roles:
   - **Admin Users** - Can access the admin dashboard with full privileges
   - **Regular Users** - Can access the user dashboard with limited privileges
4. **Password Recovery** - Users can reset their password if they forget it
5. **Responsive Web Interface** - Clean, modern UI with CSS styling that works on different devices

### How It Works:
- Users visit the login page (`/login`)
- They enter their credentials (username & password)
- The system verifies the password against the database using secure hashing
- If credentials are valid, users are redirected to their dashboard (Admin or User page)
- If users forget their password, they can use "Forgot Password" to reset it
- Each user has a secure session in their respective dashboard

## Test Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`

### User Account
- **Username:** `alaa`
- **Password:** `user123`

## Features
- User login with authentication
- Role-based access (Admin/User)
- Password reset functionality
- Secure password hashing (SHA-256)
- Responsive UI with CSS styling

## Running the Application
1. Activate the virtual environment: `.venv\Scripts\Activate.ps1`
2. Run the app: `python main.py`
3. Open in browser: `http://127.0.0.1:5000`

