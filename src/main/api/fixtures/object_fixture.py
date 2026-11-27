import logging
from typing import Any

import pytest

from main.api.classes.api_manager import ApiManager
from main.api.models.create_user_response import CreateUserResponse


def clean_user(objects: list[Any]):
    api_manager = ApiManager(objects)
    for u in objects:
        if isinstance(u, CreateUserResponse):
            api_manager.admin_steps.delete_user(u.id)
        else:
            logging.warning(f"Error in delete user_id: {u.id}")

@pytest.fixture
def created_obj():
    objects: list[Any] = []
    yield objects
    clean_user(objects)



