from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Flask application factory pattern
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:admin@mysql-db:3306/flask_app"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Importing and registering the blueprint here avoids circular imports
    from .routes import main
    app.register_blueprint(main)

    # Ensure database tables are created
    with app.app_context():
        db.create_all()

    return app
