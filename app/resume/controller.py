from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from .service import ResumeService
from .schema import (
    ResumeCreateSchema, 
    AddExperienceSchema, 
    AddSkillSchema, 
    ReorderSchema,
    UpdateResumeSchema
)

class ResumeController:

    @staticmethod
    def create_resume():
        user_id = int(get_jwt_identity())
        data = request.get_json()

        errors = ResumeCreateSchema().validate(data)
        if errors:
            return jsonify({"status": "error", "errors": errors}), 400
        response, status = ResumeService.create_resume(user_id, data)
        return jsonify(response), status
    

    @staticmethod
    def get_resume(resume_id):
        user_id = int(get_jwt_identity())
        response, status = ResumeService.get_resume(user_id, resume_id)

        # since the response has resume (non-serialised), we need to serialised it, if no errors
        if status != 200:
            return jsonify(response), status # in that case response has error message
        
        return jsonify({
            "id": response.id,
            "title": response.title,
            "summary": response.summary,

            "experiences": [
                {
                    "id": assoc.experience.id,
                    "company": assoc.experience.company,
                    "role": assoc.experience.role,
                    "start_date": assoc.experience.start_date.strftime("%Y-%m-%d"),
                    "end_date": assoc.experience.end_date.strftime("%Y-%m-%d") if assoc.experience.end_date else "Present",
                    "order": assoc.order
                } for assoc in sorted(response.experiences, key=lambda x: x.order)
                # looping through the items in the joint list
            ],

            "skills": [
                {
                    "id": assoc.skill.id,
                    "name": assoc.skill.name,
                    "order": assoc.order
                } for assoc in sorted(response.skills, key=lambda x: x.order)
            ]
        }), 200


    @staticmethod
    def add_experience_to_resume(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json() # will contain exp id, and order which user indirectly sets

        errors = AddExperienceSchema().validate(data)
        if errors: return jsonify({"status": "error", "errors": errors}), 400

        # since user chooses an exp from frontend hence it comes as request body only, same with order
        response, status = ResumeService.add_experience_to_resume(
            user_id, resume_id, data["experience_id"], data["order"]
        )
        return jsonify(response), status


    @staticmethod
    def reorder_experiences(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()

        errors = ReorderSchema().validate(data) # check if given data is an integer list
        if errors: return jsonify({"status": "error", "errors": errors}), 400

        response, status = ResumeService.reorder_experiences(
            user_id, resume_id, data["ordered_ids"]
        )
        return jsonify(response),status


    @staticmethod
    def remove_experience_from_resume(resume_id, experience_id):
        user_id = int(get_jwt_identity())

        response, status = ResumeService.remove_experience_from_resume(
            user_id, resume_id, experience_id
        ) 
        return jsonify(response), status
    

    @staticmethod
    def add_skill_to_resume(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()

        errors = AddSkillSchema().validate(data)
        if errors: return jsonify({"status": "error", "errors": errors}), 400

        response, status = ResumeService.add_skill_to_resume(user_id, resume_id, data["skill_id"], data["order"])
        return jsonify(response), status
    

    @staticmethod
    def reorder_skills(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()

        errors = ReorderSchema().validate(data)
        if errors: return jsonify({"status": "error", "errors": errors}), 400

        response, status = ResumeService.reorder_skills(user_id, resume_id, data["ordered_ids"])
        return jsonify(response), status
    

    @staticmethod
    def remove_skill_from_resume(resume_id, skill_id):
        user_id = int(get_jwt_identity())

        response, status = ResumeService.remove_skill_from_resume(
            user_id, resume_id, skill_id
        ) 
        return jsonify(response), status
    
    @staticmethod
    def update_resume(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400

        errors = UpdateResumeSchema().validate(data)
        if errors: return {"status":"error", "errors":errors}, 400

        response, status = ResumeService.update_resume(user_id, resume_id, data)
        return jsonify(response), status