import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from fastapi import status
from fastapi.testclient import TestClient

from tests.utils import assert_validation_error_by_response, assert_not_found_error_by_response, assert_ok_response
from main import app

client = TestClient(app)


def test_import_no_parent():
    """Попытка создать объект с несуществующим родителем"""
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "6054204c-f3f2-11ec-b939-0242ac120002",
                "parentId": "64aeda56-f3f2-11ec-b939-0242ac120002",
            },
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    }

    response = client.post(
        "/imports",
        json=data
    )

    assert_validation_error_by_response(response, "Parent must exist")


def test_offer_as_parent():
    """Попытка указать товар как родителя"""
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "6054204c-f3f2-11ec-b939-0242ac120002",
                "parentId": "64aeda56-f3f2-11ec-b939-0242ac120002",
            },
            {
                "type": "OFFER",
                "name": "Машина",
                "price": 10,
                "id": "64aeda56-f3f2-11ec-b939-0242ac120002",
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    }

    response = client.post(
        "/imports",
        json=data
    )

    assert_validation_error_by_response(response,
                                        fail_description_status_code="Offer cant used as parent")


def test_not_found_delete():
    """Удаление несуществующего объекта"""
    response = client.delete("/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df2")

    assert_not_found_error_by_response(response)


def test_not_found_statistic():
    """Запрос статистики несуществующего объекта"""
    response = client.get("/node/069cb8d7-bbdd-47d3-ad8f-82ef4c269df2/statistic")

    assert_not_found_error_by_response(response)


def test_sales_intervals():
    """Запрос скидок после создания товара с разным интервалом"""
    data = {
        "items": [
            {
                "type": "OFFER",
                "name": "Машина",
                "price": 10,
                "id": "d4351384-f3ef-11ec-b939-0242ac120002",
            },
        ],
        "updateDate": "2022-05-01T12:00:00.000Z"
    }

    sales_ok = {'items': [
        {'id': 'd4351384-f3ef-11ec-b939-0242ac120002', 'name': 'Машина', 'parentId': None, 'type': 'OFFER', 'price': 10,
         'date': '2022-05-01T12:00:00.000Z'}]}

    response = client.post(
        "/imports",
        json=data
    )

    assert_ok_response(response)

    # проверяем интервал до
    response = client.get(
        "/sales?date=2022-05-01T11:00:00.000Z"
    )

    assert response.json() == {'items': []}

    # проверяем итервал начинающийся в дате создания
    response = client.get(
        "/sales?date=2022-05-01T12:00:00.000Z"
    )

    assert response.json() == sales_ok

    response = client.get(
        "/sales?date=2022-05-02T12:00:00.000Z"
    )

    assert response.json() == sales_ok

    # проверяем интервал после
    response = client.get(
        "/sales?date=2022-05-02T12:00:01.000Z"
    )

    assert response.json() == {'items': []}

    response = client.delete(f"/delete/{data['items'][0]['id']}")
    assert_ok_response(response)


def test_statistic_intervals():
    """Тест интервалов у статистики"""

    data = [
        {
            "items": [
                {
                    "type": "OFFER",
                    "name": "Машина",
                    "price": 10,
                    "id": "002fe7de-f3f5-11ec-b939-0242ac120002",
                },
            ],
            "updateDate": "2022-05-01T12:00:00.000Z"
        },
        {
            "items": [
                {
                    "type": "OFFER",
                    "name": "Машина Красная",
                    "price": 10000,
                    "id": "002fe7de-f3f5-11ec-b939-0242ac120002",
                },
            ],
            "updateDate": "2022-05-01T18:00:00.000Z"
        },
        {
            "items": [
                {
                    "type": "OFFER",
                    "name": "Машина Красная",
                    "price": 19000,
                    "id": "002fe7de-f3f5-11ec-b939-0242ac120002",
                },
            ],
            "updateDate": "2022-05-01T23:00:00.000Z"
        },
    ]

    # загрузка данных
    for i in data:
        response = client.post(
            "/imports",
            json=i
        )

        assert_ok_response(response)

    # проверка несовпадающего интервала
    response = client.get(
        "/node/002fe7de-f3f5-11ec-b939-0242ac120002/statistic?"
        "dateStart=2022-05-01T10:00:00.000Z&dateEnd=2022-05-01T11:00:00.000Z&"
    )

    assert response.json() == {'items': []}

    # интервал заканчивается на времени создании
    response = client.get(
        "/node/002fe7de-f3f5-11ec-b939-0242ac120002/statistic?"
        "dateStart=2022-05-01T10:00:00.000Z&dateEnd=2022-05-01T12:00:00.000Z&"
    )

    assert response.json() == {'items': [
        {'id': '002fe7de-f3f5-11ec-b939-0242ac120002', 'name': 'Машина', 'parentId': None, 'type': 'OFFER', 'price': 10,
         'date': '2022-05-01T12:00:00.000Z'}]}

    # за всё время
    response = client.get(
        "/node/002fe7de-f3f5-11ec-b939-0242ac120002/statistic"
    )

    assert response.json() == {'items': [
        {'id': '002fe7de-f3f5-11ec-b939-0242ac120002', 'name': 'Машина', 'parentId': None, 'type': 'OFFER', 'price': 10,
         'date': '2022-05-01T12:00:00.000Z'},
        {'id': '002fe7de-f3f5-11ec-b939-0242ac120002', 'name': 'Машина Красная', 'parentId': None, 'type': 'OFFER',
         'price': 10000, 'date': '2022-05-01T18:00:00.000Z'},
        {'id': '002fe7de-f3f5-11ec-b939-0242ac120002', 'name': 'Машина Красная', 'parentId': None, 'type': 'OFFER',
         'price': 19000, 'date': '2022-05-01T23:00:00.000Z'}]}

    # за промежуток
    response = client.get(
        "/node/002fe7de-f3f5-11ec-b939-0242ac120002/statistic?"
        "dateStart=2022-05-01T10:00:00.000Z&dateEnd=2022-05-01T18:00:00.000Z&"
    )

    assert response.json() == {'items': [
        {'id': '002fe7de-f3f5-11ec-b939-0242ac120002', 'name': 'Машина', 'parentId': None, 'type': 'OFFER', 'price': 10,
         'date': '2022-05-01T12:00:00.000Z'},
        {'id': '002fe7de-f3f5-11ec-b939-0242ac120002', 'name': 'Машина Красная', 'parentId': None, 'type': 'OFFER',
         'price': 10000, 'date': '2022-05-01T18:00:00.000Z'}]}

    # за промежуток
    response = client.get(
        "/node/002fe7de-f3f5-11ec-b939-0242ac120002/statistic?"
        "dateStart=2022-05-01T15:00:00.000Z&dateEnd=2022-05-01T23:00:00.000Z&"
    )

    assert response.json() == {'items': [
        {'id': '002fe7de-f3f5-11ec-b939-0242ac120002', 'name': 'Машина Красная', 'parentId': None, 'type': 'OFFER',
         'price': 10000, 'date': '2022-05-01T18:00:00.000Z'},
        {'id': '002fe7de-f3f5-11ec-b939-0242ac120002', 'name': 'Машина Красная', 'parentId': None, 'type': 'OFFER',
         'price': 19000, 'date': '2022-05-01T23:00:00.000Z'}]}

    # проверка несовпадающего интервала
    response = client.get(
        "/node/002fe7de-f3f5-11ec-b939-0242ac120002/statistic?"
        "dateStart=2022-05-01T23:00:01.000Z&dateEnd=2022-05-05T11:00:00.000Z&"
    )

    assert response.json() == {'items': []}

    response = client.delete(f"/delete/{data[0]['items'][0]['id']}")
    assert_ok_response(response)


def test_updating_after_deletion():
    """Тест изменения цены родительской категории при удалении детей"""
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "6054204c-f3f2-11ec-b939-0242ac120002",
            },
            {
                "type": "OFFER",
                "name": "Машина",
                "price": 0,
                "parentId": "6054204c-f3f2-11ec-b939-0242ac120002",
                "id": "64aeda56-f3f2-11ec-b939-0242ac120002",
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    }

    response = client.post(
        "/imports",
        json=data
    )
    assert_ok_response(response)

    response = client.get(
        "/nodes/6054204c-f3f2-11ec-b939-0242ac120002"
    )

    assert response.json()["price"] == 0

    response = client.delete(f"/delete/64aeda56-f3f2-11ec-b939-0242ac120002")
    assert_ok_response(response)

    response = client.get(
        "/nodes/6054204c-f3f2-11ec-b939-0242ac120002"
    )

    assert response.json()["price"] is None

    response = client.delete(f"/delete/6054204c-f3f2-11ec-b939-0242ac120002")
    assert_ok_response(response)
