from app.extensions.db import db

class Project(db.Model):
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(255), nullable=True)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

    def __init__(self, **kwargs):
        super(Project, self).__init__(**kwargs)
