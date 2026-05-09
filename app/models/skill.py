from app.extensions.db import db

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, **kwargs):
        super(Skill, self).__init__(**kwargs)