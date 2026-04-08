from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity 
from .schema import ExperienceSchema, ExperienceUpdateSchema, ProfileUpdateSchema
from .service import ProfileService


class ProfileController:

    @staticmethod
    def add_skills():
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return jsonify({"error":"Invalid JSON"}), 400
        
        response,status = ProfileService.add_skills(user_id, data)
        return jsonify(response), status



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
    
    @staticmethod
    def get_full_profile():
        user_id = int(get_jwt_identity())
        response, status = ProfileService.get_full_profile(user_id)
        return jsonify(response), status