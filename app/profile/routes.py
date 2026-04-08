from flask import Blueprint
from flask_jwt_extended import jwt_required
from .controller import ProfileController

profile_bp = Blueprint('profile', __name__)


# Routes for *fetching and *updating profile info:
@profile_bp.route('', methods=["GET"])
@jwt_required()
def get_profile():
    return ProfileController.get_profile()

@profile_bp.route('', methods=["PUT"])
@jwt_required()
def update_profile():
    return ProfileController.update_profile()

@profile_bp.route('/full', methods=["GET"])
@jwt_required()
def get_full_profile():
    return ProfileController.get_full_profile()


# Routes for *adding, *fetching(all), *updating(exp_id), *deleting(exp_id) EXPeriences:
@profile_bp.route('/experience', methods=["POST"])
@jwt_required()
def add_exp():
    return ProfileController.add_experience()

@profile_bp.route('/experience', methods=["GET"])
@jwt_required()
def get_exp():
    return ProfileController.get_experience()

@profile_bp.route('/experience/<int:exp_id>', methods=["PUT"])
@jwt_required()
def update_exp(exp_id):
    return ProfileController.update_experience(exp_id)

@profile_bp.route('/experience/<int:exp_id>', methods=["DELETE"])
@jwt_required()
def delete_exp(exp_id):
    return ProfileController.delete_experience(exp_id)


@profile_bp.route('/skills', methods=["POST"])
@jwt_required()
def add_skills():
    return ProfileController.add_skills()