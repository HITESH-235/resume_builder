from datetime import datetime, timezone
from app.extensions.db import db


class Resume(db.Model):
    __tablename__ = "resume"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),  # fixed ForeignKey
        nullable=False,
        index=True
    )

    title = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime(timezone=True),  # fixed DateTime
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),  # fixed DateTime
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # one resume - many experiences
    experiences = db.relationship(
        "ResumeExperience",
        backref="resume",
        lazy="selectin"  # loads all related rows in ONE extra query instead of N queries
    )

    # one resume - many resume skills
    skills = db.relationship(
        "ResumeSkill",
        backref="resume",
        lazy="selectin"
    )


class ResumeExperience(db.Model):
    __tablename__ = "resume_experience"  # added

    resume_id = db.Column(
        db.Integer,
        db.ForeignKey("resume.id"),
        primary_key=True
    )

    experience_id = db.Column(
        db.Integer,
        db.ForeignKey("experience.id"),
        primary_key=True
    )

    order = db.Column(db.Integer, nullable=False)  # stores position in the order

    experience = db.relationship("Experience", backref="resume_links")

    # restricts duplicate combination of order and resume id
    __table_args__ = (
        db.UniqueConstraint("resume_id", "order", name="uq_resume_exp_order"),
    )


class ResumeSkill(db.Model):  # moved out (not nested)
    __tablename__ = "resume_skill"  # fixed wrong assignment

    resume_id = db.Column(
        db.Integer,
        db.ForeignKey("resume.id"),
        primary_key=True
    )

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skill.id"),
        primary_key=True
    )

    order = db.Column(db.Integer, nullable=False)

    skill = db.relationship("Skill", backref="resume_links")

    __table_args__ = (
        db.UniqueConstraint("resume_id", "order", name="uq_resume_skill_order"),
    )