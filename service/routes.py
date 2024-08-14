######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Inventory Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Inventory items.
"""

from decimal import Decimal, InvalidOperation
from flask import current_app as app  # Import Flask application
from flask_restx import Resource, reqparse, fields
from service.models import InventoryItem
from service.common import status  # HTTP Status Codes
from . import api


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return {"status": "OK"}, status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL for Inventory Service"""
    app.logger.info("Request for Root URL")
    return app.send_static_file("index.html")


def validate_decimal(value):
    """
    Validates that the given value can be converted to a Decimal.

    Args:
        value: The value to validate.

    Raises:
        ValueError: If the value cannot be converted to a Decimal.
    """
    try:
        Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{value} is not a valid decimal number") from exc


# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "InventoryItem",
    {
        "id": fields.Integer(required=True, description="ID of the product"),
        "name": fields.String(required=True, description="The name of the inventory item"),
        "description": fields.String(required=True, description="The description of the inventory item"),
        "quantity": fields.Integer(
            required=True, description="Quantity of inventory item"
        ),
        "price": fields.String(required=True, description="Price of the product", validate=validate_decimal),
        "product_id": fields.Integer(required=True, description="ID of the product"),
        "restock_level": fields.Integer(
            required=True, description="Restock level of inventory item"
        ),
        "condition": fields.String(
            required=True,
            description="The condition of the inventory item (e.g., new, open box, used, archived.)",
        ),
    },
)

inventoryItem_model = api.inherit(
    "InventoryItem",
    create_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
        "product_id": fields.Integer(
            readOnly=True, description="Product id "
        ),
    },
)

# query string arguments
inventoryItem_args = reqparse.RequestParser()
inventoryItem_args.add_argument(
    "name", type=str, location="args", required=False, help="List InventoryItems by name"
)
inventoryItem_args.add_argument(
    "condition", type=str, location="args", required=False, help="List InventoryItems by condition"
)
inventoryItem_args.add_argument(
    "id",
    type=int,
    location="args",
    required=False,
    help="List InventoryItems by it's id",
)

######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
#  PATH: /inventory/{id}
######################################################################
@api.route("/inventory/<int:item_id>")
@api.param("item_id", "The InventoryItem identifier")
class InventoryItemResource(Resource):
    """
    InventoryItemResource class

    Allows the manipulation of a single inventory item
    GET /item{id} - Returns an item with the id
    PUT /item{id} - Update an item with the id
    DELETE /item{id} -  Deletes an item with the id
    """
    # ------------------------------------------------------------------
    # RETRIEVE AN ITEM
    # ------------------------------------------------------------------
    @api.doc("get_inventory_items")
    @api.response(404, "Item not found")
    @api.marshal_with(inventoryItem_model)
    def get(self, item_id):
        """
        Retrieve a single inventory item

        This endpoint will return a item based on it's id
        """
        app.logger.info("Request to Retrieve a item with id [%s]", item_id)

        # Attempt to find the Item and abort if not found
        item = InventoryItem.find(item_id)
        if not item:
            error(status.HTTP_404_NOT_FOUND, f"Item with id '{item_id}' was not found.")

        app.logger.info("Returning item: %s", item.name)
        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING ITEM
    # ------------------------------------------------------------------

    @api.doc("update_inventory_items")
    @api.response(404, "Item not found")
    @api.response(400, "The posted item data was not valid")
    @api.expect(inventoryItem_model)
    @api.marshal_with(inventoryItem_model)
    def put(self, item_id):
        """
        Update an item

        This endpoint will update an item based the body that is posted
        """
        app.logger.info("Request to Update an item with id [%s]", item_id)

        # Attempt to find the item and abort if not found
        item = InventoryItem.find(item_id)
        if not item:
            error(status.HTTP_404_NOT_FOUND, f"Item with id '{item_id}' was not found.")

        # Update the Item with the new data
        data = api.payload
        app.logger.info("Processing: %s", data)
        item.deserialize(data)

        # Save the updates to the database
        item.update()

        app.logger.info("Item with ID: %d updated.", item.id)
        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ITEM
    # ------------------------------------------------------------------

    @api.doc("delete_inventory_items")
    @api.response(204, "Item deleted")
    def delete(self, item_id):

        """
        Delete an Inventory Item

        This endpoint will delete an Inventory Item based the id specified in the path
        """
        app.logger.info("Request to Delete an inventory with id [%s]", item_id)

        # Delete the Inventory if it exists
        item = InventoryItem.find(item_id)
        if item:
            app.logger.info("Inventory with ID: %d found.", item_id)
            item.delete()
            app.logger.info("Inventory with ID: %d delete complete.", item_id)
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /inventory
######################################################################

@api.route("/inventory", strict_slashes=False)
class InventoryItemCollection(Resource):
    """Handles all interactions with collections of InventoryItems"""

    # ------------------------------------------------------------------
    # LIST ALL ITEMS
    # ------------------------------------------------------------------

    @api.doc("list_inventory_items")
    @api.expect(inventoryItem_args, validate=True)
    @api.marshal_list_with(inventoryItem_model)
    def get(self):
        """Returns all of the Inventory Items"""
        app.logger.info("Request for inventory item list")
        items = []
        args = inventoryItem_args.parse_args()
        if args["condition"]:
            app.logger.info("Filtering by condition: %s", args["condition"])
            items = InventoryItem.find_by_condition(args["condition"])
        elif args["name"]:
            app.logger.info("Filtering by name: %s", args["name"])
            items = InventoryItem.find_by_name(args["name"])
        elif args["id"]:
            app.logger.info("Filtering by id: %s", args["id"])
            items = InventoryItem.find(args["id"])
        else:
            app.logger.info("Returning unfiltered list.")
            items = InventoryItem.all()

        results = [item.serialize() for item in items]
        app.logger.info("[%d] Inventory items returned", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ITEM
    # ------------------------------------------------------------------

    @api.doc("create_inventory_items")
    @api.response(400, "The posted data was not valid")
    @api.expect(create_model)
    @api.marshal_with(inventoryItem_model, code=201)
    def post(self):
        """
        Creates an item
        This endpoint will create a Inventory item based the data in the body that is posted
        """
        app.logger.info("Request to Create an Item")
        item = InventoryItem()
        app.logger.debug("Payload = %s", api.payload)
        item.deserialize(api.payload)
        item.create()
        app.logger.info("Inventory Item with new id [%s] saved!", item.id)
        location_url = api.url_for(InventoryItemResource, item_id=item.id, _external=True)
        return item.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /inventory/{id}/archive
######################################################################
@api.route("/inventory/<int:item_id>/archive")
@api.param("item_id", "The InventoryItem identifier")
class ArchiveResource(Resource):
    """Archive action on a item"""

    @api.doc("archive_items")
    @api.response(404, "Item not found")
    @api.response(409, "The Item is not available to archive")
    def put(self, item_id):
        """
        Archive an item

        This endpoint will mark an item as archived based on the id specified in the path
        """
        app.logger.info("Request to archive item with id [%s]", item_id)
        # Find the item and abort if not found
        item = InventoryItem.find(item_id)
        if not item:
            error(status.HTTP_404_NOT_FOUND, f"Item with id '{item_id}' was not found.")

        if item.condition == "archived":
            error(status.HTTP_400_BAD_REQUEST, "Item is already archived.")
        item.condition = "archived"
        item.update()
        app.logger.info("Item with ID: %d archived.", item.id)
        return item.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /inventory/{id}/decrement
######################################################################

@api.route("/inventory/<int:item_id>/decrement")
@api.param("item_id", "The InventoryItem identifier")
class DecrementResource(Resource):
    """Decrement actions on a Inventory item"""

    @api.doc("decrement_items")
    @api.response(404, "Item not found")
    @api.response(409, "The item is not there to decrement")
    def put(self, item_id):
        """
        Decrement an inventory item quantity

        This endpoint will decrement an Inventory item's quantity based the id specified in the path
        """
        app.logger.info(
            "Request to decrement the quantity of an inventory with id [%s]", item_id
        )
        item = InventoryItem.find(item_id)

        if not item:
            error(
                status.HTTP_404_NOT_FOUND, f"Item with id '{item_id}' was not found."
            )

        # decrement the current quantity for this item
        item.quantity -= 1
        item.quantity = max(item.quantity, 0)

        item.update()

        if item.quantity < item.restock_level:
            trigger_insufficient_product_notification(item)
        app.logger.info("The quantity of the item with ID: %d decremented.", item.id)
        return item.serialize(), status.HTTP_200_OK


######################################################################
# TRIGGER AN NOTIFICATION OF INSUFFICIENT ITEM
######################################################################
def trigger_insufficient_product_notification(item):
    """
    This function will be called only if the current inventory item's quantity is less than
    the restock_level
    """
    print(
        f"Notification: The product '{item.name}' (ID: {item.id}) is below restock level. Current count: {item.quantity}"
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

# ------------------------------------------------------------------
# Logs error messages before aborting
# ------------------------------------------------------------------
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    api.abort(status_code, reason)
