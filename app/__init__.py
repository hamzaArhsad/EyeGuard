from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from sqlalchemy import text

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    from app.routes import camera_routes
    app.register_blueprint(camera_routes.camera_bp)
    from app.routes import user_routes
    app.register_blueprint(user_routes.user_bp)
    from app.routes import auth_routes
    app.register_blueprint(auth_routes.auth_bp)
    from app.routes import flaged_incident_routes
    app.register_blueprint(flaged_incident_routes.flaged_incident_bp)

    # Create database tables
    with app.app_context():
     # Enable foreign key support in SQLite
     with db.engine.connect() as connection:
        connection.execute(db.text("PRAGMA foreign_keys = ON;"))
    # Recreate tables
     db.create_all()
    return app
