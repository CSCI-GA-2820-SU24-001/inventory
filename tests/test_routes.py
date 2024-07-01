"""
TestInventoryItem API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, InventoryItem
from .factories import InventoryItemFactory


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/inventory"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestInventoryItemService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(InventoryItem).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

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

    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertIn("name", data)
        self.assertEqual(data["name"], "Inventory REST API Service")

    def test_create_inventory_item(self):
        """It should Create a new Pet"""
        test_item = InventoryItemFactory()
        logging.debug("Test Pet: %s", test_item.serialize())
        response = self.client.post(BASE_URL, json=test_item.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_item = response.get_json()
        self.assertEqual(new_item["name"], test_item.name)
        self.assertEqual(new_item["quantity"], test_item.quantity)
        self.assertEqual(new_item["price"], test_item.price)
        self.assertEqual(new_item["product_id"], test_item.product_id)
        self.assertEqual(new_item["condition"], test_item.condition)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_item = response.get_json()
        self.assertEqual(new_item["name"], test_item.name)
        self.assertEqual(new_item["quantity"], test_item.quantity)
        self.assertEqual(new_item["price"], test_item.price)
        self.assertEqual(new_item["product_id"], test_item.product_id)
        self.assertEqual(new_item["condition"], test_item.condition)

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
        self.assertEqual(data["price"], test_item.price)
        self.assertEqual(data["product_id"], test_item.product_id)
        self.assertEqual(data["restock_level"], test_item.restock_level)
        self.assertEqual(data["condition"], test_item.condition)


    # def test_get_item_not_found(self):
    #     """It should not Get a Item thats not found"""
    #     response = self.client.get(f"{BASE_URL}/0")
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     data = response.get_json()
    #     logging.debug("Response data = %s", data)
    #     self.assertIn("was not found", data["message"])
