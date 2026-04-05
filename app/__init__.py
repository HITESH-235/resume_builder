from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .models import db


def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///resume.db' 
    # didnt give the abs path, so creates insider instance folder
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = '47-secret-key'    

    db.init_app(app)
    jwt = JWTManager(app)

    from .routes import auth_bp, profile_bp # registering blueprints:
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')

    with app.app_context():
        db.create_all()
    
    return app