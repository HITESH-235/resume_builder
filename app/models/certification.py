from app.extensions.db import db

class Certification(db.Model):
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    issuer = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(255), nullable=True)

    date = db.Column(db.Date, nullable=False)
