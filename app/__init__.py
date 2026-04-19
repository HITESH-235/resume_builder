from flask import Flask
from .extensions.db import db
from .extensions.jwt import jwt
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    # Set up paths for the built frontend
    # In production, we assume the 'dist' folder exists in the frontend directory
    frontend_dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'dist')
    
    app = Flask(__name__, static_folder=frontend_dist, static_url_path='/')
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or "47-fallback-key"
    
    # Use environment variable for DB in production, fallback to SQLite for local dev
    # Render and other platforms provide DATABASE_URL
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///resume.db")
    
    # Fix for SQLAlchemy 1.4+ which requires 'postgresql://' instead of 'postgres://'
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
        app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"].replace("postgres://", "postgresql://", 1)
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=20)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    db.init_app(app)
    jwt.init_app(app)

    from app.auth.routes import auth_bp
    from app.profile.routes import profile_bp
    from app.resume.routes import resume_bp
    from app.job_description.routes import jd_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(resume_bp, url_prefix="/api/resume")
    app.register_blueprint(jd_bp, url_prefix="/api/jd")

    # Serve the React app index at the root
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    # Catch-all for React client-side routing (handles page refreshes on non-root URLs)
    @app.errorhandler(404)
    def not_found(e):
        # If the request is an API call, return a JSON 404 error
        from flask import request, jsonify
        if request.path.startswith('/api/'):
            return jsonify(error="Not found"), 404
        
        # Otherwise, let the React router handle the unknown URL
        return app.send_static_file('index.html')

    with app.app_context():
        db.create_all()
    
    return app