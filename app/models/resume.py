from app.extensions.db import db
from datetime import datetime, timezone

class Resume(db.Model):
    __tablename__ = "resume"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
        index=True
    )

    # all resume specific fields:
    title = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=True)
    summary = db.Column(db.Text)
    designation = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    website_label = db.Column(db.String(100), nullable=True)

    active_sections = db.Column(db.JSON, nullable=True)
    layout_config = db.Column(db.JSON, nullable=True) 

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    skills = db.relationship("ResumeSkill", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    experiences = db.relationship("ResumeExperience", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    educations = db.relationship("ResumeEducation", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    projects = db.relationship("ResumeProject", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    certifications = db.relationship("ResumeCertification", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    courses = db.relationship("ResumeCourse", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    achievements = db.relationship("ResumeAchievement", backref="resume", lazy="selectin", cascade="all, delete-orphan")
    custom_items = db.relationship("ResumeCustomItem", backref="resume", lazy="selectin", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super(Resume, self).__init__(**kwargs)


class ResumeSkill(db.Model):
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey("skill.id"), primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    skill = db.relationship("Skill", backref="resume_links")

    def __init__(self, **kwargs):
        super(ResumeSkill, self).__init__(**kwargs)


class ResumeExperience(db.Model):
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), primary_key=True)
    experience_id = db.Column(db.Integer, db.ForeignKey("experience.id"), primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    experience = db.relationship("Experience", backref="resume_links")

    def __init__(self, **kwargs):
        super(ResumeExperience, self).__init__(**kwargs)


class ResumeEducation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    education_id = db.Column(db.Integer, db.ForeignKey('education.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    education = db.relationship("Education", lazy="joined")

    def __init__(self, **kwargs):
        super(ResumeEducation, self).__init__(**kwargs)


class ResumeProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    project = db.relationship("Project", lazy="joined")

    def __init__(self, **kwargs):
        super(ResumeProject, self).__init__(**kwargs)


class ResumeCertification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    certification_id = db.Column(db.Integer, db.ForeignKey('certification.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    certification = db.relationship("Certification", lazy="joined")

    def __init__(self, **kwargs):
        super(ResumeCertification, self).__init__(**kwargs)


class ResumeCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    course = db.relationship("Course", lazy="joined")

    def __init__(self, **kwargs):
        super(ResumeCourse, self).__init__(**kwargs)


class ResumeAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    achievement = db.relationship("Achievement", lazy="joined")

    def __init__(self, **kwargs):
        super(ResumeAchievement, self).__init__(**kwargs)


class ResumeCustomItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    custom_item_id = db.Column(db.Integer, db.ForeignKey('custom_item.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    custom_item = db.relationship("CustomItem", lazy="joined")

    def __init__(self, **kwargs):
        super(ResumeCustomItem, self).__init__(**kwargs)