from flask import redirect, render_template, request, session, url_for

from src.auth_service import (
    authenticate_user,
    logout_user,
    register_user,
    reset_user_password,
    username_exists,
)


def register_routes(app):
    @app.route("/")
    def home():
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        message = ""

        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            user, message = authenticate_user(username, password)

            if user:
                session["username"] = user["username"]
                session["role"] = user["role"]

                if user["role"] == "admin":
                    return redirect(url_for("admin_page"))

                return redirect(url_for("user_page"))

        return render_template("login.html", message=message)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        message = ""

        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            created, message = register_user(username, password)

            if created:
                return redirect(url_for("login"))

        return render_template("register.html", message=message)

    @app.route("/admin")
    def admin_page():
        if "username" not in session or session.get("role") != "admin":
            return redirect(url_for("login"))

        return render_template("admin.html", username=session.get("username"))

    @app.route("/user")
    def user_page():
        if "username" not in session or session.get("role") != "user":
            return redirect(url_for("login"))

        return render_template("user.html", username=session.get("username"))

    @app.route("/forgot-password", methods=["GET", "POST"])
    def forgot_password():
        message = ""

        if request.method == "POST":
            username = request.form["username"]

            if username_exists(username):
                session["reset_allowed_for"] = username
                return redirect(url_for("reset_password", username=username))

            message = "Username does not exist"

        return render_template("forgot_pass.html", message=message)

    @app.route("/reset-password/<username>", methods=["GET", "POST"])
    def reset_password(username):
        if session.get("reset_allowed_for") != username:
            return redirect(url_for("forgot_password"))

        if request.method == "POST":
            new_password = request.form["new_password"]
            reset_user_password(username, new_password)
            session.pop("reset_allowed_for", None)
            return redirect(url_for("login"))

        return render_template("reset_pass.html", username=username)

    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        logout_user(session.get("username"))
        session.clear()
        return redirect(url_for("login"))
