from app.extensions.db import db

class CustomItem(db.Model):
    __tablename__ = "custom_item"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"), nullable=False)
    
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=True)

    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)

    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0)

    # profile relationship is handled in profile.py or here