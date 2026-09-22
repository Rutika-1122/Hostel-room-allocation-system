from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from models.user_model import get_user_by_email, create_user

auth_bp = Blueprint("auth", __name__)
auth_controller = auth_bp


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        student_id = request.form.get("student_id", "").strip()

        # Validation: empty or missing fields
        if not name or not email or not password or not student_id:
            flash("All fields are required.", "error")
            return render_template("register.html")

        # Validation: email without @
        if "@" not in email:
            flash("Please enter a valid email address.", "error")
            return render_template("register.html")

        # Validation: duplicate email
        existing_user = get_user_by_email(email)
        if existing_user:
            flash("Email already registered.", "error")
            return render_template("register.html")

        # Successful registration
        create_user(
            name=name,
            email=email,
            password=password,
            student_id=student_id,
            role="Student",
        )
        flash("Registration successful. Please login to continue.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # If already logged in, redirect directly to dashboard
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # Validation: empty or missing fields
        if not email or not password:
            flash("Please enter both email and password.", "error")
            return render_template("login.html")

        # Check if user exists
        user = get_user_by_email(email)
        if not user:
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        # Validate password (support both plain text and hashed passwords)
        stored_password = user["password"]
        password_valid = False
        if stored_password == password:
            password_valid = True
        else:
            try:
                if check_password_hash(stored_password, password):
                    password_valid = True
            except Exception:
                password_valid = False

        if not password_valid:
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        # Set user session
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["role"] = user["role"]
        session["email"] = user["email"]
        session["student_id"] = user.get("student_id")

        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth.login"))

