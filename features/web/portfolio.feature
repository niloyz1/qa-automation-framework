@web @portfolio
Feature: Portfolio site (niloyzaman.com)
  As the owner of a QA portfolio
  I want its interactive features covered by automated tests
  So that the site I send to recruiters always works

  Background:
    Given I open the portfolio home page

  @smoke
  Scenario: Home page loads with a single main heading and navigation
    Then the main heading should contain "Niloy"
    And the main navigation should link to "#work", "#experience" and "#stack"

  @smoke
  Scenario: The in-page release suite passes
    When I run the in-page release suite
    Then the suite summary should report "9 passed"

  @regression
  Scenario Outline: The AI evaluator scores model answers correctly
    When I open the "ai-eval" console tab
    And I evaluate model answer "<answer>"
    Then the verdict should be "<verdict>"

    Examples:
      | answer | verdict |
      | A      | PASS    |
      | B      | BLOCK   |
      | C      | BLOCK   |

  @regression
  Scenario: The terminal answers commands
    When I open the "terminal" console tab
    And I type "whoami" in the terminal
    Then the terminal output should contain "Lead QA Engineer"

  @regression
  Scenario: Theme preference can be switched
    When I switch the colour theme
    Then the theme should change
