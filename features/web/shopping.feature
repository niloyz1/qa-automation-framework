@web @saucedemo
Feature: Shopping cart and checkout
  As a logged-in shopper
  I want to manage my cart and check out
  So that I can complete a purchase

  Background:
    Given I am logged in as the "standard" user

  @smoke
  Scenario: Add a product to the cart
    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge should show 1

  @regression
  Scenario: Remove a product from the cart
    Given I have added "Sauce Labs Bike Light" to the cart
    When I remove "Sauce Labs Bike Light" from the cart
    Then the cart badge should show 0

  @regression
  Scenario Outline: Sort products
    When I sort products by "<order>"
    Then the products should be sorted by "<order>"

    Examples:
      | order               |
      | Name (A to Z)       |
      | Name (Z to A)       |
      | Price (low to high) |
      | Price (high to low) |

  @smoke
  Scenario: Complete checkout with two products
    Given I have added "Sauce Labs Backpack" to the cart
    And I have added "Sauce Labs Bolt T-Shirt" to the cart
    When I check out with my shipping details
    Then the item total should be 45.98
    When I finish the order
    Then I should see the order confirmation

  @regression @negative
  Scenario: Checkout requires a first name
    Given I have added "Sauce Labs Onesie" to the cart
    When I check out without a first name
    Then I should see the checkout error "First Name is required"
