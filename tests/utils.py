from requests import Response
from fastapi import status


def assert_validation_error_by_response(response: Response,
                                        fail_description_status_code="Excepted 400 http status code, got {}"):
    assert response.status_code == status.HTTP_400_BAD_REQUEST, fail_description_status_code.format(
        response.status_code)
    assert response.json() == {"code": status.HTTP_400_BAD_REQUEST,
                               "message": "Validation Failed"}, f"Response must be " \
                                                                f"validation error, got {response.json()}"


def assert_not_found_error_by_response(response: Response,
                                       fail_description_status_code="Excepted 404 http status code, got {}"):
    assert response.status_code == status.HTTP_404_NOT_FOUND, fail_description_status_code.format(
        response.status_code)
    assert response.json() == {"code": status.HTTP_404_NOT_FOUND,
                               "message": "Item not found"}, f"Response must be " \
                                                             f"not found error, got {response.json()}"
