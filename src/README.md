# Data Security - Login Management System

## Project Overview

This is a comprehensive Flask-based user authentication and login management system featuring role-based access control, secure password handling, and a modern web interface with Spongebob-themed design. The application provides secure user authentication, password reset functionality, and differentiated access levels for administrators and regular users.

## How the Project Works

### Architecture

The application follows a typical Flask web application structure:

- **Backend**: Python Flask framework handles routing, session management, and business logic
- **Database**: SQLite database for user data storage
- **Frontend**: HTML templates with custom CSS styling
- **Security**: SHA-256 password hashing and session-based authentication

### Core Components

1. **Flask Application** (`main.py`):
   - Main application entry point
   - Route definitions for all pages
   - Session management
   - Database interactions

2. **Database Layer** (`init_db.py`):
   - SQLite database initialization
   - User table creation with predefined test accounts
   - Password hashing utilities

3. **Web Interface**:
   - HTML templates in `templates/` folder
   - CSS styling in `styles/` folder
   - Responsive design with modern UI elements

### User Flow

1. **Authentication Process**:
   - User visits the site (redirects to `/login`)
   - Enters username and password
   - System hashes password and compares with database
   - On success: Creates session, updates user status to "logged_in", redirects to appropriate dashboard
   - On failure: Shows error message

2. **Role-Based Access**:
   - Admin users → `/admin` dashboard
   - Regular users → `/user` dashboard
   - Session validation on each protected route

3. **Password Recovery**:
   - User enters username on forgot password page
   - If exists, redirected to reset password page
   - New password is hashed and stored
   - Redirected back to login

4. **Logout Process**:
   - Updates user status to "logged_out"
   - Clears session
   - Redirects to login page

## Design and User Interface

### Visual Design Philosophy

The application combines professional security features with a fun, engaging user interface featuring:

- **Spongebob Squarepants Theme**: Full-screen background image with cartoon character theming
- **Glass-morphism Effects**: Semi-transparent cards with blur effects for modern appearance
- **Responsive Layout**: Works on desktop and mobile devices
- **Clean Typography**: Arial font family with clear hierarchy
- **Color Scheme**:
  - Primary Blue (#2563eb) for buttons and links
  - Semi-transparent white cards with blur
  - Red (#ef4444) for logout buttons and errors
  - Light blue for informational boxes

### Page Layouts

1. **Login Page** (`/login`):
   - Centered card with username/password fields
   - "Forgot Password?" link
   - Error message display area
   - Spongebob background image

2. **Admin Dashboard** (`/admin`):
   - Welcome message with username
   - Information box explaining admin privileges
   - Red logout button

3. **User Dashboard** (`/user`):
   - Welcome message with username
   - Information box explaining user access level
   - Red logout button

4. **Forgot Password** (`/forgot-password`):
   - Username input field
   - Error handling for non-existent users

5. **Reset Password** (`/reset-password/<username>`):
   - New password input field
   - Warning about password security

### Interactive Elements

- **Form Validation**: Required fields with visual feedback
- **Hover Effects**: Buttons lift and change color on hover
- **Error Messages**: Clear, user-friendly feedback in red
- **Responsive Design**: Adapts to different screen sizes

## Technology Stack

- **Backend Framework**: Flask (Python web framework)
- **Database**: SQLite (lightweight, file-based database)
- **Security**: SHA-256 password hashing via Python's hashlib
- **Frontend**: HTML5, CSS3
- **Styling**: Custom CSS with modern effects (backdrop-filter, blur)
- **Session Management**: Flask's built-in session handling
- **Development Environment**: Python virtual environment

## Database Schema

The application uses a single SQLite table:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL
)
```

**Fields**:
- `id`: Auto-incrementing primary key
- `username`: Unique username (string)
- `password_hash`: SHA-256 hashed password (string)
- `role`: User role ("admin" or "user")
- `status`: Login status ("logged_in" or "logged_out")

## Security Features

### Password Security
- **SHA-256 Hashing**: Passwords are never stored in plain text
- **Salt-free Hashing**: Uses direct SHA-256 of password string
- **No Password Recovery**: Only password reset functionality

### Session Security
- **Flask Sessions**: Server-side session storage
- **Secret Key**: Application uses a secret key for session encryption
- **Session Clearing**: Complete session cleanup on logout

### Access Control
- **Role-Based Access**: Different dashboards for admin/user roles
- **Session Validation**: Each protected route checks for valid session
- **Status Tracking**: Database tracks user login status

## Installation and Setup

### Prerequisites
- Python 3.x installed
- Virtual environment support

### Setup Steps

1. **Clone/Download the Project**:
   ```bash
   cd c:\data_security
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate Virtual Environment**:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. **Initialize Database**:
   ```bash
   python src/init_db.py
   ```

5. **Run the Application**:
   ```bash
   python main.py
   ```

6. **Access the Application**:
   - Open browser to: `http://127.0.0.1:5000`
   - Application will redirect to login page

### Test Credentials

**Admin Account**:
- Username: `admin`
- Password: `admin123`

**User Account**:
- Username: `alaa`
- Password: `user123`

## API Routes/Endpoints

| Route | Method | Description | Access |
|-------|--------|-------------|---------|
| `/` | GET | Home page (redirects to login) | Public |
| `/login` | GET/POST | User login page | Public |
| `/admin` | GET | Admin dashboard | Admin only |
| `/user` | GET | User dashboard | User only |
| `/forgot-password` | GET/POST | Password recovery initiation | Public |
| `/reset-password/<username>` | GET/POST | Password reset page | Public |
| `/logout` | GET/POST | User logout | Authenticated users |

## Key Functions and Code Structure

### Main Application Functions

- `hash_password(password)`: SHA-256 password hashing
- `get_user_by_username(username)`: Database user lookup
- `update_password(username, new_hash)`: Password update
- `update_user_status(username, status)`: Status tracking

### Route Handlers

- `home()`: Redirects to login
- `login()`: Handles login form and authentication
- `admin_page()`: Admin dashboard (protected)
- `user_page()`: User dashboard (protected)
- `forgot_password()`: Password recovery start
- `reset_password(username)`: Password reset form
- `logout()`: Session cleanup and logout

## Understanding the Code

### Database Operations
- All database connections use `sqlite3.connect("users.db")`
- Queries use parameterized statements for security
- Connections are properly closed after operations

### Session Management
- User data stored in Flask session: `username` and `role`
- Session validation on protected routes
- Complete session clearing on logout

### Password Handling
- Passwords hashed immediately on input
- No plain text password storage or transmission
- Reset functionality creates new hash

### Role-Based Logic
- Route protection checks `session.get("role")`
- Different redirect targets based on user role
- Admin has access to admin dashboard, users to user dashboard

## File Structure

```
c:\data_security\
├── main.py                    # Main Flask application
├── WEB_DESIGN_DESCRIPTION.md  # Design documentation
├── users.db                   # SQLite database (created by init_db.py)
└── src\
    ├── init_db.py            # Database initialization script
    ├── README.md             # This documentation
    ├── styles\
    │   └── style1.css        # Main stylesheet
    └── templates\
        ├── login.html        # Login page template
        ├── admin.html        # Admin dashboard template
        ├── user.html         # User dashboard template
        ├── forgot_pass.html  # Forgot password template
        └── reset_pass.html   # Reset password template
```

## Features Summary

✅ **Secure Authentication** with SHA-256 hashing
✅ **Role-Based Access Control** (Admin/User)
✅ **Password Reset Functionality**
✅ **Session Management** with status tracking
✅ **Responsive Web Design** with modern UI
✅ **Spongebob-themed Interface** for engaging UX
✅ **Glass-morphism Effects** for modern appearance
✅ **Mobile-Friendly Design**
✅ **Error Handling** and validation
✅ **SQLite Database** for data persistence

## Development Notes

- **Debug Mode**: Application runs with `debug=True` for development
- **Database Location**: `users.db` created in project root
- **Template Location**: Templates in `src/templates/`
- **Static Files**: CSS in `src/styles/`
- **Secret Key**: Hardcoded for development (should be environment variable in production)

This project demonstrates secure web development practices combined with modern UI design, making it both functional and visually appealing. The Spongebob theming adds a unique touch while maintaining professional security standards.

