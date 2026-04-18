from flask import Blueprint
from .controller import AuthController

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/refresh', methods=["POST"])(AuthController.refresh)
auth_bp.route('/register', methods=["POST"])(AuthController.signup)
auth_bp.route('/login', methods=["POST"])(AuthController.login)