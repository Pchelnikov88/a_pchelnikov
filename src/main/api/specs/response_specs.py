from requests import Response
from http import HTTPStatus


class ResponseSpecs:
    # проверяем что сервер вернул код 200
    @staticmethod
    def request_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    # проверяем что сервер вернул код 201
    @staticmethod
    def request_created():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    # проверяем что сервер вернул код 400
    @staticmethod
    def request_bad():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    # проверяем что сервер вернул код 404
    @staticmethod
    def request_not_found():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text
        return confirm

    # проверяем что сервер вернул код 422
    @staticmethod
    def request_unprocessable():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text

        return confirm