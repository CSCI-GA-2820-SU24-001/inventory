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
price (float) - the price of the item
product_id (integer) - the id of the product
restock_level (integer) - the level at which restocking is needed
condition (string) - the condition of the item (new, open box, used)

"""

import os
import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

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


class InventoryItem(db.Model):
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
    price = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    restock_level = db.Column(db.Integer)
    condition = db.Column(db.String(15))

    def __repr__(self):
        return f"<InventoryItem {self.name} id=[{self.id}]>"

    def create(self):
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

    def update(self):
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.name)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
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
            "price": self.price,
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
            
            # Check and convert quantity
            if isinstance(data["quantity"], int):
                self.quantity = data["quantity"]
            else:
                raise DataValidationError(
                    "Invalid type for integer [quantity]: " + str(type(data["quantity"]))
                )
            
            # Check and convert price
            if isinstance(data["price"], float):
                self.price = float(data["price"])
            else:
                raise DataValidationError(
                    "Invalid type for float [price]: " + str(type(data["price"]))
                )
            
            # Check product_id
            if isinstance(data["product_id"], int):
                self.product_id = data["product_id"]
            else:
                raise DataValidationError(
                    "Invalid type for integer [product_id]: " + str(type(data["product_id"]))
                )

            # Check restock_level
            restock_level = data.get("restock_level")
            if restock_level is not None:
                if isinstance(restock_level, int):
                    self.restock_level = restock_level
                else:
                    raise DataValidationError(
                        "Invalid type for integer [restock_level]: " + str(type(restock_level))
                    )
            
            # Check condition
            condition = data.get("condition")
            if condition is not None:
                if condition in ["new", "open box", "used"]:
                    self.condition = condition
                else:
                    raise DataValidationError(
                        "Invalid value for [condition]: " + str(condition)
                    )
            else:
                self.condition = None
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
        return cls.query.session.get(cls, item_id)

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
