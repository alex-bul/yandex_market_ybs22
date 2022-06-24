# encoding=utf8

import pytest
import json
import subprocess

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from urllib import parse
from fastapi import status as fastapi_status
from fastapi.testclient import TestClient
from main import app

from pathlib import Path

client = TestClient(app)

ROOT_ID = "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"

IMPORT_BATCHES = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Смартфоны",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "jPhone 13",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 79999
            },
            {
                "type": "OFFER",
                "name": "Xomiа Readme 10",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 59999
            }
        ],
        "updateDate": "2022-02-02T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 32999
            },
            {
                "type": "OFFER",
                "name": "Phyllis 50\" LED UHD Smarter",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 49999
            }
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 69999
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    }
]

EXPECTED_TREE = {
    "type": "CATEGORY",
    "name": "Товары",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 58599,
    "parentId": None,
    "date": "2022-02-03T15:00:00.000Z",
    "children": [
        {
            "type": "CATEGORY",
            "name": "Телевизоры",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 50999,
            "date": "2022-02-03T15:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "Samson 70\" LED UHD Smart",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 32999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None,
                },
                {
                    "type": "OFFER",
                    "name": "Phyllis 50\" LED UHD Smarter",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 49999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Goldstar 65\" LED UHD LOL Very Smart",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 69999,
                    "date": "2022-02-03T15:00:00.000Z",
                    "children": None
                }
            ]
        },
        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 69999,
            "date": "2022-02-02T12:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 79999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ]
        },
    ]
}

IMPORT_BY_ONE_REQUEST = {
    "items": [
        {
            "type": "OFFER",
            "name": "Goldstar 65\" LED UHD LOL Very Smart",
            "id": "02da38bc-f3ce-11ec-b939-0242ac120002",
            "parentId": "0ded9a0a-f3ce-11ec-b939-0242ac120002",
            "price": 69999
        },
        {
            "type": "CATEGORY",
            "name": "Дорогие товары",
            "id": "0ded9a0a-f3ce-11ec-b939-0242ac120002",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
        },
        {
            "type": "OFFER",
            "name": "Samson 70\" LED UHD Smart",
            "id": "3d972e9c-f3ce-11ec-b939-0242ac120002",
            "parentId": "0ded9a0a-f3ce-11ec-b939-0242ac120002",
            "price": 32999
        },
        {
            "type": "OFFER",
            "name": "Phyllis 50\" LED UHD Smarter",
            "id": "4366b518-f3ce-11ec-b939-0242ac120002",
            "parentId": "0ded9a0a-f3ce-11ec-b939-0242ac120002",
            "price": 49999
        },
        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "1dc61c40-f3ce-11ec-b939-0242ac120002",
            "parentId": "0ded9a0a-f3ce-11ec-b939-0242ac120002"
        },
        {
            "type": "OFFER",
            "name": "jPhone 13",
            "id": "29c25022-f3ce-11ec-b939-0242ac120002",
            "parentId": "1dc61c40-f3ce-11ec-b939-0242ac120002",
            "price": 79999
        },
        {
            "type": "OFFER",
            "name": "Xomiа Readme 10",
            "id": "3399e2e0-f3ce-11ec-b939-0242ac120002",
            "parentId": "1dc61c40-f3ce-11ec-b939-0242ac120002",
            "price": 59999
        }
    ],
    "updateDate": "2022-02-24T09:00:00.000Z"
}

UPDATE_WITHOUT_CHANGES = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-05T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Смартфоны",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "jPhone 13",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 79999
            },
            {
                "type": "OFFER",
                "name": "Xomiа Readme 10",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 59999
            }
        ],
        "updateDate": "2022-02-06T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 32999
            },
            {
                "type": "OFFER",
                "name": "Phyllis 50\" LED UHD Smarter",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 49999
            }
        ],
        "updateDate": "2022-02-07T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 69999
            }
        ],
        "updateDate": "2022-02-08T07:00:00.000Z"
    }
]

EXPECTED_STATS = {
    "items": [
        {
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "name": "Товары",
            "parentId": None,
            "type": "CATEGORY",
            "price": None,
            "date": "2022-02-01T12:00:00.000Z"
        },
        {
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "name": "Товары",
            "parentId": None,
            "type": "CATEGORY",
            "price": 69999,
            "date": "2022-02-02T12:00:00.000Z"
        },
        {
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "name": "Товары",
            "parentId": None,
            "type": "CATEGORY",
            "price": 55749,
            "date": "2022-02-03T12:00:00.000Z"
        },
        {
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "name": "Товары",
            "parentId": None,
            "type": "CATEGORY",
            "price": 58599,
            "date": "2022-02-03T15:00:00.000Z"
        }
    ]
}

UPDATE_WITH_CHANGES = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Дорогие телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 52999
            },
            {
                "type": "OFFER",
                "name": "Phyllis 50\" LED UHD Smarter",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 89999
            }
        ],
        "updateDate": "2022-02-11T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 109999
            }
        ],
        "updateDate": "2022-02-12T10:21:20.000Z"
    }
]

EXPECTED_TREE_AFTER_CHANGES = {
    "type": "CATEGORY",
    "name": "Товары",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 78599,
    "parentId": None,
    "date": "2022-02-12T10:21:20.000Z",
    "children": [
        {
            "type": "CATEGORY",
            "name": "Дорогие телевизоры",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 84332,
            "date": "2022-02-12T10:21:20.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "Samson 70\" LED UHD Smart",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 52999,
                    "date": "2022-02-11T12:00:00.000Z",
                    "children": None,
                },
                {
                    "type": "OFFER",
                    "name": "Phyllis 50\" LED UHD Smarter",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 89999,
                    "date": "2022-02-11T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Goldstar 65\" LED UHD LOL Very Smart",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 109999,
                    "date": "2022-02-12T10:21:20.000Z",
                    "children": None
                }
            ]
        },
        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 69999,
            "date": "2022-02-02T12:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 79999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ]
        },
    ]
}

SALES_RESPONSE = {
    'items': [{'id': '73bc3b36-02d1-4245-ab35-3106c9ee1c65', 'name': 'Goldstar 65" LED UHD LOL Very Smart',
               'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', 'type': 'OFFER', 'price': 109999,
               'date': '2022-02-12T10:21:20.000Z'},
              {'id': '74b81fda-9cdc-4b63-8927-c978afed5cf4', 'name': 'Phyllis 50" LED UHD Smarter',
               'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', 'type': 'OFFER', 'price': 89999,
               'date': '2022-02-11T12:00:00.000Z'},
              {'id': '98883e8f-0507-482f-bce2-2fb306cf6483', 'name': 'Samson 70" LED UHD Smart',
               'parentId': '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2', 'type': 'OFFER', 'price': 52999,
               'date': '2022-02-11T12:00:00.000Z'}]
}

EXPECTED_TREE_AFTER_DELETE = {
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "name": "Товары",
    "parentId": None,
    "type": "CATEGORY",
    "price": 75749,
    "date": "2022-02-12T10:21:20.000Z",
    "children": [
        {
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "name": "Смартфоны",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "type": "CATEGORY",
            "price": 69999,
            "date": "2022-02-02T12:00:00.000Z",
            "children": [
                {
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "name": "jPhone 13",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "type": "OFFER",
                    "price": 79999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "name": "Xomiа Readme 10",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "type": "OFFER",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ]
        },
        {
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "name": "Дорогие телевизоры",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "type": "CATEGORY",
            "price": 81499,
            "date": "2022-02-12T10:21:20.000Z",
            "children": [
                {
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "name": "Samson 70\" LED UHD Smart",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "type": "OFFER",
                    "price": 52999,
                    "date": "2022-02-11T12:00:00.000Z",
                    "children": None
                },
                {
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "name": "Goldstar 65\" LED UHD LOL Very Smart",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "type": "OFFER",
                    "price": 109999,
                    "date": "2022-02-12T10:21:20.000Z",
                    "children": None
                }
            ]
        }
    ]
}


def deep_sort_children(node):
    if node.get("children"):
        node["children"].sort(key=lambda x: x["id"])

        for child in node["children"]:
            deep_sort_children(child)


def print_diff(expected, response):
    parent_path = Path(__file__).parent.parent
    with open(parent_path / "expected.json", "w") as f:
        json.dump(expected, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    with open(parent_path / "response.json", "w") as f:
        json.dump(response, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    subprocess.run(["git", "--no-pager", "diff", "--no-index",
                    "expected.json", "response.json"])


def request(url: str, method: str = "GET", json_data=None, json_response=False):
    response = client.request(method=method, url=url, json=json_data)
    return response.status_code, response.json() if json_response else response


@pytest.mark.run(order=1)
def test_import():
    for index, batch in enumerate(IMPORT_BATCHES):
        status, _ = request("/imports", method="POST", json_data=batch)

        assert status == fastapi_status.HTTP_200_OK, f"Expected HTTP status code 200, got {status}"
    print("Test import passed.")


@pytest.mark.run(order=2)
def test_nodes():
    status, response = request(f"/nodes/{ROOT_ID}", json_response=True)

    assert status == fastapi_status.HTTP_200_OK, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_TREE)

    if response != EXPECTED_TREE:
        print_diff(EXPECTED_TREE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    print("Test nodes passed.")


@pytest.mark.run(order=3)
def test_stats():
    status, response = request(
        f"/node/{ROOT_ID}/statistic", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    print(response)
    deep_sort_children(response)
    deep_sort_children(EXPECTED_STATS)

    if response != EXPECTED_STATS:
        print_diff(EXPECTED_STATS, response)
        print("Response doesn't match expected.")
        sys.exit(1)
    print("Test stats passed.")


@pytest.mark.run(order=4)
def test_update_with_changes():
    for index, batch in enumerate(UPDATE_WITH_CHANGES):
        print(f"Importing batch {index}")
        status, _ = request("/imports", method="POST", json_data=batch)

    status, response = request(f"/nodes/{ROOT_ID}", json_response=True)
    assert status == fastapi_status.HTTP_200_OK, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_TREE_AFTER_CHANGES)

    if response != EXPECTED_TREE_AFTER_CHANGES:
        print_diff(EXPECTED_TREE_AFTER_CHANGES, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)


@pytest.mark.run(order=5)
def test_sales():
    params = parse.urlencode({
        "date": "2022-02-12T11:00:00.000Z"
    })
    status, response = request(f"/sales?{params}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    response['items'].sort(key=lambda x: x["date"])
    SALES_RESPONSE['items'].sort(key=lambda x: x["date"])

    if response != SALES_RESPONSE:
        print_diff(SALES_RESPONSE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)


@pytest.mark.run(order=6)
def test_delete_and_checking_updates():
    ELEMENT_ID = "74b81fda-9cdc-4b63-8927-c978afed5cf4"

    status, _ = request(f"/delete/{ELEMENT_ID}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, response = request(f"/nodes/{ROOT_ID}", json_response=True)
    assert status == 200, f"Expected HTTP status code 404, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_TREE_AFTER_DELETE)

    if response != EXPECTED_TREE_AFTER_DELETE:
        print_diff(EXPECTED_TREE_AFTER_DELETE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)


@pytest.mark.run(order=7)
def test_order_when_update():
    status, _ = request("/imports", method="POST", json_data=IMPORT_BY_ONE_REQUEST)

    assert status == 200, f"Expected HTTP status code 200, got {status}"


@pytest.mark.run(order=8)
def test_delete():
    # delete
    status, _ = request(f"/delete/{ROOT_ID}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    # check deletion result
    status, _ = request(f"/nodes/{ROOT_ID}")
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    status, _ = request("/nodes/d515e43f-f3f6-4471-bb77-6b455017a2d2")
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    status, _ = request("/nodes/b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4")
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    status, _ = request(f"/nodes/{ROOT_ID}")
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    params = parse.urlencode({
        "date": "2022-02-12T11:00:00.000Z"
    })
    status, response = request(f"/sales?{params}", json_response=True)
    assert response == {"items": []}

    print("Test delete passed.")


if __name__ == '__main__':
    pytest.main()
