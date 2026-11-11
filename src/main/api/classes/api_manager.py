from typing import List, Any

from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps

class ApiManager:
    """Класс ApiManager — это «единая точка входа» (паттерн Facade),
    которая собирает в себе все доступные действия (шаги) для тестов."""
    def __init__(self, created_obj: List[Any]): # Принимает список created_obj (созданные объекты). Это общий контейнер, куда Steps будут складывать созданных пользователей, счета и т.д. для последующей очистки (teardown).
        self.admin_steps = AdminSteps(created_obj)
        self.user_steps = UserSteps(created_obj)