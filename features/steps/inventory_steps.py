# pylint: disable=function-redefined
# flake8: noqa
"""
Inventory Steps

Steps file for Inventory.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given, when, then  # pylint: disable=no-name-in-module

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_404_NOT_FOUND = 404
WAIT_TIMEOUT = 60


@given("the following items exist")
def step_impl(context):
    """Ensure the specified items exist in the inventory"""
    rest_endpoint = f"{context.base_url}/api/inventory"

    # Create the items listed in the table
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "quantity": int(row["quantity"]),
            "price": float(row["price"]),
            "product_id": int(row["product_id"]),
            "restock_level": int(row["restock_level"]),
            "condition": row["condition"].lower(),
        }
        context.resp = requests.post(rest_endpoint, json=payload, timeout=WAIT_TIMEOUT)

        # Print response for debugging
        print(f"Payload: {payload}")
        print(f"Response Status Code: {context.resp.status_code}")
        print(f"Response Content: {context.resp.content}")

        assert (
            context.resp.status_code == HTTP_201_CREATED
        ), f"Failed to create item: {payload['name']}"


@given("I have access to the inventory service")
def step_impl(context):
    """Check access to the inventory service"""
    rest_endpoint = f"{context.base_url}/api/inventory"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    assert context.resp.status_code == HTTP_200_OK


@when('I add a new item with name "{item_name}"')
def step_impl(context, item_name):
    """Add a new item to the inventory"""
    rest_endpoint = f"{context.base_url}/api/inventory"
    payload = {
        "name": item_name,
        "description": "A new item",
        "quantity": 1,
        "price": 10.00,
        "product_id": 999,
        "restock_level": 1,
        "condition": "new",
    }
    context.resp = requests.post(rest_endpoint, json=payload, timeout=WAIT_TIMEOUT)
    assert context.resp.status_code == HTTP_201_CREATED


@then("I should see the item in the inventory list")
def step_impl(context):
    """Check if the item is in the inventory list"""
    rest_endpoint = f"{context.base_url}/api/inventory"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    assert context.resp.status_code == HTTP_200_OK
    items = context.resp.json()
    item_names = [item["name"] for item in items]
    assert "item1" in item_names


@given("the following inventories exist")
def step_impl(context):
    """Ensure the specified inventories exist"""
    rest_endpoint = f"{context.base_url}/api/inventory"
    for row in context.table:
        payload = {
            "name": row["name"],
            "quantity": int(row["quantity"]),
            "price": float(row["price"]),
            "product_id": int(row["id"]),
            "restock_level": 1,  # Assuming default values for missing fields
            "condition": "new",  # Assuming default values for missing fields
        }
        context.resp = requests.post(rest_endpoint, json=payload, timeout=WAIT_TIMEOUT)
        assert context.resp.status_code == HTTP_201_CREATED
