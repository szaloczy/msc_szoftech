from src.spicy.spicy_room_data import SpicyRoomData

def get_room_service_map():
    from src.spicy.spicy_room_service import SpicyRoomService

    return {
        SpicyRoomData: SpicyRoomService(),
    }