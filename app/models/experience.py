from app.extensions.db import db

class Experience(db.Model):
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True) # end date null for curr job