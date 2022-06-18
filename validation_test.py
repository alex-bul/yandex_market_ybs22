from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# ВАЛИДАЦИЯ

OFFER_VALIDATION_ACTIONS = [
    ("type", None, "Excepted Validation error. Type must be == CATEGORY or OFFER, current type == None"),
    ("name", None, "Excepted Validation error. Name cannot be None, current name == None"),
    ("id", 213, "Excepted Validation error. Id must be uuid object, current id not uuid object"),
    ("ParentId", 213, "Excepted Validation error. ParentId must be uuid object, current ParentId not uuid object"),
    ("price", None, "Excepted Validation error. Price must be >= 0, current price == None"),
]

# Большая часть параметров была проверена при импорте оффера
CATEGORY_VALIDATION_ACTIONS = [
    ("price", 10, "Excepted Validation error. Price must be None, current price == 10"),
]

offer_import = {
    "type": "OFFER",
    "name": "Xomiа Readme 10",
    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
    "price": 59999,
}

category_import = {
    "type": "CATEGORY",
    "name": "Товары",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "parentId": None
}


# /imports
def test_offer_imports_validation():
    for (field, val, fail_description) in OFFER_VALIDATION_ACTIONS:
        data = offer_import.copy()
        data[field] = val

        response = client.post(
            "/imports",
            json=data
        )
        assert response.status_code == 400
        assert response.json() == {"code": status.HTTP_400_BAD_REQUEST, "message": "Validation Failed"}, \
            fail_description


def test_category_imports_validation():
    for (field, val, fail_description) in CATEGORY_VALIDATION_ACTIONS:
        data = category_import.copy()
        data[field] = val

        response = client.post(
            "/imports",
            json=data
        )
        assert response.status_code == 400
        assert response.json() == {"code": status.HTTP_400_BAD_REQUEST, "message": "Validation Failed"}, \
            fail_description


def test_category_price_validation():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
                "price": 10
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    }

    response = client.post(
        "/imports",
        json=data
    )
    assert response.status_code == 400
    assert response.json() == {"code": status.HTTP_400_BAD_REQUEST, "message": "Validation Failed"}


def test_offer_price_validation():
    data = {
        "items": [
            {
                "type": "OFFER",
                "name": "Телефон",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    }

    response = client.post(
        "/imports",
        json=data
    )
    assert response.status_code == 400
    assert response.json() == {"code": status.HTTP_400_BAD_REQUEST, "message": "Validation Failed"}


def test_unique_id_in_request():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
            },
            {
                "type": "OFFER",
                "name": "Телефон",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None,
                "price": 10
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    }

    response = client.post(
        "/imports",
        json=data
    )
    assert response.status_code == 400
    assert response.json() == {"code": status.HTTP_400_BAD_REQUEST, "message": "Validation Failed"}

# /nodes/{id}

# /delete/{id}
