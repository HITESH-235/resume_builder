from flask import Blueprint, request, jsonify
from .controllers import AuthController, ProfileController
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Blueprint('api', __name__)

auth_bp = Blueprint('auth', __name__) # for handling signup and login route
auth_bp.route('/register', methods=["POST"])(AuthController.signup)
auth_bp.route('/login', methods=["POST"])(AuthController.login)

profile_bp = Blueprint('profile', __name__)


# Routes for *adding, *fetching(all), *deleting(exp_id) EXPeriences:

@profile_bp.route('/experience', methods=["POST"]) # adding new exp
@jwt_required()
def add_exp():
    return ProfileController.add_experience()

@profile_bp.route('/experience', methods=["GET"]) # fetching all exps
@jwt_required()
def get_exp():
    return ProfileController.get_experience()

@profile_bp.route('/experience/<int:exp_id>', methods=["DELETE"])
@jwt_required()
def delete(exp_id):
    return ProfileController.delete_experience(exp_id)


# Routes for *fetching and *updating profile info:

@profile_bp.route('', methods=["GET"])
@jwt_required()
def get_profile():
    return ProfileController.get_profile()

@profile_bp.route('', methods=["PUT"])
@jwt_required()
def update_profile():
    return ProfileController.update_profile()