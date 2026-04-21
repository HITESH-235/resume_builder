from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity 
from .schema import ExperienceSchema, ExperienceUpdateSchema, ProfileUpdateSchema, SkillSchema, EducationSchema, EducationUpdateSchema, ProjectSchema, CertificationSchema, CourseSchema, AchievementSchema
from .service import ProfileService


class ProfileController:

# ------------------------------------------------------------------------------------
    # PROFILE methods:
    @staticmethod
    def get_profile():
        user_id = int(get_jwt_identity())

        response, status = ProfileService.get_profile(user_id)
        return jsonify(response), status

    @staticmethod
    def update_profile():
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        
        errors = ProfileUpdateSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        
        response, status = ProfileService.update_profile(user_id, data)
        return jsonify(response), status


# ------------------------------------------------------------------------------------
    # SKILLS methods: (no get for skills)
    @staticmethod
    def add_skills():
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400

        errors = SkillSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400

        response,status = ProfileService.add_skills(user_id, data)
        return jsonify(response), status

    @staticmethod
    def delete_skill(skill_id):
        user_id = int(get_jwt_identity())
        response, status = ProfileService.delete_skill(user_id, skill_id)
        return jsonify(response), status


# ------------------------------------------------------------------------------------
    # EXPERIENCE methods:
    @staticmethod
    def add_experience():
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400

        errors = ExperienceSchema().validate(data) # from schema with marshmallow used
        if errors: return jsonify({"status":"error", "errors":errors}), 400

        response, status = ProfileService.add_experience(user_id, data)
        return jsonify(response), status

    @staticmethod
    def get_experience():
        user_id = int(get_jwt_identity())
        response, status = ProfileService.get_user_experience(user_id)
        return jsonify(response), status
    
    @staticmethod
    def update_experience(exp_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400

        errors = ExperienceUpdateSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400

        response, status = ProfileService.update_experience(user_id, exp_id, data)
        return jsonify(response), status

    @staticmethod
    def delete_experience(exp_id):
        user_id = int(get_jwt_identity())
        response, status = ProfileService.delete_experience(user_id, exp_id)
        return jsonify(response), status


# ------------------------------------------------------------------------------------
    # EDUCATION methods:
    @staticmethod
    def add_education():
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400

        errors = EducationSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400

        response, status = ProfileService.add_education(user_id, data)
        return jsonify(response), status

    @staticmethod
    def get_education():
        user_id = int(get_jwt_identity())
        response, status = ProfileService.get_user_education(user_id)
        return jsonify(response), status
    
    @staticmethod
    def update_education(edu_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400

        errors = EducationUpdateSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400

        response, status = ProfileService.update_education(user_id, edu_id, data)
        return jsonify(response), status

    @staticmethod
    def delete_education(edu_id):
        user_id = int(get_jwt_identity())
        response, status = ProfileService.delete_education(user_id, edu_id)
        return jsonify(response), status


# ------------------------------------------------------------------------------------
    # PROJECT methods:
    @staticmethod
    def add_project():
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = ProjectSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        clean = ProjectSchema().load(data)
        response, status = ProfileService.add_project(user_id, clean)
        return jsonify(response), status

    @staticmethod
    def get_project():
        user_id = int(get_jwt_identity())
        response, status = ProfileService.get_user_project(user_id)
        return jsonify(response), status
    
    @staticmethod
    def update_project(item_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = ProjectSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        response, status = ProfileService.update_project(user_id, item_id, data)
        return jsonify(response), status

    @staticmethod
    def delete_project(item_id):
        user_id = int(get_jwt_identity())
        response, status = ProfileService.delete_project(user_id, item_id)
        return jsonify(response), status


# ------------------------------------------------------------------------------------
    # CERTIFICATION methods:
    @staticmethod
    def add_certification():
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = CertificationSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        clean = CertificationSchema().load(data)
        response, status = ProfileService.add_certification(user_id, clean)
        return jsonify(response), status

    @staticmethod
    def get_certification():
        user_id = int(get_jwt_identity())
        response, status = ProfileService.get_user_certification(user_id)
        return jsonify(response), status
    
    @staticmethod
    def update_certification(item_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = CertificationSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        response, status = ProfileService.update_certification(user_id, item_id, data)
        return jsonify(response), status

    @staticmethod
    def delete_certification(item_id):
        user_id = int(get_jwt_identity())
        response, status = ProfileService.delete_certification(user_id, item_id)
        return jsonify(response), status


# ------------------------------------------------------------------------------------
    # COURSE methods:
    @staticmethod
    def add_course():
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = CourseSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        clean = CourseSchema().load(data)
        response, status = ProfileService.add_course(user_id, clean)
        return jsonify(response), status

    @staticmethod
    def get_course():
        user_id = int(get_jwt_identity())
        response, status = ProfileService.get_user_course(user_id)
        return jsonify(response), status
    
    @staticmethod
    def update_course(item_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = CourseSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        response, status = ProfileService.update_course(user_id, item_id, data)
        return jsonify(response), status

    @staticmethod
    def delete_course(item_id):
        user_id = int(get_jwt_identity())
        response, status = ProfileService.delete_course(user_id, item_id)
        return jsonify(response), status


# ------------------------------------------------------------------------------------
    # ACHIEVEMENT methods:
    @staticmethod
    def add_achievement():
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = AchievementSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        clean = AchievementSchema().load(data)
        response, status = ProfileService.add_achievement(user_id, clean)
        return jsonify(response), status

    @staticmethod
    def get_achievement():
        user_id = int(get_jwt_identity())
        response, status = ProfileService.get_user_achievement(user_id)
        return jsonify(response), status
    
    @staticmethod
    def update_achievement(item_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400
        errors = AchievementSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        response, status = ProfileService.update_achievement(user_id, item_id, data)
        return jsonify(response), status

    @staticmethod
    def delete_achievement(item_id):
        user_id = int(get_jwt_identity())
        response, status = ProfileService.delete_achievement(user_id, item_id)
        return jsonify(response), status