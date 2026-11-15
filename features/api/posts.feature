@api
Feature: Posts REST API
  As a client of the posts service (jsonplaceholder.typicode.com)
  I want its endpoints to honour their contract
  So that consumers can rely on status codes, schemas, and response times

  @smoke
  Scenario: Get a single post
    When I request GET "/posts/1"
    Then the response status should be 200
    And the response should match the "post" schema
    And the response should be faster than 3000 ms

  @regression
  Scenario: List posts for a user
    When I request GET "/posts?userId=1"
    Then the response status should be 200
    And every item should match the "post" schema
    And every item should have "userId" equal to 1

  @smoke
  Scenario: Create a post
    When I create a post titled "Release notes" with body "All checks passed"
    Then the response status should be 201
    And the response field "title" should be "Release notes"
    And the response should contain a new "id"

  @regression @negative
  Scenario Outline: Unknown resources return 404
    When I request GET "<path>"
    Then the response status should be 404

    Examples:
      | path          |
      | /posts/99999  |
      | /nope         |
