import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from urllib import parse

from fastapi import status
from fastapi.testclient import TestClient

from tests.utils import assert_validation_error_by_response
from main import app

client = TestClient(app)

# ВАЛИДАЦИЯ

OFFER_VALIDATION_ACTIONS = [
    ("type", None, "Excepted Validation error. Type must be == CATEGORY or OFFER, current type == {0}"),
    ("type", "Car", "Excepted Validation error. Type must be == CATEGORY or OFFER, current type == {0}"),
    ("name", None, "Excepted Validation error. Name cannot be None, current name == {0}"),
    ("name", 3213, "Excepted Validation error. Name cannot be None, current name == {0}"),
    ("id", 213, "Excepted Validation error. Id must be uuid object, current id == {0}"),
    ("id", None, "Excepted Validation error. Id must be uuid object, current id == {0}"),
    ("ParentId", "fsdfdfs", "Excepted Validation error. ParentId must be uuid object, current ParentId == {0}"),
    ("ParentId", 213, "Excepted Validation error. ParentId must be uuid object, current ParentId == {0}"),
    ("price", None, "Excepted Validation error. Price must be >= 0, current price == {0}"),
    ("price", -2000, "Excepted Validation error. Price must be >= 0, current price == {0}"),
    ("extra_field", -2000, "Excepted Validation error. Extra field mustnt exist, current extra_field == {0}"),
]

# Большая часть параметров была проверена при импорте оффера
CATEGORY_VALIDATION_ACTIONS = [
    ("price", 10, "Excepted Validation error. Price must be None, current price == {0}"),
]

offer_import = {
    "type": "OFFER",
    "name": "Xomiа Readme 10",
    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d5",
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

        assert_validation_error_by_response(response, fail_description.format(val))


def test_category_imports_validation():
    for (field, val, fail_description) in CATEGORY_VALIDATION_ACTIONS:
        data = category_import.copy()
        data[field] = val

        response = client.post(
            "/imports",
            json=data
        )

        assert_validation_error_by_response(response, fail_description.format(val))


def test_change_type():
    data = offer_import.copy()

    client.post(
        "/imports",
        json=data
    )

    data["type"] = "CATEGORY"

    response = client.post(
        "/imports",
        json=data
    )

    client.delete(f"/delete/{data['id']}")

    assert_validation_error_by_response(response, "Shop unit cant change type")


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
    assert_validation_error_by_response(response)


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

    assert_validation_error_by_response(response)


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
    assert_validation_error_by_response(response)


def test_date_validation():
    dates = ["2022.02.01 14:00:00", "2022.02.01T14:00:00", "2022.02.30T14:00:00.000Z", 22323223]
    for i in dates:
        data = {
            "items": [
                {
                    "type": "CATEGORY",
                    "name": "Товары",
                    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                    "parentId": None,
                }
            ],
            "updateDate": i
        }

        response = client.post(
            "/imports",
            json=data
        )
        assert_validation_error_by_response(response)


# /nodes/{id}
def test_nodes_validation():
    ids = ["1212131", "sdfsdfsf"]
    for id in ids:
        response = client.get(f"/nodes/{id}")

        assert_validation_error_by_response(response)


# /delete/{id}
def test_delete_validation():
    ids = ["1212131", "sdfsdfsf"]
    for id in ids:
        response = client.delete(f"/delete/{id}")

        assert_validation_error_by_response(response)


# /sales
def test_sales_validation():
    dates = ["2022.02.01 14:00:00", "2022.02.01T14:00:00", "2022.02.30T14:00:00.000Z", 22323223]
    for i in dates:
        response = client.get("/sales")

        assert_validation_error_by_response(response)


# /node/{id}/statistic
def test_node_statistic_interval():
    params = parse.urlencode({
        "dateStart": "2022-02-12T11:00:00.000Z",
        "dateEnd": "2022-02-10T11:00:00.000Z"
    })
    response = client.get(f"/node/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1/statistic?{params}")

    assert_validation_error_by_response(response)
