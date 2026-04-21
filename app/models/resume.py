from datetime import datetime, timezone
from app.extensions.db import db


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),  # fixed ForeignKey
        nullable=False,
        index=True
    )

    # all resume specific fields:
    title = db.Column(db.String(150), nullable=False)  # Displayed on the PDF
    name = db.Column(db.String(150), nullable=True)     # Dashboard label / heading
    summary = db.Column(db.Text)
    designation = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(150), nullable=True)

    created_at = db.Column( # putting this column in Resume just as a good practice
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # all many-many relationship (e.g. one resume-many exp, and vice versa)
    skills = db.relationship("ResumeSkill", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    experiences = db.relationship("ResumeExperience", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    educations = db.relationship("ResumeEducation", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    projects = db.relationship("ResumeProject", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    certifications = db.relationship("ResumeCertification", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    courses = db.relationship("ResumeCourse", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    achievements = db.relationship("ResumeAchievement", backref="resume", lazy="selectin", cascade="all, delete-orphan")


class ResumeSkill(db.Model):  # moved out (not nested)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), primary_key=True)
    order = db.Column(db.Integer, nullable=False) # stores position in the order
    skill = db.relationship("Skill", backref="resume_links")

    __table_args__ = ( # restricts duplicate combination of order and resume id
        db.UniqueConstraint("resume_id", "order", name="uq_resume_skill_order"),
    )


class ResumeExperience(db.Model):
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), primary_key=True)
    experience_id = db.Column(db.Integer, db.ForeignKey("experience.id"), primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    experience = db.relationship("Experience", backref="resume_links")

    __table_args__ = (
        db.UniqueConstraint("resume_id", "order", name="uq_resume_exp_order"),
    )


class ResumeEducation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    education_id = db.Column(db.Integer, db.ForeignKey('education.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    education = db.relationship("Education", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("resume_id", "order", name="uq_resume_edu_order"),
    )


class ResumeProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    project = db.relationship("Project", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("resume_id", "order", name="uq_resume_proj_order"),
    )


class ResumeCertification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    certification_id = db.Column(db.Integer, db.ForeignKey('certification.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    certification = db.relationship("Certification", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("resume_id", "order", name="uq_resume_cert_order"),
    )


class ResumeCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    course = db.relationship("Course", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("resume_id", "order", name="uq_resume_course_order"),
    )


class ResumeAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    achievement = db.relationship("Achievement", lazy="joined")

    __table_args__ = (
        db.UniqueConstraint("resume_id", "order", name="uq_resume_achieve_order"),
    )