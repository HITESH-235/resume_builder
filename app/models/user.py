from app.extensions.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    # one to one rel: 1 user -> 1 profile
    profile = db.relationship('Profile', backref='user', uselist=False) # one to one link
    # useList (def=True) assumes every relation to be one to many, hence change it

    job_descriptions = db.relationship('JobDescription', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)