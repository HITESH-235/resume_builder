from app.extensions.db import db
from app.models import User, Resume, Experience, Skill, ResumeSkill, ResumeExperience, Education, ResumeEducation, Project, ResumeProject, Certification, ResumeCertification, Course, ResumeCourse, Achievement, ResumeAchievement
from app.models.experience import Experience
from app.models.skill import Skill
from app.models.education import Education
from app.models.user import User


class ResumeService:

# -------------------------------------------------------------------------------------------------------
    # CREATE/FETCH/UPDATE/DELETE (basic resume info):

    @staticmethod
    def create_resume(user_id, data):
        resume = Resume(
            user_id = user_id,
            title = data["title"],
            summary = data.get("summary")
        )
        db.session.add(resume)
        db.session.commit()
        return {"message":"Resume created", "resume_id":resume.id}, 201


    @staticmethod
    def get_resume(user_id, resume_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()

        if not resume: return {"error":"Resume not found"}, 404
        return resume, 200 # *needs to be serialised in controller*

    @staticmethod
    def get_all_resumes(user_id):
        resumes = Resume.query.filter_by(user_id=user_id).all()
        return [{"id": r.id, "title": r.title, "name": r.name, "summary": r.summary, "updated_at": r.updated_at} for r in resumes], 200

    @staticmethod
    def update_resume(user_id, resume_id, data):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error":"Resume not found"}, 404

        if "title" in data: resume.title = data["title"]
        if "name" in data: resume.name = data["name"]
        if "summary" in data: resume.summary = data["summary"]
        if "designation" in data: resume.designation = data["designation"]
        if "email" in data: resume.email = data["email"]
        if "phone" in data: resume.phone = data["phone"]
        if "location" in data: resume.location = data["location"]

        db.session.commit()
        return {"message":"Resume updated"}, 200

    @staticmethod
    def delete_resume(user_id, resume_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error":"Resume not found"}, 404
        db.session.delete(resume)
        db.session.commit()
        return {"message":"Resume deleted"}, 200

    @staticmethod
    def duplicate_resume(user_id, resume_id):
        original = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not original: return {"error":"Resume not found"}, 404

        copy = Resume(
            user_id=user_id,
            title=original.title,
            name=(original.name or original.title) + " (Copy)",
            summary=original.summary,
            designation=original.designation,
            email=original.email,
            phone=original.phone,
            location=original.location,
        )
        db.session.add(copy)
        db.session.flush()  # get copy.id

        # Duplicate all associations to form new associations
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

        db.session.commit()
        return {"message":"Resume duplicated", "resume_id": copy.id}, 201


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Skills from resume:

    @staticmethod # same logic as in add_experience_to_resume
    def add_skill_to_resume(user_id, resume_id, skill_id, order):
        # check resume exists
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error":"Resume not found"}, 404

        # check skill_id to be present in Skill table
        skill = Skill.query.get(skill_id)
        if not skill: return {"error":"Invalid skill"}, 400

        # new skill to be added should not be present with the same skill_id in the resume
        existing = ResumeSkill.query.filter_by(
            resume_id = resume_id,
            skill_id = skill_id
        ).first()
        if existing: return {"error":"Skill already added"}, 400

        # list of skills in the joint table for a given resume_id, sorted in order
        associations = ResumeSkill.query.filter_by(resume_id=resume_id).order_by(ResumeSkill.order).all()
        
        # making new skill's given order in-bound:
        if order < 0: order = 0
        if order > len(associations): order = len(associations) # put at end

        # shift the other orders by 1, that are affected by insertion:
        for assoc in associations: 
            if assoc.order >= order: assoc.order += 1
        
        # making the new row for the joint table
        new_assoc = ResumeSkill(
            resume_id = resume_id,
            skill_id = skill_id,
            order = order
        )

        db.session.add(new_assoc)
        db.session.commit()
        return {"message":"Skill added successfully"}, 201


    @staticmethod
    def remove_skill_from_resume(user_id, resume_id, skill_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeSkill.query.filter_by(
            skill_id = skill_id, 
            resume_id=resume_id
        ).first() # the single row from joint table rep. the experience to be deleted

        if not assoc: return {"error":"Skill not in resume"}, 404

        removed_order = assoc.order # decrement by 1 to all orders bigger than this

        db.session.delete(assoc)
        remaining = ResumeSkill.query.filter_by(resume_id=resume_id).all()
        for item in remaining:
            if item.order > removed_order: item.order -= 1

        db.session.commit()
        return {"message":"Skill removed"}, 200
        

    @staticmethod
    def reorder_skills(user_id, resume_id, ordered_skill_ids):
        # check if resume exists by id:
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error":"Resume not found"}, 404

        # list of skills in joint table
        associations = ResumeSkill.query.filter_by(
            resume_id=resume_id
        ).all()

        # check if current skill id list does contain all elements given in new ordered skill list
        existing_ids = {a.skill_id for a in associations}
        if set(ordered_skill_ids) != existing_ids:
            return {"error": "Invalid ordering set"}, 400

        # map for skill_id:item to link update order for each skill_id using the item
        id_to_assoc = {a.skill_id: a for a in associations}

        for assoc in associations:
            assoc.order += 1000
        db.session.flush()

        for new_order, skill_id in enumerate(ordered_skill_ids): # the index in give list rep. new order
            id_to_assoc[skill_id].order = new_order

        db.session.commit()
        return {"message": "Skills Reordered"}, 200
    

# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Experience from resume:

    @staticmethod
    def add_experience_to_resume(user_id, resume_id, experience_id, order):
        # check resume exists
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume:
            return {"error":"Resume not found"}, 404

        # check experience_id to be present in Experience table and linked to the same profile
        exp = Experience.query.get(experience_id)
        if not exp or exp.profile.user_id != user_id:
            return {"error":"Invalid experience"}, 400

        # new experience to be added should not be present with the same experience_id in the resume
        existing = ResumeExperience.query.filter_by(
            resume_id=resume_id,
            experience_id=experience_id
        ).first()
        if existing: return {"error":"Experience already added"}, 400

        # list of experiences in the joint table for a given resume_id, sorted in order
        associations = ResumeExperience.query.filter_by(resume_id=resume_id).order_by(ResumeExperience.order).all()

        # making the new give order in-bound
        if order < 0: order = 0 # will require shifting
        if order > len(associations): order = len(associations) # append then new exp at end

        # shift the other orders by 1, that are affected by insertion:
        for assoc in associations:
            if assoc.order >= order: assoc.order += 1

        # making the new row for the joint table
        new_assoc = ResumeExperience(resume_id=resume_id, experience_id=experience_id, order=order)
        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Experience added successfully"}, 201 # 201 is for successful additions


    @staticmethod
    def remove_experience_from_resume(user_id, resume_id, experience_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeExperience.query.filter_by(
            experience_id = experience_id, 
            resume_id=resume_id
        ).first() # the single row from joint table rep. the experience to be deleted

        if not assoc: return {"error":"Experience not in resume"}, 404

        removed_order = assoc.order # decrement by 1 to all orders bigger than this

        db.session.delete(assoc)
        remaining = ResumeExperience.query.filter_by(resume_id=resume_id).all()
        for item in remaining:
            if item.order > removed_order: item.order -= 1

        db.session.commit()
        return {"message":"Experience removed"}, 200


    @staticmethod
    def reorder_experiences(user_id, resume_id, ordered_experience_ids):
        # check if resume exists by id:
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error":"Resume not found"}, 404

        # list of experiences in joint table
        associations = ResumeExperience.query.filter_by(
            resume_id=resume_id
        ).all()

        # check if current experience id list does contain all elements given in new ordered experience list
        existing_ids = {a.experience_id for a in associations}
        if set(ordered_experience_ids) != existing_ids:
            return {"error": "Invalid ordering set"}, 400

        # map for experience_id:item to link update order for each experience_id using the item
        id_to_assoc = {a.experience_id: a for a in associations}

        for assoc in associations:
            assoc.order += 1000 # change all orders temporarily so that temporary duplicate pairs arent created while reordering
        db.session.flush()

        for new_order, exp_id in enumerate(ordered_experience_ids): # the index in give list rep. new order
            id_to_assoc[exp_id].order = new_order

        db.session.commit()
        return {"message": "Experiences reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Education from resume:
    
    @staticmethod
    def add_education_to_resume(user_id, resume_id, education_id, order):
        # check resume exists
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume:
            return {"error":"Resume not found"}, 404

        # check education_id to be present in Education table and linked to the same profile
        edu = Education.query.get(education_id)
        if not edu or edu.profile.user_id != user_id:
            return {"error":"Invalid education"}, 400

        # new education to be added should not be present with the same education_id in the resume
        existing = ResumeEducation.query.filter_by(
            resume_id=resume_id,
            education_id=education_id
        ).first()
        if existing: return {"error":"Education already added"}, 400

        # list of educations in the joint table for a given resume_id, sorted in order
        associations = ResumeEducation.query.filter_by(resume_id=resume_id).order_by(ResumeEducation.order).all()

        # making the new give order in-bound
        if order < 0: order = 0 # will require shifting
        if order > len(associations): order = len(associations) # append then new edu at end

        # shift the other orders by 1, that are affected by insertion:
        for assoc in associations:
            if assoc.order >= order: assoc.order += 1

        # making the new row for the joint table
        new_assoc = ResumeEducation(
            resume_id = resume_id,
            education_id = education_id,
            order = order
        )

        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Education added successfully"}, 201


    @staticmethod
    def remove_education_from_resume(user_id, resume_id, education_id):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        assoc = ResumeEducation.query.filter_by(
            education_id = education_id, 
            resume_id=resume_id
        ).first()

        if not assoc: return {"error":"Education not in resume"}, 404

        removed_order = assoc.order

        db.session.delete(assoc)
        remaining = ResumeEducation.query.filter_by(resume_id=resume_id).all()
        for item in remaining:
            if item.order > removed_order: item.order -= 1

        db.session.commit()
        return {"message":"Education removed"}, 200


    @staticmethod
    def reorder_educations(user_id, resume_id, ordered_education_ids):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error":"Resume not found"}, 404

        associations = ResumeEducation.query.filter_by(
            resume_id=resume_id
        ).all()

        existing_ids = {a.education_id for a in associations}
        if set(ordered_education_ids) != existing_ids:
            return {"error": "Invalid ordering set"}, 400

        id_to_assoc = {a.education_id: a for a in associations}

        for assoc in associations:
            assoc.order += 1000
        db.session.flush()

        for new_order, edu_id in enumerate(ordered_education_ids):
            id_to_assoc[edu_id].order = new_order

        db.session.commit()
        return {"message": "Educations reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Project from resume:

    @staticmethod
    def add_project_to_resume(user_id, resume_id, project_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        existing = ResumeProject.query.filter_by(resume_id=resume_id, project_id=project_id).first()
        if existing: return {"error": "Project already in resume"}, 400

        new_assoc = ResumeProject(resume_id=resume_id, project_id=project_id, order=order)
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

        associations = ResumeProject.query.filter_by(resume_id=resume_id).all()
        existing_ids = {a.project_id for a in associations}
        if set(ordered_ids) != existing_ids:
            return {"error": "Invalid ordering set"}, 400

        id_to_assoc = {a.project_id: a for a in associations}

        for assoc in associations:
            assoc.order += 1000
        db.session.flush()

        for new_order, p_id in enumerate(ordered_ids):
            id_to_assoc[p_id].order = new_order

        db.session.commit()
        return {"message": "Projects reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Certification from resume:

    @staticmethod
    def add_certification_to_resume(user_id, resume_id, certification_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        existing = ResumeCertification.query.filter_by(resume_id=resume_id, certification_id=certification_id).first()
        if existing: return {"error": "Certification already in resume"}, 400

        new_assoc = ResumeCertification(resume_id=resume_id, certification_id=certification_id, order=order)
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

        associations = ResumeCertification.query.filter_by(resume_id=resume_id).all()
        existing_ids = {a.certification_id for a in associations}
        if set(ordered_ids) != existing_ids:
            return {"error": "Invalid ordering set"}, 400

        id_to_assoc = {a.certification_id: a for a in associations}

        for assoc in associations:
            assoc.order += 1000
        db.session.flush()

        for new_order, cert_id in enumerate(ordered_ids):
            id_to_assoc[cert_id].order = new_order

        db.session.commit()
        return {"message": "Certifications reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Course from resume:

    @staticmethod
    def add_course_to_resume(user_id, resume_id, course_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        existing = ResumeCourse.query.filter_by(resume_id=resume_id, course_id=course_id).first()
        if existing: return {"error": "Course already in resume"}, 400

        new_assoc = ResumeCourse(resume_id=resume_id, course_id=course_id, order=order)
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

        associations = ResumeCourse.query.filter_by(resume_id=resume_id).all()
        existing_ids = {a.course_id for a in associations}
        if set(ordered_ids) != existing_ids:
            return {"error": "Invalid ordering set"}, 400

        id_to_assoc = {a.course_id: a for a in associations}

        for assoc in associations:
            assoc.order += 1000
        db.session.flush()

        for new_order, c_id in enumerate(ordered_ids):
            id_to_assoc[c_id].order = new_order

        db.session.commit()
        return {"message": "Courses reordered"}, 200


# -------------------------------------------------------------------------------------------------------
    # ADD/REMOVE/REORDER Achievement from resume:

    @staticmethod
    def add_achievement_to_resume(user_id, resume_id, achievement_id, order):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error": "Resume not found"}, 404

        existing = ResumeAchievement.query.filter_by(resume_id=resume_id, achievement_id=achievement_id).first()
        if existing: return {"error": "Achievement already in resume"}, 400

        new_assoc = ResumeAchievement(resume_id=resume_id, achievement_id=achievement_id, order=order)
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

        associations = ResumeAchievement.query.filter_by(resume_id=resume_id).all()
        existing_ids = {a.achievement_id for a in associations}
        if set(ordered_ids) != existing_ids:
            return {"error": "Invalid ordering set"}, 400

        id_to_assoc = {a.achievement_id: a for a in associations}

        for assoc in associations:
            assoc.order += 1000
        db.session.flush()

        for new_order, a_id in enumerate(ordered_ids):
            id_to_assoc[a_id].order = new_order

        db.session.commit()
        return {"message": "Achievements reordered"}, 200