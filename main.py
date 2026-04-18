from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_user_by_username(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()
    return user


def update_password(username, new_password_hash):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE username = ?",
        (new_password_hash, username)
    )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)

        if user:
            user_id, db_username, db_password_hash, role = user

            if hash_password(password) == db_password_hash:
                if role == "admin":
                    return redirect(url_for("admin_page"))
                else:
                    return redirect(url_for("user_page"))
            else:
                message = "Wrong password"
        else:
            message = "User not found"

    return render_template("login.html", message=message)


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        user = get_user_by_username(username)

        if user:
            return redirect(url_for("reset_password", username=username))
        else:
            message = "Username does not exist"

    return render_template("forgot_password.html", message=message)


@app.route("/reset-password/<username>", methods=["GET", "POST"])
def reset_password(username):
    if request.method == "POST":
        new_password = request.form["new_password"]
        hashed_password = hash_password(new_password)
        update_password(username, hashed_password)
        return redirect(url_for("login"))

    return render_template("reset_password.html", username=username)


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


@app.route("/user")
def user_page():
    return render_template("user.html")


if __name__ == "__main__":
    app.run(debug=True)