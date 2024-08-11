Feature: Inventory Management


  Background:
    Given the following items exist
      | name   | description | quantity | price | product_id | restock_level | condition |
      | laptop | Electronics | 25       | 1000  | 1          | 10            | NEW       |
      | tablet | Electronics | 50       | 500   | 2          | 5             | ARCHIVED  |
      | chair  | Furniture   | 75       | 150   | 3          | 15            | USED      |
      | marker | Stationery  | 18       | 1     | 4          | 18            | USED      |

  Scenario: Add new inventory item
    Given I have access to the inventory service
    When I add a new item with name "item1"
    Then I should see the item in the inventory list

  Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory RESTful Service" in the title
    And I should not see "404 Not Found"

  Scenario: Create an Item
    When I visit the "Home Page"
    And I set the "Name" to "Joyful"
    And I set the "Description" to "Rhino"
    And I set the "Quantity" to "10"
    And I set the "Price" to "99.99"
    And I set the "Product ID" to "123"
    And I set the "Restock Level" to "5"
    And I select "NEW" in the "Condition" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "system_product_id" field

    And I press the "Clear" button
    Then the "system_product_id" field should be empty
    Then the "product_name" field should be empty
    Then the "product_description" field should be empty
    Then the "product_quantity" field should be empty
    Then the "product_price" field should be empty
    Then the "product_product_id" field should be empty
    Then the "product_restock_level" field should be empty
    Then the "product_condition" field should be empty

    When I paste the "system_product_id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Joyful" in the "Name" field
    And I should see "Rhino" in the "Description" field
    And I should see "10" in the "Quantity" field
    And I should see "99.99" in the "Price" field
    And I should see "123" in the "Product ID" field
    And I should see "5" in the "Restock Level" field
    And I should see "NEW" in the "Condition" dropdown

  Scenario: Search for an Item by Name
    When I visit the "Home Page"
    And I set the "Name" to "laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "laptop" in the "Name" field
    And I should see "Electronics" in the "Description" field
    And I should see "25" in the "Quantity" field
    And I should see "1000" in the "Price" field
    And I should see "1" in the "Product ID" field
    And I should see "10" in the "Restock Level" field
    And I should see "NEW" in the "Condition" dropdown

  Scenario: Search for an Item by Condition
    When I visit the "Home Page"
    And I select "USED" in the "Condition" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "chair" in the results
    And I should see "marker" in the results
    And I should not see "laptop" in the results
    And I should not see "tablet" in the results

  Scenario: Delete an inventory item
    Given the following items exist
      | name   | description | quantity | price | product_id | restock_level | condition |
      | laptop | Electronics | 25       | 1000  | 1          | 10            | NEW       |
    When I visit the "Home Page"
    And I press the "List All" button
    And I capture the ID of the item with name "laptop"
    And I delete the inventory item with the captured ID
    Then the item should not be listed in the inventory

  Scenario: Read an inventory item
    When I visit the "Home Page"
    And I press the "List All" button
    And I capture the ID of the item with name "chair"
    And I set the "system_product_id" to the captured ID for "chair"
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "chair" in the results
    And I should see "Furniture" in the results
    And I should see "75" in the results

  Scenario: Archive an inventory item
    When I visit the "Home Page"
    And I press the "List All" button
    And I capture the ID of the item with name "laptop"
    And I set the "system_product_id" to the captured ID for "laptop"
    And I press the "Archive" button
    Then I should see the message "Success"
    And I should see "laptop" in the results
    And I should see "ARCHIVED" in the "Condition" dropdown
    And I should not see "NEW" in the results
    When I set the "system_product_id" to the captured ID for "laptop"
    And I press the "Archive" button
    Then I should see the specific error message "400 Bad Request: Item is already archived"

  Scenario: Update an inventory item
    Given the following items exist
      | name   | description | quantity | price | product_id | restock_level | condition |
      | laptop | Electronics | 25       | 1000  | 1          | 10            | NEW       |
      | tablet | Electronics | 50       | 500   | 2          | 5             | ARCHIVED  |
      | chair  | Furniture   | 75       | 150   | 3          | 15            | USED      |
      | marker | Stationery  | 18       | 1     | 4          | 18            | USED      |

    When I visit the "Home Page"
    And I set the "Name" to "laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "laptop" in the "Name" field
    When I change "Name" to "updated laptop"
    And I change "Quantity" to "45"
    And I change "Price" to "450"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "system_product_id" field
    When I press the "Clear" button
    When I paste the "system_product_id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "updated laptop" in the "Name" field
    And I should see "45" in the "Quantity" field
    And I should see "450" in the "Price" field
    When I press the "Clear" button
    And I set the "Name" to "updated laptop"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "updated laptop" in the results
    And I should not see "laptop" in the results

  Scenario: List all inventory items
    When I visit the "Home Page"
    And I press the "List All" button
    Then I should see the message "Success"
    Then I should see at least the following items in the results
      | name   | description | quantity | price | product_id | restock_level | condition |
      | laptop | Electronics | 25       | 1000  | 1          | 10            | NEW       |
      | tablet | Electronics | 50       | 500   | 2          | 5             | OPEN      |
      | chair  | Furniture   | 75       | 150   | 3          | 15            | USED      |
      | marker | Stationery  | 18       | 1     | 4          | 18            | USED      |
