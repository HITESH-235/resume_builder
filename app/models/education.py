from app.extensions.db import db

class Education(db.Model):
    __tablename__ = "education"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    institution = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True) # null for current study
    description = db.Column(db.Text, nullable=True)
