"""
TestInventoryItem API Service Test Suite
"""
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, InventoryItem
from tests.factories import InventoryItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestInventoryItemService(TestCase):
    """ REST API Server Tests """

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
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertIn("name", data)
        self.assertEqual(data["name"], "Inventory REST API Service")

    def test_create_inventory_item(self):
        """It should Create a new Inventory Item"""
        item = InventoryItemFactory()
        logging.debug(item)
        resp = self.client.post(
            "/inventory",
            json=item.serialize(),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        location = resp.headers.get("Location")
        self.assertIsNotNone(location)

        # Check the location header
        resp = self.client.get(location)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_item = resp.get_json()
        self.assertEqual(new_item["name"], item.name)
        self.assertEqual(new_item["quantity"], item.quantity)
        self.assertEqual(new_item["price"], item.price)
        self.assertEqual(new_item["product_id"], item.product_id)
        self.assertEqual(new_item["condition"], item.condition)

    def test_create_inventory_item_no_data(self):
        """It should not Create an Inventory Item with no data"""
        resp = self.client.post(
            "/inventory",
            json={},
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_inventory_item_bad_data(self):
        """It should not Create an Inventory Item with bad data"""
        resp = self.client.post(
            "/inventory",
            json={"name": "Widget", "quantity": "one hundred"},
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
