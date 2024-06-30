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

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import InventoryItem
from service.common import status  # HTTP Status Codes


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Inventory REST API Service",
            version="1.0",
            paths={
                "health": url_for("health_check", _external=True),
                "create": url_for("create_inventory_item", _external=True),
                "list": url_for("list_inventory_items", _external=True),
            },
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW INVENTORY ITEM
######################################################################
@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    """
    Create an Inventory Item
    This endpoint will create an Inventory Item based on the data in the body that is posted
    """
    app.logger.info("Request to Create an Inventory Item...")
    check_content_type("application/json")

    item = InventoryItem()
    # Get the data from the request and deserialize it
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    item.deserialize(data)

    # Save the new Inventory Item to the database
    item.create()
    app.logger.info("Inventory Item with new id [%s] saved!", item.id)

    # Return the location of the new Inventory Item
    location_url = url_for("get_inventory_item", item_id=item.id, _external=True)
    return (
        jsonify(item.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# READ AN INVENTORY ITEM
######################################################################


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_items(item_id):
    """
    Retrieve a single Item

    This endpoint will return a Item based on it's id
    """
    app.logger.info("Request to Retrieve a item with id [%s]", item_id)

    # Attempt to find the Item and abort if not found
    item = InventoryItem.find(item_id)
    if not item:
        abort(status.HTTP_404_NOT_FOUND, f"Item with id '{item_id}' was not found.")

    app.logger.info("Returning item: %s", item.name)
    return jsonify(item.serialize()), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
