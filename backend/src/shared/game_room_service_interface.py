from abc import ABC, abstractmethod

class GameRoomService(ABC):

    @staticmethod
    @abstractmethod
    async def update_all_users(room, user_id=None):
        """ Update all users in the room with the current state of the room.
        Contains everything that is needed to render the room in the client.
        :param room: room data object
        :param user_id: user ID to update specifically, if provided
        :return:
        """
        raise NotImplementedError()