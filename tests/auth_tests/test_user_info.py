import pytest
from src.app.user_management.domain.value_objects.user_info import UserEmail


def test_equality():

    ue1 = UserEmail(email="john@doe.com")
    ue2 = UserEmail(email="john@doe.com")
    assert ue1 == ue2


def test_immutability():
    ue1 = UserEmail(email="john@doe.com")
    with pytest.raises(Exception) as e:
        ue1.email = "blah@blah.mail"
