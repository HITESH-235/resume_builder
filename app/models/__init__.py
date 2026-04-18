from app.extensions.db import db

# import models so SQLAlchemy registers them (so db knows its correct)
from .user import User
from .profile import Profile, profile_skills
from .experience import Experience
from .skill import Skill
from .job_description import JobDescription