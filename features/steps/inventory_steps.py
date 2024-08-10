# import requests
# from behave import given, when, then


# @given("the server is started")
# def step_impl(context):
#     context.base_url = os.getenv("BASE_URL", "http://localhost:8080")

#     context.resp = requests.get(context.base_url + "/")
#     assert context.resp.status_code == 200

import requests
from compare3 import expect
from behave import given  # pylint: disable=no-name-in-module

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

WAIT_TIMEOUT = 60


@given("the following items")
def step_impl(context):
    """Delete all items and load new ones"""

    # Get a list all of the items
    rest_endpoint = f"{context.base_url}/api/inventory"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    expect(context.resp.status_code).equal_to(HTTP_200_OK)
    # and delete them one by one
    for inventory in context.resp.json():
        context.resp = requests.delete(
            f"{rest_endpoint}/{inventory['id']}", timeout=WAIT_TIMEOUT
        )
        expect(context.resp.status_code).equal_to(HTTP_204_NO_CONTENT)

    # load the database with new items
    for row in context.table:
        payload = {
            "name": row["name"],
            "category": row["category"],
            "available": row["available"] in ["True", "true", "1"],
            "gender": row["gender"],
            "birthday": row["birthday"],
        }
        context.resp = requests.post(rest_endpoint, json=payload, timeout=WAIT_TIMEOUT)
        expect(context.resp.status_code).equal_to(HTTP_201_CREATED)
