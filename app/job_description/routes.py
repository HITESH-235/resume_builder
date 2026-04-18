from flask import Blueprint
from flask_jwt_extended import jwt_required
from .controller import JobDescriptionController

jd_bp = Blueprint('job_description', __name__)

@jd_bp.route('/job-description', methods=["POST"])
@jwt_required()
def create_jd():
    return JobDescriptionController.create_jd()

@jd_bp.route('/job-description', methods=["GET"])
@jwt_required()
def get_jds():
    return JobDescriptionController.get_jds()