"""
TestInventoryItem API Service Test Suite
"""

import os
import logging
from decimal import Decimal
from urllib.parse import quote_plus

from service.common import status
from service.routes import validate_decimal

from tests.test_base import BaseTestCase
from .factories import InventoryItemFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/api/inventory"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestInventoryItemService(BaseTestCase):
    """REST API Server Tests"""

    ############################################################
    # Utility function to bulk create items
    ############################################################
    def _create_items(self, count: int = 1) -> list:
        """Factory method to create items in bulk"""
        items = []
        for _ in range(count):
            test_item = InventoryItemFactory()
            response = self.client.post(BASE_URL, json=test_item.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test item",
            )
            new_item = response.get_json()
            test_item.id = new_item["id"]
            items.append(test_item)
        return items

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_health_check(self):
        """It should return 200 OK with the correct JSON response"""
        response = self.client.get("/health")
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that the response JSON is {"status": "OK"}
        self.assertEqual(response.json, {"status": "OK"})

    def test_valid_decimal(self):
        """It should pass for valid decimal strings"""
        try:
            validate_decimal("123.45")
            validate_decimal("0.001")
            validate_decimal("-123.45")
        except ValueError:
            self.fail("validate_decimal() raised ValueError unexpectedly!")

    def test_invalid_decimal(self):
        """It should raise ValueError for invalid decimal strings"""
        with self.assertRaises(ValueError):
            validate_decimal("abc")
        with self.assertRaises(ValueError):
            validate_decimal("123.45.67")
        with self.assertRaises(ValueError):
            validate_decimal("")

    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(b"Inventory REST API Service", resp.data)

    def test_create_inventory_item(self):
        """It should Create a new Inventory Item"""
        test_item = InventoryItemFactory()
        logging.debug("Test Inventory Item: %s", test_item.serialize())
        response = self.client.post(BASE_URL, json=test_item.serialize())
        if response.status_code != status.HTTP_201_CREATED:
            logging.error("Response data: %s", response.get_json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_item = response.get_json()
        self.assertEqual(new_item["name"], test_item.name)
        self.assertEqual(new_item["quantity"], test_item.quantity)
        self.assertEqual(Decimal(new_item["price"]), test_item.price)
        self.assertEqual(new_item["product_id"], test_item.product_id)
        self.assertEqual(new_item["condition"], test_item.condition)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_item = response.get_json()
        self.assertEqual(new_item["name"], test_item.name)
        self.assertEqual(new_item["quantity"], test_item.quantity)
        self.assertEqual(Decimal(new_item["price"]), test_item.price)
        self.assertEqual(new_item["product_id"], test_item.product_id)
        self.assertEqual(new_item["condition"], test_item.condition)

    def test_create_inventory_item_no_data(self):
        """It should not Create an Inventory Item with no data"""
        resp = self.client.post("/api/inventory", json={}, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_inventory_item_bad_data(self):
        """It should not Create an Inventory Item with bad data"""
        resp = self.client.post(
            "/api/inventory",
            json={"name": "Widget", "quantity": "one hundred"},
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # ----------------------------------------------------------
    # TEST READ
    # ----------------------------------------------------------
    def test_get_item(self):
        """It should Get a single Item"""
        # get the id of a item
        test_item = self._create_items(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_item.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_item.name)
        self.assertEqual(data["description"], test_item.description)
        self.assertEqual(data["quantity"], test_item.quantity)
        self.assertEqual(Decimal(data["price"]), test_item.price)
        self.assertEqual(data["product_id"], test_item.product_id)
        self.assertEqual(data["restock_level"], test_item.restock_level)
        self.assertEqual(data["condition"], test_item.condition)

    def test_get_item_not_found(self):
        """It should not Get a Item thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    # ----------------------------------------------------------
    # TEST UPDATE
    # ----------------------------------------------------------
    def test_update_item(self):
        """It should Update an existing Item"""
        # create an item to update
        test_item = InventoryItemFactory()
        response = self.client.post(BASE_URL, json=test_item.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the item
        new_item = response.get_json()
        logging.debug(new_item)
        new_item["condition"] = "used"
        response = self.client.put(f"{BASE_URL}/{new_item['id']}", json=new_item)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_item = response.get_json()
        self.assertEqual(updated_item["condition"], "used")

    # ----------------------------------------------------------
    # TEST Delete
    # ----------------------------------------------------------
    def test_delete_inventory(self):
        """It should Delete an Inventory"""
        test_inventory = self._create_items(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_inventory(self):
        """It should Delete an inventory even if it doesn't exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

    # ----------------------------------------------------------
    # TEST Decrement the quantity of an inventory item
    # ----------------------------------------------------------

    def test_decrement_an_inventory_item_quantity(self):
        """It should decrement the quantity of an inventory item"""
        test_inventory = self._create_items(1)[0]
        response = self.client.put(f"{BASE_URL}/{test_inventory.id}/decrement")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_inventory.name)
        self.assertEqual(data["description"], test_inventory.description)
        if test_inventory.quantity > 0:
            self.assertEqual(data["quantity"], (test_inventory.quantity - 1))
        else:
            self.assertEqual(data["quantity"], test_inventory.quantity)
        self.assertEqual(Decimal(data["price"]), test_inventory.price)
        self.assertEqual(data["product_id"], test_inventory.product_id)
        self.assertEqual(data["restock_level"], test_inventory.restock_level)
        self.assertEqual(data["condition"], test_inventory.condition)

    def test_decrement_inventory_item_count_below_zero(self):
        """Test decrementing the inventory item count below zero"""
        new_obj = InventoryItemFactory()
        response = self.client.post(BASE_URL, json=new_obj.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        item = response.get_json()
        item["quantity"] = 0
        response = self.client.put(f"{BASE_URL}/{item['id']}", json=item)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Decrement the inventory item count
        response = self.client.put(f"{BASE_URL}/{item['id']}/decrement")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        data = response.get_json()
        self.assertEqual(data["quantity"], 0)

    def test_item_not_found(self):
        """It should return 404 Not Found when the item does not exist"""
        non_existent_id = 99999  # Assuming this ID does not exist in your test database

        # Simulate the PUT request to decrement an item that does not exist
        response = self.client.put(f"/api/inventory/{non_existent_id}/decrement")

        # Assert that the response status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Optionally, check the error message returned
        expected_message = f"Item with id '{non_existent_id}' was not found."
        self.assertIn(expected_message, response.json['message'])

    # ----------------------------------------------------------
    # TEST ARCHIVE ITEM (new action endpoint)
    # ----------------------------------------------------------
    def test_archive_item(self):
        """It should Archive an existing Item"""
        # create an item to archive
        test_item = self._create_items(1)[0]
        response = self.client.put(f"{BASE_URL}/{test_item.id}/archive")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        archived_item = response.get_json()
        self.assertEqual(archived_item["condition"], "archived")

    def test_archive_item_not_found(self):
        """It should not Archive an Item that is not found"""
        response = self.client.put(f"{BASE_URL}/0/archive")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("was not found", data["message"])

    def test_archive_item_already_archived(self):
        """It should not Archive an Item that is already archived"""
        test_item = self._create_items(1)[0]
        # Archive the item
        response = self.client.put(f"{BASE_URL}/{test_item.id}/archive")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to archive it again
        response = self.client.put(f"{BASE_URL}/{test_item.id}/archive")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.get_json()
        self.assertIn("Item is already archived", data["message"])

    # ----------------------------------------------------------
    # TEST LIST
    # ----------------------------------------------------------
    def test_get_item_list(self):
        """It should Get a list of InevntoryItems"""
        self._create_items(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    # ----------------------------------------------------------
    # TEST QUERY
    # ----------------------------------------------------------
    def test_query_by_name(self):
        """It should Query InventoryItems by name"""
        items = self._create_items(5)
        test_name = items[0].name
        name_count = len([item for item in items if item.name == test_name])
        response = self.client.get(
            BASE_URL, query_string=f"name={quote_plus(test_name)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)
        # check the data just to be sure
        for item in data:
            self.assertEqual(item["name"], test_name)

    def test_query_by_condition(self):
        """It should Query InventoryItems by condition"""
        items = self._create_items(5)
        test_condition = items[0].condition
        condition_count = len(
            [item for item in items if item.condition == test_condition]
        )
        response = self.client.get(
            BASE_URL, query_string=f"condition={quote_plus(test_condition)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), condition_count)
        # check the data just to be sure
        for item in data:
            self.assertEqual(item["condition"], test_condition)

    def test_query_by_id(self):
        """It should Query InventoryItems by id"""
        items = self._create_items(5)
        test_id = items[0].id
        test_id_str = str(test_id)
        id_count = len([item for item in items if item.id == test_id_str])
        response = self.client.get(
            BASE_URL, query_string=f"name={quote_plus(test_id_str)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), id_count)
        # check the data just to be sure
        for item in data:
            self.assertEqual(item["id"], test_id)


######################################################################
#  T E S T   S A D   P A T H S
######################################################################


class TestSadPaths(BaseTestCase):
    """Test REST Exception Handling"""

    def test_method_not_allowed(self):
        """It should not allow update without a item id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_item_no_data(self):
        """It should not Create an InventoryItem with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_no_content_type(self):
        """It should not Create a InventoryItem with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_item_wrong_content_type(self):
        """It should not Create a InventoryItem with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_item_bad_available(self):
        """It should not Create a InventoryItem with bad available data"""
        test_item = InventoryItemFactory()
        logging.debug(test_item)
        # change condition to a number
        test_item.condition = 69
        response = self.client.post(BASE_URL, json=test_item.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_item_not_found(self):
        """It should return 404 Not Found when the item does not exist"""
        non_existent_id = 9999  # Assuming this ID does not exist in test database
        response = self.client.get(f"{BASE_URL}/{non_existent_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
