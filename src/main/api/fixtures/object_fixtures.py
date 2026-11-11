import pytest
import logging
from typing import List, Any
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_response import CreateUserResponse

"""Это «уборщик» (Teardown), который автоматически удаляет за тестами созданные данные 
(например, пользователей). Он гарантирует, что после завершения теста база данных не засоряется, 
и следующие тесты начинаются с «чистого листа»."""

@pytest.fixture
def created_obj():
    """Фикстура, которая удаляет пользователя"""
    objects: List[Any] = []
    yield objects
    clean_user(objects)

def clean_user(objects: List[Any]):
    """Вспомогательная функция, удаляет пользователя"""
    api_manager = ApiManager(objects)
    for u in objects:
        if isinstance(u, CreateUserResponse):
            api_manager.admin_steps.delete_user(u.id)
        else:
            logging.warning(f"Error in delete user_id: {u.id}")