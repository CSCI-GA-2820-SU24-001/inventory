# pylint: disable=function-redefined
# flake8: noqa
"""
Inventory Steps

Steps file for Inventory.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given  # pylint: disable=no-name-in-module

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

WAIT_TIMEOUT = 60


@given("the following items")
def step_impl(context):
    """Delete all Inventory Items and load new ones"""

    # Get a list of all the inventory items
    rest_endpoint = f"{context.base_url}/inventory"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    assert context.resp.status_code == HTTP_200_OK
    # and delete them one by one
    for item in context.resp.json():
        context.resp = requests.delete(
            f"{rest_endpoint}/{item['id']}", timeout=WAIT_TIMEOUT
        )
        assert context.resp.status_code == HTTP_204_NO_CONTENT

    # load the database with new items
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "quantity": int(row["quantity"]),
            "price": float(row["price"]),
            "product_id": int(row["product_id"]),
            "restock_level": int(row["restock_level"]),
            "condition": row["condition"],
        }
        context.resp = requests.post(rest_endpoint, json=payload, timeout=WAIT_TIMEOUT)
        assert context.resp.status_code == HTTP_201_CREATED
