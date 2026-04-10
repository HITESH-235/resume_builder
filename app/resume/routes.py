from flask import Blueprint
from flask_jwt_extended import jwt_required
from .controller import ResumeController

resume_bp = Blueprint("resume", __name__)



# Create and fetch a resume:
@resume_bp.route('', methods=["POST"])
@jwt_required()
def create_resume():
    return ResumeController.create_resume()

@resume_bp.route('/<int:resume_id>', methods=["GET"])
@jwt_required()
def get_resume(resume_id):
    return ResumeController.get_resume(resume_id)



# Add and sort-all experiences in the resume:
@resume_bp.route('/<int:resume_id>/experience', methods=["POST"])
@jwt_required()
def add_experience_to_resume(resume_id):
    return ResumeController.add_experience_to_resume(resume_id)
    
@resume_bp.route('/<int:resume_id>/experience/order', methods=["PUT"])
@jwt_required()
def reorder_experiences(resume_id):
    return ResumeController.reorder_experiences(resume_id)

@resume_bp.route('/<int:resume_id>/experience/<int:experience_id>', methods=["DELETE"])
@jwt_required()
def remove_experience_from_resume(resume_id, experience_id):
    return ResumeController.remove_experience_from_resume(resume_id, experience_id)



# Add and sort-all skills in the resume:
@resume_bp.route('/<int:resume_id>/skill', methods=["POST"])
@jwt_required()
def add_skill_to_resume(resume_id):
    return ResumeController.add_skill_to_resume(resume_id)

@resume_bp.route('/<int:resume_id>/skill/order', methods=["PUT"])
@jwt_required()
def reorder_skills(resume_id):
    return ResumeController.reorder_skills(resume_id)

@resume_bp.route('/<int:resume_id>/skill/<int:skill_id>', methods=["DELETE"])
@jwt_required()
def remove_skill_from_resume(resume_id, skill_id):
    return ResumeController.remove_skill_from_resume(resume_id, skill_id)

@resume_bp.route('/<int:resume_id>', methods=["PUT"])
@jwt_required()
def update_resume(resume_id):
    return ResumeController.update_resume(resume_id)