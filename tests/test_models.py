"""
Test cases for InventoryItem Model
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch
from wsgi import app
from service.models import InventoryItem, DataValidationError, db
from tests.factories import InventoryItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  I N V E N T O R Y   M O D E L   T E S T   C A S E S
######################################################################
class TestInventoryItemModel(TestCase):
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
        item = InventoryItem(
            name="Scissors",
            quantity=1000000,
            price=0.88,
            product_id=2,
            condition="used",
        )
        self.assertEqual(str(item), "<InventoryItem Scissors id=[None]>")
        self.assertTrue(item is not None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.name, "Scissors")
        self.assertEqual(item.quantity, 1000000)
        self.assertEqual(item.price, 0.88)
        self.assertEqual(item.product_id, 2)
        self.assertEqual(item.condition, "used")

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

    def test_update_a_item(self):
        """It should Update an item"""
        item = InventoryItemFactory()
        logging.debug(item)
        item.id = None
        item.create()
        logging.debug(item)
        self.assertIsNotNone(item.id)
        # Change it an save it
        item.condition = "new"
        item.price = 20
        original_id = item.id
        item.update()
        self.assertEqual(item.id, original_id)
        self.assertEqual(item.condition, "new")
        self.assertEqual(item.price, 20)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        item = InventoryItem.all()
        self.assertEqual(len(item), 1)
        self.assertEqual(item[0].id, original_id)
        self.assertEqual(item[0].condition, "new")

    def test_update_no_id(self):
        """It should not Update an Inventory Item with no id"""
        item = InventoryItemFactory()
        logging.debug(item)
        item.id = None
        self.assertRaises(DataValidationError, item.update)

    def test_list_all_inventory_items(self):
        """It should List all Inventory Items in the database"""
        items = InventoryItem.all()
        self.assertEqual(items, [])
        # Create 5 Inventory Items
        for _ in range(5):
            item = InventoryItemFactory()
            item.create()
        # See if we get back 5 inventory items
        items = InventoryItem.all()
        self.assertEqual(len(items), 5)

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
        data["quantity"] = "one hundred"  # Invalid quantity
        item = InventoryItem()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_bad_price(self):
        """It should not deserialize a bad price attribute"""
        test_item = InventoryItemFactory()
        data = test_item.serialize()
        data["price"] = "ten dollars"  # Invalid price
        item = InventoryItem()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_bad_product_id(self):
        """It should not deserialize a bad product_id attribute"""
        test_item = InventoryItemFactory()
        data = test_item.serialize()
        data["product_id"] = "invalid_id"  # Invalid product_id
        item = InventoryItem()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_bad_restock_level(self):
        """It should not deserialize a bad restock_level attribute"""
        test_item = InventoryItemFactory()
        data = test_item.serialize()
        data["restock_level"] = "fifty"  # Invalid restock_level
        item = InventoryItem()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_bad_condition(self):
        """It should not deserialize a bad condition attribute"""
        test_item = InventoryItemFactory()
        data = test_item.serialize()
        data["condition"] = "excellent"  # Invalid condition
        item = InventoryItem()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_delete_an_inventory(self):
        """It should Delete an Inventory"""
        inventory = InventoryItemFactory()
        inventory.create()
        self.assertEqual(len(InventoryItem.all()), 1)
        # delete the inventory and make sure it isn't in the database
        inventory.delete()
        self.assertEqual(len(InventoryItem.all()), 0)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestInventoryItemModel):
    """Item Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        item = InventoryItemFactory()
        self.assertRaises(DataValidationError, item.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        item = InventoryItemFactory()
        self.assertRaises(DataValidationError, item.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        item = InventoryItemFactory()
        self.assertRaises(DataValidationError, item.delete)


######################################################################
#  Q U E R Y   T E S T   C A S E S
######################################################################
class TestModelQueries(TestInventoryItemModel):
    """Inventory Item Model Query Tests"""

    def test_find_item(self):
        """It should Find an Inventory item by ID"""
        items = InventoryItemFactory.create_batch(5)
        for item in items:
            item.create()
        logging.debug(items)
        # make sure they got saved
        self.assertEqual(len(InventoryItem.all()), 5)
        # find the 2nd item in the list
        item = InventoryItem.find(items[1].id)
        self.assertIsNot(item, None)
        self.assertEqual(item.id, items[1].id)
        self.assertEqual(item.name, items[1].name)
        self.assertEqual(item.description, items[1].description)
        self.assertEqual(item.quantity, items[1].quantity)
        self.assertEqual(item.price, items[1].price)
        self.assertEqual(item.product_id, items[1].product_id)
        self.assertEqual(item.restock_level, items[1].restock_level)
        self.assertEqual(item.condition, items[1].condition)

    def test_find_by_name(self):
        """It should Find a InventoryItem by Name"""
        items = InventoryItemFactory.create_batch(10)
        for item in items:
            item.create()
        name = items[0].name
        count = len([item for item in items if item.name == name])
        found = InventoryItem.find_by_name(name)
        self.assertEqual(found.count(), count)
        for item in found:
            self.assertEqual(item.name, name)

    def test_find_by_condition(self):
        """It should Find InventoryItems by Category"""
        items = InventoryItemFactory.create_batch(10)
        for item in items:
            item.create()
        condition = items[0].condition
        count = len([item for item in items if item.condition == condition])
        found = InventoryItem.find_by_condition(condition)
        self.assertEqual(found.count(), count)
        for item in found:
            self.assertEqual(item.condition, condition)

    # def test_find_by_price(self):
    #     """It should Find InventoryItems by price"""
    #     items = InventoryItemFactory.create_batch(10)
    #     for item in items:
    #         item.create()
    #     price = items[0].price
    #     count = len([item for item in items if item.price == price])
    #     found = InventoryItem.find_by_price(price)
    #     self.assertEqual(found.count(), count)
    #     for item in found:
    #         self.assertEqual(item.price, price)
