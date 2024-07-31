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