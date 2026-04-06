from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy() # initiate the sqlalch obj to interact with db
# don't define db again in init file


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    # one to one rel: 1 user -> 1 profile
    profile = db.relationship('Profile', backref='user', uselist=False) # one to one link
    # useList (def=True) assumes every relation to be one to many, hence change it

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Many to Many rel: (Profile - Skills) (Raw table rather than a model class)
profile_skills = db.Table('profile_skills',
    db.Column('profile_id', db.Integer, db.ForeignKey('profile.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    )


class Profile(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)

    # one to many rel: 1 profile -> many experiences
    experiences = db.relationship('Experience', backref='profile', lazy=True) # plural since many exp for one profile

    # profile_skills becomes the joint table for bw profiles and skills, containing unique pairs
    skills = db.relationship('Skill', secondary=profile_skills, backref='profiles') # this way a many-many relation is created
    # notice the reference "profiles" (not "profile") to maintain many-many convention


class Experience(db.Model):
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True) # end date null for curr job

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)