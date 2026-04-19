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

    title = db.Column(db.String(150), nullable=False)  # Displayed on the PDF
    name = db.Column(db.String(150), nullable=True)     # Dashboard label / heading
    summary = db.Column(db.Text)
    designation = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(150), nullable=True)

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

    # one resume - many educations
    educations = db.relationship(
        "ResumeEducation",
        backref="resume",
        lazy="selectin"
    )

    projects = db.relationship("ResumeProject", backref="resume", lazy="selectin")
    certifications = db.relationship("ResumeCertification", backref="resume", lazy="selectin")
    courses = db.relationship("ResumeCourse", backref="resume", lazy="selectin")
    achievements = db.relationship("ResumeAchievement", backref="resume", lazy="selectin")



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

class ResumeEducation(db.Model):
    __tablename__ = 'resume_education'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    education_id = db.Column(db.Integer, db.ForeignKey('education.id'), nullable=False)

    order = db.Column(db.Integer, default=0)

    education = db.relationship("Education", lazy="joined")

class ResumeProject(db.Model):
    __tablename__ = 'resume_project'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    project = db.relationship("Project", lazy="joined")

class ResumeCertification(db.Model):
    __tablename__ = 'resume_certification'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    certification_id = db.Column(db.Integer, db.ForeignKey('certification.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    certification = db.relationship("Certification", lazy="joined")

class ResumeCourse(db.Model):
    __tablename__ = 'resume_course'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    course = db.relationship("Course", lazy="joined")

class ResumeAchievement(db.Model):
    __tablename__ = 'resume_achievement'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    achievement = db.relationship("Achievement", lazy="joined")