from app.extensions.db import db
from app.models.resume import Resume, ResumeExperience, ResumeSkill
from app.models.experience import Experience
from app.models.skill import Skill
from app.models.user import User


class ResumeService:

    @staticmethod
    def create_resume(user_id, data):
        resume = Resume(
            user_id = user_id,
            title = data["title"],
            summary = data.get("summary") # since nullable is allowed
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
        new_assoc = ResumeExperience(
            resume_id = resume_id,
            experience_id = experience_id,
            order = order
        )

        db.session.add(new_assoc)
        db.session.commit()
        return {"message": "Experience added successfully"}, 201 # 201 is for successful additions


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
    def update_resume(user_id, resume_id, data):
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        if not resume: return {"error":"Resume not found"}, 404

        if "title" in data:
            resume.title = data["title"]
        if "summary" in data:
            resume.summary = data["summary"]

        db.session.commit()
        return {"message":"Resume updated"}, 200