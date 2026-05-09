from app.extensions.db import db

class Achievement(db.Model):
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    date = db.Column(db.Date, nullable=False)

    def __init__(self, **kwargs): # contructor to make it easier to create objects
        super(Achievement, self).__init__(**kwargs) # (kwargs processes simple inputs to dictionary and passes to super class)
