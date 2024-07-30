Feature: Inventory Management
  Scenario: Add new inventory item
    Given I have access to the inventory service
    When I add a new item with name "item1"
    Then I should see the item in the inventory list
