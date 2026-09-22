from models import fetch_records, insert_record


def get_user_by_email(email):
    """Fetch a user record by email address."""
    query = "SELECT * FROM users WHERE email = :email"
    records = fetch_records(query, {"email": email})
    return records[0] if records else None


def create_user(name, email, password, student_id, role="Student"):
    """Insert a new user into the users table and return the new row ID."""
    query = """
        INSERT INTO users (name, email, password, role, student_id)
        VALUES (:name, :email, :password, :role, :student_id)
    """
    params = {
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "student_id": student_id,
    }
    return insert_record(query, params)
