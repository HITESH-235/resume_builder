from app.extensions.db import db

# association table for many-to-many (Profile <-> Skill)
profile_skills = db.Table(
    "profile_skills",
    db.Column("profile_id", db.Integer, db.ForeignKey("profile.id"), primary_key=True),
    db.Column("skill_id", db.Integer, db.ForeignKey("skill.id"), primary_key=True),
)

class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)

    # one-to-many: 1 profile -> many experiences
    experiences = db.relationship("Experience", backref="profile", lazy=True)

    # one-to-many: 1 profile -> many educations
    educations = db.relationship("Education", backref="profile", cascade="all, delete-orphan")
    projects = db.relationship("Project", backref="profile", cascade="all, delete-orphan")
    certifications = db.relationship("Certification", backref="profile", cascade="all, delete-orphan")
    courses = db.relationship("Course", backref="profile", cascade="all, delete-orphan")
    achievements = db.relationship("Achievement", backref="profile", cascade="all, delete-orphan")

    # many-to-many: profile <-> skills
    skills = db.relationship("Skill", secondary=profile_skills, backref="profiles")