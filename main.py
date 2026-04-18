from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__, template_folder='src/templates', static_folder='src/styles', static_url_path='/static')
app.secret_key = "data_security_secret_key"


# the function to hash the password using SHA-256 algorithm
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#table creation and inserting data into it
def get_user_by_username(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash, role, status FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()
    return user


#cahnge the password paeg 
def update_password(username, new_password_hash):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE username = ?",
        (new_password_hash, username)
    )

    conn.commit()
    conn.close()

# the function to update the user status in the database
def update_user_status(username, new_status):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET status = ? WHERE username = ?",
        (new_status, username)
    )

    conn.commit()
    conn.close()

# the hoem page is the loiin page the user cant login to teh web with out username and password
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
            user_id, db_username, db_password_hash, role, status = user

            if hash_password(password) == db_password_hash:
                session["username"] = db_username
                session["role"] = role

                update_user_status(db_username, "logged_in")

                if role == "admin":
                    return redirect(url_for("admin_page"))
                else:
                    return redirect(url_for("user_page"))
            else:
                message = "Wrong password"
        else:
            message = "User not found"

    return render_template("login.html", message=message)



@app.route("/admin")
def admin_page():
    if "username" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin.html", username=session.get("username"))


@app.route("/user")
def user_page():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("user.html", username=session.get("username"))





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

    return render_template("forgot_pass.html", message=message)


@app.route("/reset-password/<username>", methods=["GET", "POST"])
def reset_password(username):
    if request.method == "POST":
        new_password = request.form["new_password"]
        hashed_password = hash_password(new_password)
        update_password(username, hashed_password)
        return redirect(url_for("login"))

    return render_template("reset_pass.html", username=username)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    username = session.get("username")

    if username:
        update_user_status(username, "logged_out")

    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)