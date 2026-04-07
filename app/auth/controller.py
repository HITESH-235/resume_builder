from flask import request, jsonify
from .service import AuthService
from .schema import UserRegistrationSchema, LoginSchema



class AuthController:

    @staticmethod
    def signup():
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400

        # A. using marshmallow in schemas (marshmallow requires instance to send error)
        errors = UserRegistrationSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
            
        # B. explicit version when picked from schemas:
        # errors2 = UserRegistration2.validate(data)
        # if errors2: # if errors dictionary is not empty
        #     return jsonify({"status":"error", "message":errors2}), 400

        # after error checking regardless of methods:
        response, status = AuthService.register_user(data)
        return jsonify(response), status


    @staticmethod
    def login():
        data = request.get_json()
        if not data: return jsonify({"error":"Invalid JSON"}), 400

        errors = LoginSchema().validate(data)
        if errors: return jsonify({"status":"error", "errors":errors}), 400
        
        # errors2 = ExperienceSchema2.validate(data)
        # if errors2:
        #     return jsonify({"status":"error", "errors":errors2}), 400

        response, status = AuthService.login_user(data)
        return jsonify(response), status