from flask import Flask
from .extensions.db import db
from .extensions.jwt import jwt


def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///resume.db' 
    # didnt give the abs path, so creates insider instance folder
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = '47-secret-key' 

    db.init_app(app)
    jwt.init_app(app)

    from app.auth.routes import auth_bp
    from app.profile.routes import profile_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')

    with app.app_context():
        db.create_all()
    
    return app