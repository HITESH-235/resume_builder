from flask import Blueprint
from flask_jwt_extended import jwt_required
from .controller import ResumeController

resume_bp = Blueprint("resume", __name__)


# --------------------------------------------------------------------------------------------------------------
# Resume routes:

@resume_bp.route('', methods=["POST"])
@jwt_required()
def create_resume():
    return ResumeController.create_resume()

@resume_bp.route('', methods=["GET"])
@jwt_required()
def get_all_resumes():
    return ResumeController.get_all_resumes()

@resume_bp.route('/<int:resume_id>', methods=["GET"])
@jwt_required()
def get_resume(resume_id):
    return ResumeController.get_resume(resume_id)

@resume_bp.route('/<int:resume_id>', methods=["PUT"])
@jwt_required()
def update_resume(resume_id):
    return ResumeController.update_resume(resume_id)

@resume_bp.route('/<int:resume_id>', methods=["DELETE"])
@jwt_required()
def delete_resume(resume_id):
    return ResumeController.delete_resume(resume_id)

@resume_bp.route('/<int:resume_id>/duplicate', methods=["POST"])
@jwt_required()
def duplicate_resume(resume_id):
    return ResumeController.duplicate_resume(resume_id)


# --------------------------------------------------------------------------------------------------------------
# Resume's experience routes:

@resume_bp.route('/<int:resume_id>/experience', methods=["POST"])
@jwt_required()
def add_experience_to_resume(resume_id):
    return ResumeController.add_experience_to_resume(resume_id)
    
@resume_bp.route('/<int:resume_id>/experience/<int:experience_id>', methods=["DELETE"])
@jwt_required()
def remove_experience_from_resume(resume_id, experience_id):
    return ResumeController.remove_experience_from_resume(resume_id, experience_id)

@resume_bp.route('/<int:resume_id>/experience/order', methods=["PUT"])
@jwt_required()
def reorder_experiences(resume_id):
    return ResumeController.reorder_experiences(resume_id)


# --------------------------------------------------------------------------------------------------------------
# Resume's skill routes:

@resume_bp.route('/<int:resume_id>/skill', methods=["POST"])
@jwt_required()
def add_skill_to_resume(resume_id):
    return ResumeController.add_skill_to_resume(resume_id)

@resume_bp.route('/<int:resume_id>/skill/<int:skill_id>', methods=["DELETE"])
@jwt_required()
def remove_skill_from_resume(resume_id, skill_id):
    return ResumeController.remove_skill_from_resume(resume_id, skill_id)

@resume_bp.route('/<int:resume_id>/skill/order', methods=["PUT"])
@jwt_required()
def reorder_skills(resume_id):
    return ResumeController.reorder_skills(resume_id)


# --------------------------------------------------------------------------------------------------------------
# Resume's education routes:

@resume_bp.route('/<int:resume_id>/education', methods=["POST"])
@jwt_required()
def add_education_to_resume(resume_id):
    return ResumeController.add_education_to_resume(resume_id)

@resume_bp.route('/<int:resume_id>/education/<int:education_id>', methods=["DELETE"])
@jwt_required()
def remove_education_from_resume(resume_id, education_id):
    return ResumeController.remove_education_from_resume(resume_id, education_id)

@resume_bp.route('/<int:resume_id>/education/order', methods=["PUT"])
@jwt_required()
def reorder_educations(resume_id):
    return ResumeController.reorder_educations(resume_id)


# --------------------------------------------------------------------------------------------------------------
# Resume's project routes:

@resume_bp.route('/<int:resume_id>/project', methods=['POST'])
@jwt_required()
def add_project(resume_id):
    return ResumeController.add_project(resume_id)

@resume_bp.route('/<int:resume_id>/project/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_project(resume_id, item_id):
    return ResumeController.remove_project(resume_id, item_id)

@resume_bp.route('/<int:resume_id>/project/reorder', methods=['PUT'])
@jwt_required()
def reorder_project(resume_id):
    return ResumeController.reorder_project(resume_id)


# --------------------------------------------------------------------------------------------------------------
# Resume's certification routes:

@resume_bp.route('/<int:resume_id>/certification', methods=['POST'])
@jwt_required()
def add_certification(resume_id):
    return ResumeController.add_certification(resume_id)

@resume_bp.route('/<int:resume_id>/certification/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_certification(resume_id, item_id):
    return ResumeController.remove_certification(resume_id, item_id)

@resume_bp.route('/<int:resume_id>/certification/reorder', methods=['PUT'])
@jwt_required()
def reorder_certification(resume_id):
    return ResumeController.reorder_certification(resume_id)


# --------------------------------------------------------------------------------------------------------------
# Resume's course routes:

@resume_bp.route('/<int:resume_id>/course', methods=['POST'])
@jwt_required()
def add_course(resume_id):
    return ResumeController.add_course(resume_id)

@resume_bp.route('/<int:resume_id>/course/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_course(resume_id, item_id):
    return ResumeController.remove_course(resume_id, item_id)

@resume_bp.route('/<int:resume_id>/course/reorder', methods=['PUT'])
@jwt_required()
def reorder_course(resume_id):
    return ResumeController.reorder_course(resume_id)


# --------------------------------------------------------------------------------------------------------------
# Resume's achievement routes:

@resume_bp.route('/<int:resume_id>/achievement', methods=['POST'])
@jwt_required()
def add_achievement(resume_id):
    return ResumeController.add_achievement(resume_id)

@resume_bp.route('/<int:resume_id>/achievement/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_achievement(resume_id, item_id):
    return ResumeController.remove_achievement(resume_id, item_id)

@resume_bp.route('/<int:resume_id>/achievement/reorder', methods=['PUT'])
@jwt_required()
def reorder_achievement(resume_id):
    return ResumeController.reorder_achievement(resume_id)