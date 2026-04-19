from flask import Flask
from .extensions.db import db
from .extensions.jwt import jwt
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or "47-fallback-key"
    
    # didnt give the abs path, so creates insider instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///resume.db' 
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=20)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    # optional: helps debugging during development
    app.config["DEBUG"] = True

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

    with app.app_context():
        db.create_all()
    
    return app