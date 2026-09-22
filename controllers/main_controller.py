from flask import Blueprint, redirect, url_for, session, render_template, flash
from models import fetch_records

main_bp = Blueprint("main", __name__)
main_controller = main_bp


@main_bp.route("/", methods=["GET"])
def index():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        flash("Please log in to access your dashboard.", "error")
        return redirect(url_for("auth.login"))

    user_info = {
        "id": session.get("user_id"),
        "name": session.get("user_name"),
        "role": session.get("role"),
        "email": session.get("email"),
        "student_id": session.get("student_id"),
    }

    # Fetch counts or summary for dashboard if available
    rooms_count = 0
    requests_count = 0
    try:
        rooms_res = fetch_records("SELECT COUNT(*) AS count FROM rooms")
        if rooms_res:
            rooms_count = rooms_res[0].get("count", 0)
        req_res = fetch_records("SELECT COUNT(*) AS count FROM room_requests")
        if req_res:
            requests_count = req_res[0].get("count", 0)
    except Exception:
        pass

    return render_template(
        "dashboard.html",
        user=user_info,
        rooms_count=rooms_count,
        requests_count=requests_count,
    )


@main_bp.route("/rooms", methods=["GET"])
def rooms():
    if "user_id" not in session:
        flash("Please log in to view rooms.", "error")
        return redirect(url_for("auth.login"))

    rooms_list = []
    try:
        rooms_list = fetch_records("SELECT * FROM rooms")
    except Exception:
        rooms_list = []

    return render_template("rooms.html", rooms=rooms_list, user=session)

