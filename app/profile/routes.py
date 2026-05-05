from flask import Blueprint
from flask_jwt_extended import jwt_required
from .controller import ProfileController

profile_bp = Blueprint('profile', __name__)


# ------------------------------------------------------------------------------------
# PROFILE routes:
@profile_bp.route('', methods=["GET"])
@jwt_required()
def get_profile():
    return ProfileController.get_profile()

@profile_bp.route('', methods=["PUT"])
@jwt_required()
def update_profile():
    return ProfileController.update_profile()


# ------------------------------------------------------------------------------------
# SKILLS routes:
@profile_bp.route('/skills', methods=["POST"])
@jwt_required()
def add_skills():
    return ProfileController.add_skills()

@profile_bp.route('/skills/<int:skill_id>', methods=["DELETE"])
@jwt_required()
def delete_skill(skill_id):
    return ProfileController.delete_skill(skill_id)


# ------------------------------------------------------------------------------------
# EXPERIENCE routes:
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


# ------------------------------------------------------------------------------------
# EDUCATION routes:
@profile_bp.route('/education', methods=["POST"])
@jwt_required()
def add_edu():
    return ProfileController.add_education()

@profile_bp.route('/education', methods=["GET"])
@jwt_required()
def get_edu():
    return ProfileController.get_education()

@profile_bp.route('/education/<int:edu_id>', methods=["PUT"])
@jwt_required()
def update_edu(edu_id):
    return ProfileController.update_education(edu_id)

@profile_bp.route('/education/<int:edu_id>', methods=["DELETE"])
@jwt_required()
def delete_edu(edu_id):
    return ProfileController.delete_education(edu_id)


# ------------------------------------------------------------------------------------
# PROJECT routes:
@profile_bp.route('/project', methods=['POST'])
@jwt_required()
def add_project():
    return ProfileController.add_project()

@profile_bp.route('/project', methods=['GET'])
@jwt_required()
def get_project():
    return ProfileController.get_project()

@profile_bp.route('/project/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_project(item_id):
    return ProfileController.update_project(item_id)

@profile_bp.route('/project/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_project(item_id):
    return ProfileController.delete_project(item_id)


# ------------------------------------------------------------------------------------
# CERTIFICATION routes:
@profile_bp.route('/certification', methods=['POST'])
@jwt_required()
def add_certification():
    return ProfileController.add_certification()

@profile_bp.route('/certification', methods=['GET'])
@jwt_required()
def get_certification():
    return ProfileController.get_certification()

@profile_bp.route('/certification/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_certification(item_id):
    return ProfileController.update_certification(item_id)

@profile_bp.route('/certification/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_certification(item_id):
    return ProfileController.delete_certification(item_id)


# ------------------------------------------------------------------------------------
# COURSE routes:
@profile_bp.route('/course', methods=['POST'])
@jwt_required()
def add_course():
    return ProfileController.add_course()

@profile_bp.route('/course', methods=['GET'])
@jwt_required()
def get_course():
    return ProfileController.get_course()

@profile_bp.route('/course/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_course(item_id):
    return ProfileController.update_course(item_id)

@profile_bp.route('/course/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_course(item_id):
    return ProfileController.delete_course(item_id)


# ------------------------------------------------------------------------------------
# ACHIEVEMENT routes:
@profile_bp.route('/achievement', methods=['POST'])
@jwt_required()
def add_achievement():
    return ProfileController.add_achievement()

@profile_bp.route('/achievement', methods=['GET'])
@jwt_required()
def get_achievement():
    return ProfileController.get_achievement()

@profile_bp.route('/achievement/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_achievement(item_id):
    return ProfileController.update_achievement(item_id)

@profile_bp.route('/achievement/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_achievement(item_id):
    return ProfileController.delete_achievement(item_id)


# ------------------------------------------------------------------------------------
# CUSTOM ITEM routes:
@profile_bp.route('/custom-item', methods=['POST'])
@jwt_required()
def add_custom_item():
    return ProfileController.add_custom_item()

@profile_bp.route('/custom-item', methods=['GET'])
@jwt_required()
def get_custom_items():
    return ProfileController.get_custom_item()
@profile_bp.route('/custom-item/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_custom_item(item_id):
    return ProfileController.update_custom_item(item_id)

@profile_bp.route('/custom-item/order', methods=['PUT'])
@jwt_required()
def reorder_custom_items():
    return ProfileController.reorder_custom_items()

@profile_bp.route('/custom-item/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_custom_item(item_id):
    return ProfileController.delete_custom_item(item_id)