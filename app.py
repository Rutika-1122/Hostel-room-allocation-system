import os
import urllib.parse
from dotenv import load_dotenv
from flask import Flask
from models import db
from controllers.main_controller import main_bp
from controllers.db_controller import db_bp
from controllers.auth_controller import auth_bp

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Build MySQL connection URL with URL-encoded username and password
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "hostel_db")

    encoded_user = urllib.parse.quote_plus(db_user)
    encoded_password = urllib.parse.quote_plus(db_password)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{encoded_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "hostel_room_allocation_secret_key_2026")

    # Initialize database extension
    db.init_app(app)

    # Register blueprints - no route handlers in this file
    app.register_blueprint(main_bp)
    app.register_blueprint(db_bp)
    app.register_blueprint(auth_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
