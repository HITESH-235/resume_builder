from app.extensions.db import db

class Course(db.Model):
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    institution = db.Column(db.String(150), nullable=False)

    date = db.Column(db.Date, nullable=False)
