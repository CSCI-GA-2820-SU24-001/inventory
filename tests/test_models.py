"""
Test cases for InventoryItem Model
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import InventoryItem, DataValidationError, db
from tests.factories import InventoryItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  I N V E N T O R Y   M O D E L   T E S T   C A S E S
######################################################################
class TestCaseBase(TestCase):
    """Test Cases for InventoryItem Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(InventoryItem).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()


######################################################################
#  Inventory Item   M O D E L   T E S T   C A S E S
######################################################################
class TestInventoryItemModel(TestCaseBase):
    """Inventory Item Model CRUD Tests"""

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_an_inventory_item(self):
        """It should Create an Inventory Item and assert that it exists"""
        item = InventoryItem(
            name="Widget", quantity=100, price=10.99, product_id=1, condition="new"
        )
        self.assertEqual(str(item), "<InventoryItem Widget id=[None]>")
        self.assertTrue(item is not None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.name, "Widget")
        self.assertEqual(item.quantity, 100)
        self.assertEqual(item.price, 10.99)
        self.assertEqual(item.product_id, 1)
        self.assertEqual(item.condition, "new")

    def test_read_a_item(self):
        """It should Read a Item"""
        item = InventoryItemFactory()
        logging.debug(item)
        item.id = None
        item.create()
        self.assertIsNotNone(item.id)
        # Fetch it back
        found_item = InventoryItem.find(item.id)
        self.assertEqual(found_item.id, item.id)
        self.assertEqual(found_item.name, item.name)

    def test_update_no_id(self):
        """It should not Update an Inventory Item with no id"""
        item = InventoryItemFactory()
        logging.debug(item)
        item.id = None
        self.assertRaises(DataValidationError, item.update)

    def test_serialize_an_inventory_item(self):
        """It should serialize an Inventory Item"""
        item = InventoryItemFactory()
        data = item.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], item.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], item.name)
        self.assertIn("quantity", data)
        self.assertEqual(data["quantity"], item.quantity)
        self.assertIn("price", data)
        self.assertEqual(data["price"], item.price)
        self.assertIn("product_id", data)
        self.assertEqual(data["product_id"], item.product_id)
        self.assertIn("condition", data)
        self.assertEqual(data["condition"], item.condition)

    def test_deserialize_an_inventory_item(self):
        """It should de-serialize an Inventory Item"""
        data = InventoryItemFactory().serialize()
        item = InventoryItem()
        item.deserialize(data)
        self.assertNotEqual(item, None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.name, data["name"])
        self.assertEqual(item.quantity, data["quantity"])
        self.assertEqual(item.price, data["price"])
        self.assertEqual(item.product_id, data["product_id"])
        self.assertEqual(item.condition, data["condition"])

    def test_deserialize_missing_data(self):
        """It should not deserialize an Inventory Item with missing data"""
        data = {"name": "Widget", "quantity": 100}
        item = InventoryItem()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        item = InventoryItem()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_bad_quantity(self):
        """It should not deserialize a bad quantity attribute"""
        test_item = InventoryItemFactory()
        data = test_item.serialize()
        data["quantity"] = "one hundred"
        item = InventoryItem()
        self.assertRaises(DataValidationError, item.deserialize, data)
