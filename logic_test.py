# encoding=utf8

import json
import subprocess
import sys

from fastapi import status
from fastapi.testclient import TestClient
from main import app

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
            "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
            "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "price": 69999
        },
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
        },
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
        },
        {
            "type": "CATEGORY",
            "name": "Товары",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "parentId": None
        }
    ],
    "updateDate": "2022-02-04T09:00:00.000Z"
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
        "updateDate": "2022-02-08T15:00:00.000Z"
    }
]

EXPECTED_TREE_AFTER_NO_CHANGES = {
    "type": "CATEGORY",
    "name": "Товары",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 58599,
    "parentId": None,
    "date": "2022-02-08T15:00:00.000Z",
    "children": [
        {
            "type": "CATEGORY",
            "name": "Телевизоры",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 50999,
            "date": "2022-02-08T15:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "Samson 70\" LED UHD Smart",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 32999,
                    "date": "2022-02-07T12:00:00.000Z",
                    "children": None,
                },
                {
                    "type": "OFFER",
                    "name": "Phyllis 50\" LED UHD Smarter",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 49999,
                    "date": "2022-02-07T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Goldstar 65\" LED UHD LOL Very Smart",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 69999,
                    "date": "2022-02-08T15:00:00.000Z",
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
            "date": "2022-02-06T12:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 79999,
                    "date": "2022-02-06T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 59999,
                    "date": "2022-02-06T12:00:00.000Z",
                    "children": None
                }
            ]
        },
    ]
}


def deep_sort_children(node):
    if node.get("children"):
        node["children"].sort(key=lambda x: x["id"])

        for child in node["children"]:
            deep_sort_children(child)


def print_diff(expected, response):
    with open("expected.json", "w") as f:
        json.dump(expected, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    with open("response.json", "w") as f:
        json.dump(response, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    subprocess.run(["git", "--no-pager", "diff", "--no-index",
                    "expected.json", "response.json"])


def request(url: str, method: str = "GET", json_data=None, json_response=False):
    response = client.request(method=method, url=url, json=json_data)
    return response.status_code, response.json() if json_response else response


def test_import():
    for index, batch in enumerate(UPDATE_WITHOUT_CHANGES):
        print(f"Importing batch {index}")
        status, _ = request("/imports", method="POST", json_data=batch)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test import passed.")


def test_nodes():
    status, response = request(f"/nodes/{ROOT_ID}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_TREE)

    if response == EXPECTED_TREE:
        print_diff(EXPECTED_TREE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    print("Test nodes passed.")


def test_update_without_change():
    """"""
    for index, batch in enumerate(UPDATE_WITHOUT_CHANGES):
        print(f"Importing batch {index}")
        status, _ = request("/imports", method="POST", json_data=batch)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, response = request(f"/nodes/{ROOT_ID}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_TREE_AFTER_NO_CHANGES)

    if response != EXPECTED_TREE_AFTER_NO_CHANGES:
        print_diff(EXPECTED_TREE_AFTER_NO_CHANGES, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)


# def test_sales():
#     params = urllib.parse.urlencode({
#         "date": "2022-02-04T00:00:00.000Z"
#     })
#     status, response = request(f"/sales?{params}", json_response=True)
#     assert status == 200, f"Expected HTTP status code 200, got {status}"
#     print("Test sales passed.")
#
#
# def test_stats():
#     params = urllib.parse.urlencode({
#         "dateStart": "2022-02-01T00:00:00.000Z",
#         "dateEnd": "2022-02-03T00:00:00.000Z"
#     })
#     status, response = request(
#         f"/node/{ROOT_ID}/statistic?{params}", json_response=True)
#
#     assert status == 200, f"Expected HTTP status code 200, got {status}"
#     print("Test stats passed.")
#
#
def test_delete():
    status, _ = request(f"/delete/{ROOT_ID}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, _ = request(f"/nodes/{ROOT_ID}")
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    print("Test delete passed.")
