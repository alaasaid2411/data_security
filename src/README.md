# Data Security - Login Management System

## Project Overview

This project is a Flask web application for user authentication. It was built for a data security class assignment and demonstrates login with username and password, password hashing, role-based access control, password reset, and an SQL database.

The application runs locally on `localhost` and uses SQLite for storing users.

## Main Features

- Login page with username and password.
- Register page for creating new standard users.
- Passwords are stored as SHA-256 hashes, not as plaintext.
- Admin and standard user roles.
- Admin has a different access page than a regular user.
- Forgot password flow that creates a new password instead of restoring the old one.
- Session-based login and logout.
- User status tracking in the database: `logged_in` or `logged_out`.
- Error messages for wrong password or missing username.
- Responsive HTML/CSS interface.

## Technologies

- Python
- Flask
- SQLite
- HTML
- CSS
- SHA-256 hashing with Python `hashlib`

## File Structure

```text
project-root/
|-- main.py
|-- users.db
|-- WEB_DESIGN_DESCRIPTION.md
|-- src/
    |-- __init__.py
    |-- README.md
    |-- app.py
    |-- auth_service.py
    |-- database.py
    |-- init_db.py
    |-- routes.py
    |-- security.py
    |-- styles/
    |   |-- style1.css
    |-- templates/
        |-- login.html
        |-- register.html
        |-- admin.html
        |-- user.html
        |-- forgot_pass.html
        |-- reset_pass.html
```

## Layered Design Pattern

The project is organized into clear layers instead of putting the full implementation inside `main.py`.

### Entry Point Layer

`main.py`

- Starts the application.
- Imports `create_app()`.
- Does not contain route logic, database logic, or password logic.

### Application Factory Layer

`src/app.py`

- Creates the Flask application.
- Connects the templates folder and static CSS folder.
- Registers all routes.

### Routes / Controller Layer

`src/routes.py`

- Contains the HTTP routes.
- Reads form data from the frontend.
- Uses the service layer to perform authentication actions.
- Decides which page to render or where to redirect.

Examples:

- `/login`
- `/register`
- `/admin`
- `/user`
- `/forgot-password`
- `/reset-password/<username>`
- `/logout`

### Service / Business Logic Layer

`src/auth_service.py`

- Contains the authentication logic.
- Checks if a username exists.
- Checks if the password is correct.
- Handles password reset.
- Handles logout status updates.

This layer connects the routes to the database layer without exposing database details to the routes.

### Database Access Layer

`src/database.py`

- Contains all direct SQLite operations.
- Opens connections to `users.db`.
- Gets users by username.
- Updates password hashes.
- Updates user login status.

### Security Layer

`src/security.py`

- Contains the `PasswordHasher` class.
- Uses SHA-256 to hash passwords before comparing or saving them.
- Keeps password hashing inside a dedicated object instead of a standalone function.

### Frontend Layer

`src/templates/` and `src/styles/`

- `templates/` contains the HTML pages.
- `styles/style1.css` contains the CSS design.
- The frontend sends form data to the backend routes.

## Request Flow Example

Login request flow:

```text
Browser form
-> src/routes.py
-> src/auth_service.py
-> src/security.py
-> src/database.py
-> users.db
```

If the login is successful, the user is redirected based on their role:

```text
admin user -> /admin
standard user -> /user
```

## Database

The database is implemented with SQLite in the file `users.db`.

The application uses one table named `users`:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL
);
```

### Initial Users

The database initialization script creates two users:

| Username | Password | Role | Notes |
|---|---|---|---|
| `admin` | `admin123` | `admin` | First user in the database |
| `alaa` | `user123` | `user` | Standard user |

The passwords above are only the test credentials. In the database itself, the passwords are stored as SHA-256 hashes.

## Application Routes

| Route | Methods | Description |
|---|---|---|
| `/` | GET | Redirects to `/login` |
| `/login` | GET, POST | Login page |
| `/register` | GET, POST | Register a new standard user |
| `/admin` | GET | Admin page, available only for admin users |
| `/user` | GET | Standard user page |
| `/forgot-password` | GET, POST | Starts the password reset flow |
| `/reset-password/<username>` | GET, POST | Creates and saves a new password |
| `/logout` | GET, POST | Logs out and clears the session |

## How Authentication Works

1. The user enters a username and password on the login page.
2. The application searches for the username in the SQL database.
3. The entered password is hashed with SHA-256.
4. The hash is compared with the saved password hash in the database.
5. If the credentials are correct:
   - The username and role are saved in the Flask session.
   - The user status is updated to `logged_in`.
   - Admin users are redirected to `/admin`.
   - Standard users are redirected to `/user`.
6. If the credentials are wrong, an error message is displayed on the login page.

## Password Reset

The application does not restore or display the old password.

Instead:

1. The user enters their username in `/forgot-password`.
2. If the username exists, the user is redirected to a reset page.
3. The user enters a new password.
4. The new password is hashed with SHA-256.
5. The hash replaces the old hash in the database.

This demonstrates that the original password cannot be recovered from the database.

## Running the Project

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Flask

```powershell
pip install flask
```

### 4. Initialize the database

```powershell
python src\init_db.py
```

### 5. Run the application

```powershell
python main.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Security Notes

This project is suitable for a class assignment and demonstrates important security concepts:

- Passwords are not stored in plaintext.
- SQL queries use parameters.
- Sessions are used to keep users logged in.
- Admin and user roles are separated.
- The old password cannot be recovered during password reset.

For a real production system, the project should be improved with:

- A stronger password hashing algorithm such as bcrypt or Argon2.
- A secret key stored in an environment variable instead of directly in the code.
- A safer password reset process using a temporary reset token.
- CSRF protection for forms.
- Stronger password rules.

## Current Implementation Status

Implemented:

- Layered backend structure.
- Login system.
- Standard user registration.
- SHA-256 password hashing.
- SQLite database.
- Admin and user separation.
- Forgot password and reset password pages.
- Logout.
- Login error messages.
- Cleaned CSS without missing image dependencies.

Not implemented:

- New user registration.
- Admin user management panel.
- Email-based password reset.
- Production-level security hardening.
