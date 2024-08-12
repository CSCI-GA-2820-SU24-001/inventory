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

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import logging
import requests
from behave import when, then  # pylint: disable=no-name-in-module
from selenium.common.exceptions import TimeoutException  # Add this import
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ID_PREFIX = "product_"
WAIT_TIMEOUT = 60  # 60 seconds timeout
# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_404_NOT_FOUND = 404


@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.driver.get(context.base_url)
    WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the document title for a message"""
    actual_title = context.driver.title
    print(f"Actual title: {actual_title}")  # Debug print statement
    assert message in actual_title


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, "body")
    assert text_string not in element.text


@then('I should see "{expected_value}" in the "Description" field')
def step_impl(context, expected_value):
    element_id = ID_PREFIX + "description"
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), expected_value)
    )
    assert found, f"Expected value '{expected_value}' not found in 'Description' field"


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    print(f"Looking for element with ID: {element_id}")  # Debug print statement
    element = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    print(f"Found element with ID: {element_id}")  # Debug print statement
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    print(f"Looking for element with ID: {element_id}")  # Debug print statement
    element = Select(
        WebDriverWait(context.driver, 20).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
    )
    print(f"Found element with ID: {element_id}")  # Debug print statement
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(
        WebDriverWait(context.driver, 20).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
    )
    assert element.first_selected_option.text == text


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    assert (
        element.get_attribute("value") == ""
    ), f"Expected {element_name} field to be empty, but it was not."


# Repeat this pattern for other field checks


##################################################################
# These two functions simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    try:
        element = WebDriverWait(context.driver, 120).until(
            EC.presence_of_element_located((By.ID, element_name))
        )
        context.clipboard = element.get_attribute("value")
        print(f"Clipboard contains: {context.clipboard}")
    except TimeoutException:
        raise AssertionError(f"Failed to find the element with ID: {element_name}")


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    try:
        element = WebDriverWait(context.driver, 120).until(
            EC.presence_of_element_located((By.ID, element_name))
        )
        element.clear()
        element.send_keys(context.clipboard)
    except TimeoutException:
        raise AssertionError(f"Failed to find the element with ID: {element_name}")


##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html that is the button text
# in lowercase followed by '-btn' so the Clear button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################


@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower().replace(" ", "-") + "-btn"  # Corrected ID format
    print(f"Looking for button with ID: {button_id}")  # Debug print statement
    WebDriverWait(context.driver, 30).until(
        EC.element_to_be_clickable((By.ID, button_id))
    ).click()
    print(f"Clicked button with ID: {button_id}")  # Debug print statement


@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), name)
    )
    assert found


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element(By.ID, "search_results")
    search_results = element.text.split("\n")

    print(f"Search Results:\n{search_results}")  # Debugging output

    for result in search_results:
        # Ensure 'name' is not a part of any complete entry
        if (
            name.lower() == result.split()[1].lower()
        ):  # Assuming the second word in the line is the name
            raise AssertionError(
                f"Found '{name}' in search results, but it should not be present."
            )


@then('I should see the message "{message}"')
def step_impl(context, message):
    try:
        found = WebDriverWait(context.driver, 120).until(
            EC.visibility_of_element_located((By.ID, "flash_message"))
        )
        actual_message = found.text.strip()
        expected_message = message.strip()
        print(f"Actual message found: '{actual_message}'")  # Debugging statement
        assert (
            expected_message.lower() in actual_message.lower()
        ), f"Expected message '{expected_message}' but got '{actual_message}'"
    except TimeoutException:
        raise AssertionError(
            f"Failed to find the message '{message}' within the timeout period."
        )


@then(
    'I should see the specific error message "Item is already archived."'
)
def step_impl(context):
    try:
        # Wait for the flash message to appear
        found = WebDriverWait(context.driver, 120).until(
            EC.visibility_of_element_located((By.ID, "flash_message"))
        )
        actual_message = found.text.strip()
        expected_message = "Item is already archived."
        print(f"Actual message found: '{actual_message}'")  # Debugging statement
        assert (
            expected_message in actual_message
        ), f"Expected message '{expected_message}' but got '{actual_message}'"
    except TimeoutException:
        raise AssertionError(
            f"Failed to find the message '{expected_message}' within the timeout period."
        )


@then("I should see at least the following items in the results")
def step_impl(context):
    # Find the search results table
    table = WebDriverWait(context.driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )

    # Get all rows from the results table
    table_rows = table.find_elements(By.TAG_NAME, "tr")

    # Extract the expected names from the context table
    expected_names = [row["name"].strip().lower() for row in context.table]

    found_names = set()

    # Search through the table rows for the names
    for row in table_rows[1:]:  # Skip the header row
        columns = row.find_elements(By.TAG_NAME, "td")
        actual_name = columns[1].text.strip().lower()  # Name is in the second column

        if actual_name in expected_names:
            found_names.add(actual_name)

        # If all expected names are found, stop searching
        if len(found_names) == len(expected_names):
            break

    assert len(found_names) == len(expected_names), (
        f"Not all expected names were found in the inventory. "
        f"Expected: {expected_names}, Found: {found_names}"
    )

    print("All expected names were found in the results.")


##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by ID_PREFIX so the Name field has an id='product_name'
# We can then lowercase the name and prefix with product_ to get the id
##################################################################


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)


@then('I should see "{expected_value}" in the "Name" field')
def step_impl(context, expected_value):
    element_id = ID_PREFIX + "name"
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), expected_value)
    )
    assert found, f"Expected value '{expected_value}' not found in 'Name' field"


@then('I should see "{expected_value}" in the "Quantity" field')
def step_impl(context, expected_value):
    element_id = ID_PREFIX + "quantity"
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), expected_value)
    )
    assert found, f"Expected value '{expected_value}' not found in 'Quantity' field"


@then('I should see "{expected_value}" in the "Product ID" field')
def step_impl(context, expected_value):
    element_id = ID_PREFIX + "product_id"
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), expected_value)
    )
    assert found, f"Expected value '{expected_value}' not found in 'Product ID' field"


@then('I should see "{expected_value}" in the "Price" field')
def step_impl(context, expected_value):
    element_id = ID_PREFIX + "price"
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), expected_value)
    )
    assert found, f"Expected value '{expected_value}' not found in 'Price' field"


@then('I should see "{expected_value}" in the "Restock Level" field')
def step_impl(context, expected_value):
    element_id = ID_PREFIX + "restock_level"
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), expected_value)
    )
    assert (
        found
    ), f"Expected value '{expected_value}' not found in 'Restock Level' field"


@when("I delete the inventory item with id {item_id}")
def step_impl(context, item_id):
    element_id = "product_id"
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(item_id)
    delete_button_id = "delete-btn"
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.element_to_be_clickable((By.ID, delete_button_id))
    ).click()


@then("the inventory item with id {item_id} should not exist")
def step_impl(context, item_id):
    element_id = "product_id"
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(item_id)
    retrieve_button_id = "retrieve-btn"
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.element_to_be_clickable((By.ID, retrieve_button_id))
    ).click()
    # After clicking Retrieve, check if an error message or empty result is returned
    flash_message = (
        WebDriverWait(context.driver, context.wait_seconds)
        .until(EC.presence_of_element_located((By.ID, "flash_message")))
        .text
    )
    assert (
        "not found" in flash_message.lower()
    ), f"Item with ID {item_id} was unexpectedly found."


@then("the inventory should contain")
def step_impl(context):
    rest_endpoint = f"{context.base_url}/inventory"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    assert context.resp.status_code == HTTP_200_OK

    items = context.resp.json()
    expected_items = []

    for row in context.table:
        expected_item = {
            "name": row["name"],
            "description": row["description"],
            "quantity": int(row["quantity"]),
            "price": float(row["price"]),
            "product_id": int(row["product_id"]),
            "restock_level": int(row["restock_level"]),
            "condition": row["condition"].lower(),
        }
        expected_items.append(expected_item)

    # Now check if all expected items are in the response
    items_found = []
    for expected_item in expected_items:
        for item in items:
            if (
                item["name"] == expected_item["name"]
                and item["description"] == expected_item["description"]
                and item["quantity"] == expected_item["quantity"]
                and item["price"] == expected_item["price"]
                and item["product_id"] == expected_item["product_id"]
                and item["restock_level"] == expected_item["restock_level"]
                and item["condition"].lower() == expected_item["condition"]
            ):
                items_found.append(item)
                break

    assert len(items_found) == len(expected_items), (
        f"Not all expected items were found in the inventory. "
        f"Expected: {expected_items}, Found: {items_found}"
    )


@when("I delete the inventory item with the captured ID")
def step_impl(context):
    item_id = context.captured_id
    assert item_id, "No captured ID found to delete."

    rest_endpoint = f"{context.base_url}/api/inventory/{item_id}"
    context.resp = requests.delete(rest_endpoint, timeout=WAIT_TIMEOUT)
    assert (
        context.resp.status_code == HTTP_204_NO_CONTENT
    ), f"Failed to delete item with ID {item_id}."


@then("the inventory item with the captured ID should not exist")
def step_impl(context):
    item_id = context.captured_id
    assert item_id, "No captured ID found to check."

    rest_endpoint = f"{context.base_url}/inventory/{item_id}"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    assert (
        context.resp.status_code == HTTP_404_NOT_FOUND
    ), f"Item with ID {item_id} still exists."


@when('I capture the ID of the item with name "{item_name}"')
def step_impl(context, item_name):
    try:
        # Wait for the table to be populated
        wait = WebDriverWait(context.driver, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#search_results table tr:nth-child(2)")
            )
        )

        # Locate the table inside the 'search_results' div
        table = context.driver.find_element(By.CSS_SELECTOR, "#search_results table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Iterate over the rows to find the matching item by name
        for row in rows[1:]:  # Skip the header row
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) < 8:
                continue  # Skip if the row doesn't have enough columns

            name_in_row = (
                columns[1].text.strip().lower()
            )  # Name is in the second column

            if name_in_row == item_name.lower():
                captured_id = columns[0].text.strip()  # ID is in the first column
                context.captured_id = captured_id
                print(f"Captured ID for '{item_name}': {captured_id}")
                return  # Exit after capturing the ID

        # If the loop completes without returning, the item wasn't found
        raise AssertionError(f"Item '{item_name}' not found in the table.")

    except TimeoutException:
        raise AssertionError(
            "Timed out waiting for the table to be populated before capturing the ID."
        )
    except Exception as e:
        raise AssertionError(f"An error occurred while capturing the ID: {str(e)}")


@when('I set the "product_id" to the captured ID for "{item_name}"')
def step_impl(context, item_name):
    # Get the captured ID for the item
    item_id = context.captured_ids.get(item_name)
    assert item_id is not None, f"Item ID for {item_name} not found."

    # Set the product_id field with the captured ID
    element = context.driver.find_element(By.ID, "product_id")
    element.clear()
    element.send_keys(item_id)


@when('I set the "product_id" to the ID for "{item_name}"')
def step_impl(context, item_name):
    # Get the captured ID for the item from the previous capture step
    item_id = context.captured_ids.get(item_name)
    assert item_id is not None, f"Item ID for {item_name} not found in captured IDs."

    # Find the input field for product_id and set its value to the captured ID
    element = context.driver.find_element(By.ID, "product_id")
    element.clear()
    element.send_keys(item_id)


@then("the item should not be listed in the inventory")
def step_impl(context):
    item_id = context.captured_id
    assert item_id, "No captured ID found to check."

    rest_endpoint = f"{context.base_url}/inventory/{item_id}"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    assert (
        context.resp.status_code == HTTP_404_NOT_FOUND
    ), f"Item with ID {item_id} still exists."


@when('I set the "system_product_id" to the captured ID for "{item_name}"')
def step_impl(context, item_name):
    # Get the captured ID for the item from the previous capture step
    item_id = context.captured_id
    assert item_id is not None, f"Item ID for {item_name} not found in captured IDs."

    # Find the input field for system_product_id and set its value to the captured ID
    element = context.driver.find_element(By.ID, "system_product_id")
    element.clear()
    element.send_keys(item_id)
