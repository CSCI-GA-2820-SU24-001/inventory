"""
Models for YourResourceModel

All of the models are stored in this module

Models
------
InventoryItem - An item in the inventory

Attributes:
-----------
name (string) - the name of the item
description (string) - the description of the item
quantity (integer) - the quantity of the item in stock
price (Numeric) - the price of the item
product_id (integer) - the id of the product
restock_level (integer) - the level at which restocking is needed
condition (string) - the condition of the item (new, open box, used, archived)

"""

import os
import logging
from enum import Enum
from decimal import Decimal, InvalidOperation
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric

# Global variables for retry (must be int)
RETRY_COUNT = int(os.environ.get("RETRY_COUNT", 5))
RETRY_DELAY = int(os.environ.get("RETRY_DELAY", 1))
RETRY_BACKOFF = int(os.environ.get("RETRY_BACKOFF", 2))

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Condition(Enum):
    """Enumeration of valid Inventory Item Conditions"""

    NEW = "new"
    OPEN_BOX = "open box"
    USED = "used"
    ARCHIVED = "archived"


class InventoryItem(db.Model):  # pylint: disable=too-many-instance-attributes
    """
    Class that represents an InventoryItem

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(Numeric(8, 2), nullable=False)  # Updated to Numeric
    product_id = db.Column(db.Integer, nullable=False)
    restock_level = db.Column(db.Integer)
    condition = db.Column(db.String(15))

    def __repr__(self):
        return f"<InventoryItem {self.name} id=[{self.id}]>"

    def create(self) -> None:
        """
        Creates a YourResourceModel to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self) -> None:
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self) -> None:
        """Removes a YourResourceModel from the data store"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self) -> dict:
        """Serializes an InventoryItem into a dictionary"""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "quantity": self.quantity,
            "price": str(self.price.quantize(Decimal(".01"))),
            "product_id": self.product_id,
            "restock_level": self.restock_level,
            "condition": self.condition,
        }

    def deserialize(self, data: dict):
        """
        Deserializes an InventoryItem from a dictionary
        Args:
            data (dict): A dictionary containing the InventoryItem data
        """
        try:
            self.name = data["name"]
            self.description = data.get("description")
            self.quantity = self._validate_quantity(data["quantity"])
            self.price = self._validate_price(data["price"])
            self.product_id = self._validate_product_id(data["product_id"])
            self.restock_level = self._validate_restock_level(data.get("restock_level"))
            self.condition = self._validate_condition(data.get("condition"))
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid InventoryItem: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid InventoryItem: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    def _validate_quantity(self, quantity):
        if isinstance(quantity, int):
            return quantity
        raise DataValidationError(
            "Invalid type for integer [quantity]: " + str(type(quantity))
        )

    def _validate_price(self, price):
        try:
            return Decimal(price)
        except InvalidOperation as error:  # Catch the correct exception
            raise DataValidationError(
                f"Invalid type for decimal [price]: {error}"
            ) from error

    def _validate_product_id(self, product_id):
        if isinstance(product_id, int):
            return product_id
        raise DataValidationError(
            "Invalid type for integer [product_id]: " + str(type(product_id))
        )

    def _validate_restock_level(self, restock_level):
        if restock_level is not None:
            if isinstance(restock_level, int):
                return restock_level
            raise DataValidationError(
                "Invalid type for integer [restock_level]: " + str(type(restock_level))
            )
        return None

    def _validate_condition(self, condition):
        if condition is not None:
            if condition in ["new", "open box", "used", "archived"]:
                return condition
            raise DataValidationError(
                "Invalid value for [condition]: " + str(condition)
            )
        return None

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls) -> list:
        """Returns all of the InventoryItems in the database"""
        logger.info("Processing all InventoryItems")
        return cls.query.all()

    @classmethod
    def find(cls, item_id: int):
        """Finds an InventoryItem by its ID

        :param item_id: the id of the InventoryItem to find
        :type item_id: int

        :return: an instance with the item_id, or None if not found
        :rtype: InventoryItem
        """
        logger.info("Processing lookup for id %s ...", item_id)
        return cls.query.filter(cls.id == item_id).first()

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all InventoryItems with the given name

        :param name: the name of the InventoryItems you want to match
        :type name: str

        :return: a collection of InventoryItems with that name
        :rtype: list
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_condition(cls, condition: str) -> list:
        """Returns all of the Items in a condition

        :param condition: the condition of the Items you want to match
        :type condition: str

        :return: a collection of Items in that condition
        :rtype: list

        """
        logger.info("Processing condition query for %s ...", condition)
        return cls.query.filter(cls.condition == condition)
