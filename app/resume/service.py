from app.extensions.db import db
from app.models import User, Resume, Experience, Skill, ResumeSkill, ResumeExperience, Education, ResumeEducation, Project, ResumeProject, Certification, ResumeCertification, Course, ResumeCourse, Achievement, ResumeAchievement, ResumeCustomItem, CustomItem


class ResumeService:

# -------------------------------------------------------------------------------------------------------
    # RESUME general functions:

    @staticmethod
    def create_resume(user_id, data):
        new_resume = Resume(
            user_id=user_id,
            title=data.get('title'),
            name=data.get('name'),
            summary=data.get('summary'),
            designation=data.get('designation'),
            email=data.get('email'),
            phone=data.get('phone'),
            location=data.get('location'),
            active_sections=data.get('active_sections'),
            layout_config=data.get('layout_config')
        )
        db.session.add(new_resume)
        db.session.commit()
        return {"message": "Resume created successfully", "resume_id": new_resume.id}, 201

    @staticmethod
    def get_all_resumes(user_id):
        resumes = Resume.query.filter_by(user_id=user_id).all()
        return {
            "resumes": [
                {
                    "id": r.id, 
                    "title": r.title, 
                    "name": r.name,
                    "updated_at": r.updated_at.isoformat()
                } for r in resumes
            ]
        }, 200

    @staticmethod
    def get_resume(user_id, resume_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume:
            return {"error": "Resume not found"}, 404
        return resume, 200

    @staticmethod
    def update_resume(user_id, resume_id, data):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume:
            return {"error": "Resume not found"}, 404

        # Update core fields if provided
        for field in ['title', 'name', 'summary', 'designation', 'email', 'phone', 'location', 'active_sections', 'layout_config']:
            if field in data:
                setattr(resume, field, data[field])

        db.session.commit()
        return {"message": "Resume updated successfully"}, 200

    @staticmethod
    def delete_resume(user_id, resume_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume:
            return {"error": "Resume not found"}, 404
        db.session.delete(resume)
        db.session.commit()
        return {"message": "Resume deleted successfully"}, 200

    @staticmethod
    def duplicate_resume(user_id, resume_id):
        original = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not original:
            return {"error": "Resume not found"}, 404

        copy = Resume(
            user_id=user_id,
            title=f"Copy of {original.title}",
            name=original.name,
            summary=original.summary,
            designation=original.designation,
            email=original.email,
            phone=original.phone,
            location=original.location,
            active_sections=original.active_sections,
            layout_config=original.layout_config
        )
        db.session.add(copy)
        db.session.flush()

        # Copy all associations
        for assoc in original.skills:
            db.session.add(ResumeSkill(resume_id=copy.id, skill_id=assoc.skill_id, order=assoc.order))
        for assoc in original.experiences:
            db.session.add(ResumeExperience(resume_id=copy.id, experience_id=assoc.experience_id, order=assoc.order))
        for assoc in original.educations:
            db.session.add(ResumeEducation(resume_id=copy.id, education_id=assoc.education_id, order=assoc.order))
        for assoc in original.projects:
            db.session.add(ResumeProject(resume_id=copy.id, project_id=assoc.project_id, order=assoc.order))
        for assoc in original.certifications:
            db.session.add(ResumeCertification(resume_id=copy.id, certification_id=assoc.certification_id, order=assoc.order))
        for assoc in original.courses:
            db.session.add(ResumeCourse(resume_id=copy.id, course_id=assoc.course_id, order=assoc.order))
        for assoc in original.achievements:
            db.session.add(ResumeAchievement(resume_id=copy.id, achievement_id=assoc.achievement_id, order=assoc.order))
        for assoc in original.custom_items:
            db.session.add(ResumeCustomItem(resume_id=copy.id, custom_item_id=assoc.custom_item_id, order=assoc.order))

        db.session.commit()
        return {"message":"Resume duplicated", "resume_id": copy.id}, 201


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Skills from resume:

    @staticmethod
    def add_skill_to_resume(user_id, resume_id, skill_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        skill = Skill.query.get(skill_id)
        if not skill: return {"error": "Skill not found"}, 404

        existing = ResumeSkill.query.filter_by(resume_id=resume_id, skill_id=skill_id).first()
        if existing: return {"error": "Skill already added to resume"}, 400

        max_order = db.session.query(db.func.max(ResumeSkill.order)).filter_by(resume_id=resume_id).scalar()
        next_order = (max_order or 0) + 1

        new_assoc = ResumeSkill(resume_id=resume_id, skill_id=skill_id, order=next_order)
        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Skill added to resume"}, 201

    @staticmethod
    def remove_skill_from_resume(user_id, resume_id, skill_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeSkill.query.filter_by(resume_id=resume_id, skill_id=skill_id).first()
        if not assoc: return {"error": "Skill not in resume"}, 404

        removed_order = assoc.order
        db.session.delete(assoc)
        db.session.flush()

        # Update orders of remaining skills
        remaining = ResumeSkill.query.filter_by(resume_id=resume_id).all()
        for s in remaining:
            if s.order > removed_order:
                s.order -= 1

        db.session.commit()
        return {"message": "Skill removed from resume"}, 200

    @staticmethod
    def reorder_skills(user_id, resume_id, ordered_ids):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        skills = ResumeSkill.query.filter_by(resume_id=resume_id).all()
        
        # Temporarily offset to avoid unique constraint collisions
        for s in skills:
            s.order += 10000
        db.session.flush()

        id_to_skill = {s.skill_id: s for s in skills}
        for index, s_id in enumerate(ordered_ids):
            if s_id in id_to_skill:
                id_to_skill[s_id].order = index + 1

        db.session.commit()
        return {"message": "Skills reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Experience from resume:

    @staticmethod
    def add_experience_to_resume(user_id, resume_id, experience_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        exp = Experience.query.get(experience_id)
        if not exp: return {"error": "Experience not found"}, 404

        existing = ResumeExperience.query.filter_by(resume_id=resume_id, experience_id=experience_id).first()
        if existing: return {"error": "Experience already added"}, 400

        max_order = db.session.query(db.func.max(ResumeExperience.order)).filter_by(resume_id=resume_id).scalar()
        next_order = (max_order or 0) + 1

        new_assoc = ResumeExperience(resume_id=resume_id, experience_id=experience_id, order=next_order)
        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Experience added to resume"}, 201

    @staticmethod
    def remove_experience_from_resume(user_id, resume_id, experience_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeExperience.query.filter_by(resume_id=resume_id, experience_id=experience_id).first()
        if not assoc: return {"error": "Experience not in resume"}, 404

        removed_order = assoc.order
        db.session.delete(assoc)
        db.session.flush()

        remaining = ResumeExperience.query.filter_by(resume_id=resume_id).all()
        for item in remaining:
            if item.order > removed_order:
                item.order -= 1

        db.session.commit()
        return {"message": "Experience removed from resume"}, 200

    @staticmethod
    def reorder_experiences(user_id, resume_id, ordered_ids):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        exps = ResumeExperience.query.filter_by(resume_id=resume_id).all()

        # Offset to avoid collisions
        for e in exps:
            e.order += 10000
        db.session.flush()

        id_to_exp = {e.experience_id: e for e in exps}
        for index, e_id in enumerate(ordered_ids):
            if e_id in id_to_exp:
                id_to_exp[e_id].order = index + 1

        db.session.commit()
        return {"message": "Experiences reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Education from resume:

    @staticmethod
    def add_education_to_resume(user_id, resume_id, education_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        edu = Education.query.get(education_id)
        if not edu: return {"error": "Education not found"}, 404

        existing = ResumeEducation.query.filter_by(resume_id=resume_id, education_id=education_id).first()
        if existing: return {"error": "Education already added"}, 400

        max_order = db.session.query(db.func.max(ResumeEducation.order)).filter_by(resume_id=resume_id).scalar()
        next_order = (max_order or 0) + 1

        new_assoc = ResumeEducation(resume_id=resume_id, education_id=education_id, order=next_order)
        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Education added to resume"}, 201

    @staticmethod
    def remove_education_from_resume(user_id, resume_id, education_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeEducation.query.filter_by(resume_id=resume_id, education_id=education_id).first()
        if not assoc: return {"error": "Education not in resume"}, 404

        removed_order = assoc.order
        db.session.delete(assoc)
        db.session.flush()

        remaining = ResumeEducation.query.filter_by(resume_id=resume_id).all()
        for item in remaining:
            if item.order > removed_order:
                item.order -= 1

        db.session.commit()
        return {"message": "Education removed from resume"}, 200

    @staticmethod
    def reorder_educations(user_id, resume_id, ordered_ids):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        edus = ResumeEducation.query.filter_by(resume_id=resume_id).all()

        for e in edus:
            e.order += 10000
        db.session.flush()

        id_to_edu = {e.education_id: e for e in edus}
        for index, e_id in enumerate(ordered_ids):
            if e_id in id_to_edu:
                id_to_edu[e_id].order = index + 1

        db.session.commit()
        return {"message": "Educations reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Project from resume:

    @staticmethod
    def add_project_to_resume(user_id, resume_id, project_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        project = Project.query.get(project_id)
        if not project: return {"error": "Project not found"}, 404

        existing = ResumeProject.query.filter_by(resume_id=resume_id, project_id=project_id).first()
        if existing: return {"error": "Project already added"}, 400

        max_order = db.session.query(db.func.max(ResumeProject.order)).filter_by(resume_id=resume_id).scalar()
        next_order = (max_order or 0) + 1

        new_assoc = ResumeProject(resume_id=resume_id, project_id=project_id, order=next_order)
        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Project added to resume"}, 201

    @staticmethod
    def remove_project_from_resume(user_id, resume_id, project_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeProject.query.filter_by(resume_id=resume_id, project_id=project_id).first()
        if not assoc: return {"error": "Project not in resume"}, 404

        removed_order = assoc.order
        db.session.delete(assoc)
        db.session.flush()

        remaining = ResumeProject.query.filter_by(resume_id=resume_id).all()
        for item in remaining:
            if item.order > removed_order:
                item.order -= 1

        db.session.commit()
        return {"message": "Project removed from resume"}, 200

    @staticmethod
    def reorder_projects(user_id, resume_id, ordered_ids):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        projects = ResumeProject.query.filter_by(resume_id=resume_id).all()

        for p in projects:
            p.order += 10000
        db.session.flush()

        id_to_proj = {p.project_id: p for p in projects}
        for index, p_id in enumerate(ordered_ids):
            if p_id in id_to_proj:
                id_to_proj[p_id].order = index + 1

        db.session.commit()
        return {"message": "Projects reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Certification from resume:

    @staticmethod
    def add_certification_to_resume(user_id, resume_id, certification_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        cert = Certification.query.get(certification_id)
        if not cert: return {"error": "Certification not found"}, 404

        existing = ResumeCertification.query.filter_by(resume_id=resume_id, certification_id=certification_id).first()
        if existing: return {"error": "Certification already added"}, 400

        max_order = db.session.query(db.func.max(ResumeCertification.order)).filter_by(resume_id=resume_id).scalar()
        next_order = (max_order or 0) + 1

        new_assoc = ResumeCertification(resume_id=resume_id, certification_id=certification_id, order=next_order)
        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Certification added to resume"}, 201

    @staticmethod
    def remove_certification_from_resume(user_id, resume_id, certification_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeCertification.query.filter_by(resume_id=resume_id, certification_id=certification_id).first()
        if not assoc: return {"error": "Certification not in resume"}, 404

        removed_order = assoc.order
        db.session.delete(assoc)
        db.session.flush()

        remaining = ResumeCertification.query.filter_by(resume_id=resume_id).all()
        for item in remaining:
            if item.order > removed_order:
                item.order -= 1

        db.session.commit()
        return {"message": "Certification removed from resume"}, 200

    @staticmethod
    def reorder_certifications(user_id, resume_id, ordered_ids):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        certs = ResumeCertification.query.filter_by(resume_id=resume_id).all()
        
        # Safe offset
        for c in certs:
            c.order += 10000
        db.session.flush()

        id_to_cert = {c.certification_id: c for c in certs}

        for index, c_id in enumerate(ordered_ids):
            if c_id in id_to_cert:
                id_to_cert[c_id].order = index + 1

        db.session.commit()
        return {"message": "Certifications reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Course from resume:

    @staticmethod
    def add_course_to_resume(user_id, resume_id, course_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        course = Course.query.get(course_id)
        if not course: return {"error": "Course not found"}, 404

        existing = ResumeCourse.query.filter_by(resume_id=resume_id, course_id=course_id).first()
        if existing: return {"error": "Course already added"}, 400

        max_order = db.session.query(db.func.max(ResumeCourse.order)).filter_by(resume_id=resume_id).scalar()
        next_order = (max_order or 0) + 1

        new_assoc = ResumeCourse(resume_id=resume_id, course_id=course_id, order=next_order)
        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Course added to resume"}, 201

    @staticmethod
    def remove_course_from_resume(user_id, resume_id, course_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeCourse.query.filter_by(resume_id=resume_id, course_id=course_id).first()
        if not assoc: return {"error": "Course not in resume"}, 404

        removed_order = assoc.order
        db.session.delete(assoc)
        db.session.flush()

        remaining = ResumeCourse.query.filter_by(resume_id=resume_id).all()
        for item in remaining:
            if item.order > removed_order:
                item.order -= 1

        db.session.commit()
        return {"message": "Course removed from resume"}, 200

    @staticmethod
    def reorder_courses(user_id, resume_id, ordered_ids):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        courses = ResumeCourse.query.filter_by(resume_id=resume_id).all()
        
        # Safe offset
        for c in courses:
            c.order += 10000
        db.session.flush()

        id_to_course = {c.course_id: c for c in courses}

        for index, c_id in enumerate(ordered_ids):
            if c_id in id_to_course:
                id_to_course[c_id].order = index + 1

        db.session.commit()
        return {"message": "Courses reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Achievement from resume:

    @staticmethod
    def add_achievement_to_resume(user_id, resume_id, achievement_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        achievement = Achievement.query.get(achievement_id)
        if not achievement: return {"error": "Achievement not found"}, 404

        existing = ResumeAchievement.query.filter_by(resume_id=resume_id, achievement_id=achievement_id).first()
        if existing: return {"error": "Achievement already added"}, 400

        max_order = db.session.query(db.func.max(ResumeAchievement.order)).filter_by(resume_id=resume_id).scalar()
        next_order = (max_order or 0) + 1

        new_assoc = ResumeAchievement(resume_id=resume_id, achievement_id=achievement_id, order=next_order)
        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Achievement added to resume"}, 201

    @staticmethod
    def remove_achievement_from_resume(user_id, resume_id, achievement_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeAchievement.query.filter_by(resume_id=resume_id, achievement_id=achievement_id).first()
        if not assoc: return {"error": "Achievement not in resume"}, 404

        removed_order = assoc.order
        db.session.delete(assoc)
        db.session.flush()

        remaining = ResumeAchievement.query.filter_by(resume_id=resume_id).all()
        for item in remaining:
            if item.order > removed_order:
                item.order -= 1

        db.session.commit()
        return {"message": "Achievement removed from resume"}, 200

    @staticmethod
    def reorder_achievements(user_id, resume_id, ordered_ids):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        achievements = ResumeAchievement.query.filter_by(resume_id=resume_id).all()
        
        # Safe offset
        for a in achievements:
            a.order += 10000
        db.session.flush()

        id_to_assoc = {a.achievement_id: a for a in achievements}

        for index, a_id in enumerate(ordered_ids):
            if a_id in id_to_assoc:
                id_to_assoc[a_id].order = index + 1

        db.session.commit()
        return {"message": "Achievements reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Custom-Item from resume:

    @staticmethod
    def add_custom_item_to_resume(user_id, resume_id, custom_item_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        custom_item = CustomItem.query.get(custom_item_id)
        if not custom_item: return {"error": "Custom item not found"}, 404

        existing = ResumeCustomItem.query.filter_by(resume_id=resume_id, custom_item_id=custom_item_id).first()
        if existing: return {"error": "Custom item already added"}, 400

        max_order = db.session.query(db.func.max(ResumeCustomItem.order)).filter_by(resume_id=resume_id).scalar()
        next_order = (max_order or 0) + 1

        new_assoc = ResumeCustomItem(resume_id=resume_id, custom_item_id=custom_item_id, order=next_order)
        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Custom item added to resume"}, 201

    @staticmethod
    def remove_custom_item_from_resume(user_id, resume_id, custom_item_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeCustomItem.query.filter_by(resume_id=resume_id, custom_item_id=custom_item_id).first()
        if not assoc: return {"error": "Custom item not in resume"}, 404

        removed_order = assoc.order
        db.session.delete(assoc)
        db.session.flush()

        remaining = ResumeCustomItem.query.filter_by(resume_id=resume_id).all()
        for item in remaining:
            if item.order > removed_order:
                item.order -= 1

        db.session.commit()
        return {"message": "Custom item removed from resume"}, 200

    @staticmethod
    def reorder_custom_items(user_id, resume_id, ordered_ids):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assocs = ResumeCustomItem.query.filter_by(resume_id=resume_id).all()
        
        # Safe offset
        for a in assocs:
            a.order += 10000
        db.session.flush()

        id_to_assoc = {a.custom_item_id: a for a in assocs}

        for index, item_id in enumerate(ordered_ids):
            if item_id in id_to_assoc:
                id_to_assoc[item_id].order = index + 1

        db.session.commit()
        return {"message": "Custom items reordered"}, 200