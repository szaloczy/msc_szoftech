import pytest
import src.models.user as users

@pytest.fixture(autouse=True)
def reset_users():
    users.users = []
    yield
    users.users = []

def test_add_and_get_user():
    users.add_user("Teszt Elek", "id-456")
    assert len(users.users) == 1
    user = users.get_user("id-456")
    assert user is not None
    assert user["name"] == "Teszt Elek"

def test_remove_user():
    users.add_user("Teszt Player", "id-987")  #

    remove = users.remove_user("id-987")
    assert remove is True
    assert len(users.users) == 0

    not_valid_user = users.remove_user("not-valid-id")
    assert not_valid_user is False

def test_generate_unique_id():
    id1 = users.generate_unique_id()
    id2 = users.generate_unique_id()
    assert id1 != id2