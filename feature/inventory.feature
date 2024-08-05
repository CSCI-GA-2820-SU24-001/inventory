Feature: Inventory Management
  Scenario: Add new inventory item
    Given I have access to the inventory service
    When I add a new item with name "item1"
    Then I should see the item in the inventory list

  Background:
    Given the following items
      | id  | name   | description | quantity | price | product_id | restock_level | condition |
      | 34  | laptop | Electronics | 25       | 1000  | 1          | 10            | NEW       |
      | 567 | tablet | Electronics | 50       | 500   | 2          | 5             | REFURB    |
      | 890 | chair  | Furniture   | 75       | 150   | 3          | 15            | USED      |
      | 456 | marker | Stationery  | 18       | 1     | 4          | 18            | USED      |

  Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory REST API Service" in the title
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
    When I copy the "ID" field
    And I press the "Clear" button
    Then the "ID" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    And the "Quantity" field should be empty
    And the "Price" field should be empty
    And the "Product ID" field should be empty
    And the "Restock Level" field should be empty
    And the "Condition" field should be empty
    When I paste the "ID" field
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
    Given the following inventories exist:
      | id  | name   | quantity | price |
      | 34  | laptop | 25       | 1000  |
      | 567 | tablet | 50       | 500   |
      | 890 | chair  | 75       | 150   |
      | 456 | marker | 18       | 1     |
    When I delete the inventory item with id 567
    Then the inventory item with id 567 should not exist
    And the inventory should contain:
      | id  | name   | description | quantity | price | product_id | restock_level | condition |
      | 34  | laptop | Electronics | 25       | 1000  | 1          | 10            | NEW       |
      | 890 | chair  | Furniture   | 75       | 150   | 3          | 15            | USED      |
      | 456 | marker | Stationery  | 18       | 1     | 4          | 18            | USED      |

  Scenario: Read an inventory item
    When I visit the "Home Page"
    And I set the "Product ID" to "890"
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "chair" in the results
    And I should see "Furniture" in the results
    And I should see "75" in the results
    And I should not see "laptop" in the results
    And I should not see "tablet" in the results
    And I should not see "marker" in the results

  Scenario: Decrement an inventory item quantity
    When I visit the "Home Page"
    And I set the "product_id" to "34"
    And I press the "Decrement" button
    Then I should see the message "Success"
    And I should see "laptop" in the results
    And I should see "24" in the results
    And I should not see "25" in the results

  Scenario: Archive an inventory item
    When I visit the "Home Page"
    And I set the "Product ID" to "34"
    And I press the "Archive" button
    Then I should see the message "Success"
    And I should see "laptop" in the results
    And I should see "Archived" in the results
    And I should not see "NEW" in the results
    When I set the "Product ID" to "34"
    And I press the "Archive" button
    Then I should see the message "400 Bad Request: Item is already archived" in the results

  Scenario: Update an inventory item
    When I visit the "Home Page"
    And I set the "Name" to "tablet"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "tablet" in the "Name" field
    And I should see "Electronics" in the "Category" field
    When I change "Name" to "updated tablet"
    And I change "Quantity" to "45"
    And I change "Price" to "450"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "updated tablet" in the "Name" field
    And I should see "45" in the "Quantity" field
    And I should see "450" in the "Price" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "updated tablet" in the results
    And I should not see "tablet" in the results

  Scenario: List all inventory items
    When I visit the "Home Page"
    And I press the "List All" button
    Then I should see the message "Success"
    And I should see the following items in the results:
      | id  | name   | description | quantity | price | product_id | restock_level | condition |
      | 34  | laptop | Electronics | 25       | 1000  | 1          | 10            | NEW       |
      | 567 | tablet | Electronics | 50       | 500   | 2          | 5             | OPEN      |
      | 890 | chair  | Furniture   | 75       | 150   | 3          | 15            | USED      |
      | 456 | marker | Stationery  | 18       | 1     | 4          | 18            | USED      |
