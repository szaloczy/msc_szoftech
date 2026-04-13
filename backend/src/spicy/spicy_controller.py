from flask import request, jsonify, Blueprint

from src.spicy.spicy_room_service import SpicyRoomService

spicy_game_controller = Blueprint('game_controller', __name__)

@spicy_game_controller.route('/api/startgame', methods=['POST'])
async def start_game_endpoint():
    player_id = request.cookies.get("userId")
    room_id = request.get_json().get('roomId')

    if not player_id:
        return jsonify({"message": "Player id is required"}), 400

    if not room_id:
        return jsonify({"message": "Room id is required"}), 400

    try:
        # Call the service to start the game
        message =  await SpicyRoomService.start_game(player_id, room_id)
        return jsonify({"message": message}), 200
    except Exception as e:
        return e.msg(), 400