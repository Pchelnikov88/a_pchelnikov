from src.main.api.models.login_user_request import LoginUserRequest
import requests
from src.main.api.configs.config import Config
from src.main.api.models.login_user_response import LoginUserResponse


class RequestSpecs:
    @staticmethod
    def base_headers():
        """Этот метод создает и возвращает базовый словарь HTTP-заголовков"""
        return {
            "Content-Type": "application/json",
            "accept": "application/json",
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        """Этот метод авторизует пользователя и возвращает готовые заголовки с токеном для дальнейших запросов."""
        request = LoginUserRequest(username=username, password=password) # Упаковывает данные для входа
        response = requests.post( # Отправляет запрос на логин
            url="http://localhost:4111/api/auth/token/login",
            json=request.model_dump(),
            headers=RequestSpecs.base_headers()
        )

        if response.status_code == 200: # Проверяет успешность входа
            response_data = LoginUserResponse(**response.json()) # Парсит токен из ответа
            token = response_data.token
            headers = RequestSpecs.base_headers() # Формирует и возвращает заголовки
            headers["Authorization"] = f"Bearer {token}"
            return {
                "headers": headers,
                "base_url": Config.fetch("backendUrl"),
            }

        raise Exception("Failed to login")

    @staticmethod
    def unauth_headers():
        """Метод возвращает заголовки и базовый URL для запросов,
        которые не требуют авторизации (например, логин, регистрация)

        Когда пользователь только логинится, у него еще нет токена.
        Поэтому нельзя использовать auth_headers(). Для таких ручек используется unauth_headers() —
        он дает заголовки без Authorization, но с правильным форматом и URL"""
        return {
            "headers": RequestSpecs.base_headers(),
            "base_url": Config.fetch("backendUrl"),
        }