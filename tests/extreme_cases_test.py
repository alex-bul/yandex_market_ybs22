import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from fastapi import status
from fastapi.testclient import TestClient

from tests.utils import assert_validation_error_by_response, assert_not_found_error_by_response
from main import app

client = TestClient(app)


def test_import_no_parent():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": "061cd8d7-bbad-47d5-ap8f-82ef4c269ks9",
            },
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    }

    response = client.post(
        "/imports",
        json=data
    )

    assert_validation_error_by_response(response, "Parent must be exist")


def test_offer_as_parent():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": "061cd8d7-bbad-47d5-ap8f-82ef4c269ks9",
            },
            {
                "type": "OFFER",
                "name": "Машина",
                "price": 10,
                "id": "061cd8d7-bbad-47d5-ap8f-82ef4c269ks9",
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    }

    response = client.post(
        "/imports",
        json=data
    )

    assert_validation_error_by_response(response,
                                        fail_description_status_code="Offer cant be used as parent")


def test_not_found_delete():
    response = client.delete("/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1")

    assert_not_found_error_by_response(response)


def test_not_found_statistic():
    response = client.get("/node/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1/statistic")

    assert_not_found_error_by_response(response)
