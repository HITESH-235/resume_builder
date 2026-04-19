from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from .service import ResumeService
from .schema import (
    ResumeCreateSchema, 
    AddExperienceSchema, 
    AddSkillSchema, 
    AddEducationSchema,
    AddProjectSchema,
    AddCertificationSchema,
    AddCourseSchema,
    AddAchievementSchema,
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
    def get_all_resumes():
        user_id = int(get_jwt_identity())
        response, status = ResumeService.get_all_resumes(user_id)
        return jsonify(response), status

    @staticmethod
    def delete_resume(resume_id):
        user_id = int(get_jwt_identity())
        response, status = ResumeService.delete_resume(user_id, resume_id)
        return jsonify(response), status

    @staticmethod
    def duplicate_resume(resume_id):
        user_id = int(get_jwt_identity())
        response, status = ResumeService.duplicate_resume(user_id, resume_id)
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
            "name": response.name,
            "summary": response.summary,
            "designation": response.designation,
            "email": response.email,
            "phone": response.phone,
            "location": response.location,

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
            ],

            "educations": [
                {
                    "id": assoc.education.id,
                    "institution": assoc.education.institution,
                    "degree": assoc.education.degree,
                    "description": assoc.education.description,
                    "start_date": assoc.education.start_date.strftime("%Y-%m-%d"),
                    "end_date": assoc.education.end_date.strftime("%Y-%m-%d") if assoc.education.end_date else "Present",
                    "order": assoc.order
                } for assoc in sorted(response.educations, key=lambda x: x.order)
            ],

            "projects": [
                {
                    "id": assoc.project.id,
                    "name": assoc.project.name,
                    "role": assoc.project.role,
                    "description": assoc.project.description,
                    "link": assoc.project.link,
                    "start_date": assoc.project.start_date.strftime("%Y-%m-%d"),
                    "end_date": assoc.project.end_date.strftime("%Y-%m-%d") if assoc.project.end_date else "Present",
                    "order": assoc.order
                } for assoc in sorted(response.projects, key=lambda x: x.order)
            ],

            "certifications": [
                {
                    "id": assoc.certification.id,
                    "name": assoc.certification.name,
                    "issuer": assoc.certification.issuer,
                    "url": assoc.certification.url,
                    "date": assoc.certification.date.strftime("%Y-%m-%d"),
                    "order": assoc.order
                } for assoc in sorted(response.certifications, key=lambda x: x.order)
            ],

            "courses": [
                {
                    "id": assoc.course.id,
                    "name": assoc.course.name,
                    "institution": assoc.course.institution,
                    "date": assoc.course.date.strftime("%Y-%m-%d"),
                    "order": assoc.order
                } for assoc in sorted(response.courses, key=lambda x: x.order)
            ],

            "achievements": [
                {
                    "id": assoc.achievement.id,
                    "title": assoc.achievement.title,
                    "description": assoc.achievement.description,
                    "date": assoc.achievement.date.strftime("%Y-%m-%d"),
                    "order": assoc.order
                } for assoc in sorted(response.achievements, key=lambda x: x.order)
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
    def add_education_to_resume(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()

        errors = AddEducationSchema().validate(data)
        if errors: return jsonify({"status": "error", "errors": errors}), 400

        response, status = ResumeService.add_education_to_resume(user_id, resume_id, data["education_id"], data["order"])
        return jsonify(response), status
    
    @staticmethod
    def reorder_educations(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()

        errors = ReorderSchema().validate(data)
        if errors: return jsonify({"status": "error", "errors": errors}), 400

        response, status = ResumeService.reorder_educations(user_id, resume_id, data["ordered_ids"])
        return jsonify(response), status

    @staticmethod
    def remove_education_from_resume(resume_id, education_id):
        user_id = int(get_jwt_identity())

        response, status = ResumeService.remove_education_from_resume(
            user_id, resume_id, education_id
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
    @staticmethod
    def add_project(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = AddProjectSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        project_id = data.get('project_id')
        order = data.get('order')
        response, status = ResumeService.add_project_to_resume(user_id, resume_id, project_id, order)
        return jsonify(response), status

    @staticmethod
    def reorder_project(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = ReorderSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        order_data = data.get('order_data')
        response, status = ResumeService.reorder_projects(user_id, resume_id, order_data)
        return jsonify(response), status

    @staticmethod
    def remove_project(resume_id, project_id):
        user_id = int(get_jwt_identity())
        response, status = ResumeService.remove_project_from_resume(user_id, resume_id, project_id)
        return jsonify(response), status

    @staticmethod
    def add_certification(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = AddCertificationSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        certification_id = data.get('certification_id')
        order = data.get('order')
        response, status = ResumeService.add_certification_to_resume(user_id, resume_id, certification_id, order)
        return jsonify(response), status

    @staticmethod
    def reorder_certification(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = ReorderSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        order_data = data.get('order_data')
        response, status = ResumeService.reorder_certifications(user_id, resume_id, order_data)
        return jsonify(response), status

    @staticmethod
    def remove_certification(resume_id, certification_id):
        user_id = int(get_jwt_identity())
        response, status = ResumeService.remove_certification_from_resume(user_id, resume_id, certification_id)
        return jsonify(response), status

    @staticmethod
    def add_course(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = AddCourseSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        course_id = data.get('course_id')
        order = data.get('order')
        response, status = ResumeService.add_course_to_resume(user_id, resume_id, course_id, order)
        return jsonify(response), status

    @staticmethod
    def reorder_course(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = ReorderSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        order_data = data.get('order_data')
        response, status = ResumeService.reorder_courses(user_id, resume_id, order_data)
        return jsonify(response), status

    @staticmethod
    def remove_course(resume_id, course_id):
        user_id = int(get_jwt_identity())
        response, status = ResumeService.remove_course_from_resume(user_id, resume_id, course_id)
        return jsonify(response), status

    @staticmethod
    def add_achievement(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = AddAchievementSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        achievement_id = data.get('achievement_id')
        order = data.get('order')
        response, status = ResumeService.add_achievement_to_resume(user_id, resume_id, achievement_id, order)
        return jsonify(response), status

    @staticmethod
    def reorder_achievement(resume_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = ReorderSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        order_data = data.get('order_data')
        response, status = ResumeService.reorder_achievements(user_id, resume_id, order_data)
        return jsonify(response), status

    @staticmethod
    def remove_achievement(resume_id, achievement_id):
        user_id = int(get_jwt_identity())
        response, status = ResumeService.remove_achievement_from_resume(user_id, resume_id, achievement_id)
        return jsonify(response), status
