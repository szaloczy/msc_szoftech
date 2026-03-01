from flask import Blueprint, jsonify, request

from backend.src.models.user import get_user, generate_unique_id, add_user, remove_user

users_controller = Blueprint('users_controller', __name__)

def create_response(data=None, error=None, status=200):
    return jsonify({
        "succes": error is None,
        "data": data,
        "error": error
    }),status

@users_controller.route('/api/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = get_user(user_id)

    if not user:
        return create_response(error="User not found", status=404)

    return create_response(data=user)

@users_controller.route('/api/users', methods=['POST'])
def create_user():
    body = request.get_json()

    if not body or 'name' not in body:
        return create_response(error="'name' field required!", status=400)

    user_name = str(body['name']).strip()
    if not user_name:
        return create_response(error="Name cannot be empty!", status=400)

    new_id = generate_unique_id()
    new_user = add_user(user_name, new_id)

    return create_response(data=new_user, status=201)


@users_controller.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    is_deleted = remove_user(user_id)

    if not is_deleted:
        return create_response(error="User not found.", status=404)

    return create_response(data={"message": "User successfully deleted."})
