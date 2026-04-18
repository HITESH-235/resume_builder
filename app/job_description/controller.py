from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from .service import JobDescriptionService
from .schema import JobDescriptionSchema

class JobDescriptionController:

    @staticmethod
    def create_jd(): # create a new job description for the user
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data: return jsonify({"error": "Invalid JSON"}), 400

        errors = JobDescriptionSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400

        response, status = JobDescriptionService.create_jd(user_id, data)
        return jsonify(response), status
    

    @staticmethod
    def get_jds(): # get list of all job descriptions the user added (with their title and content)
        user_id = int(get_jwt_identity())

        response, status = JobDescriptionService.get_jds(user_id)
        return jsonify(response), status