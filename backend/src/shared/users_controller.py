from flask import Blueprint

users_controller = Blueprint('users_controller', __name__)

@users_controller.route('/api/users', methods=['PUT'])
def create_user():
    pass