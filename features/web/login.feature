@web @saucedemo
Feature: Login
  As a shopper on Swag Labs (saucedemo.com)
  I want to log in with my account
  So that I can browse and buy products

  Background:
    Given I am on the login page

  @smoke
  Scenario: Standard user logs in successfully
    When I log in as the "standard" user
    Then I should see the products page

  @regression @negative
  Scenario: Locked-out user is rejected
    When I log in as the "locked_out" user
    Then I should see the login error "Sorry, this user has been locked out."

  @regression @negative
  Scenario Outline: Login form validation
    When I log in with username "<username>" and password "<password>"
    Then I should see the login error "<error>"

    Examples:
      | username      | password     | error                                |
      |               | secret_sauce | Username is required                 |
      | standard_user |              | Password is required                 |
      | standard_user | wrong        | Username and password do not match   |
