@mobile
Feature: Mobile shopping (Sauce Labs My Demo App)
  As a shopper using the native app on Android or iOS
  I want to browse the catalog and add products to my cart
  So that I can buy on the go

  # Platform is chosen at run time:  pytest -m mobile --platform android|ios

  Background:
    Given the app is open on the catalog screen

  @smoke
  Scenario: Catalog shows products
    Then the catalog should list "Sauce Labs Backpack"

  @smoke
  Scenario: Add a product to the cart from its detail screen
    When I open the product "Sauce Labs Backpack"
    And I add the product to the cart
    Then the cart badge should show "1"

  @regression
  Scenario: Cart offers checkout
    When I open the product "Sauce Labs Backpack"
    And I add the product to the cart
    And I open the cart
    Then I should be able to proceed to checkout
