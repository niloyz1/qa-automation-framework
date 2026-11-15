@llm
Feature: LLM answer quality gate
  As a QA engineer validating a generative AI summarization feature
  I want every recorded model answer scored by deterministic evaluators
  So that hallucinations, PII leaks, and prompt injections are caught before release

  Background:
    Given the source document "q3-note"

  @smoke
  Scenario: A faithful summary passes every check
    Given the recorded answer "faithful"
    When the answer is evaluated
    Then every check should pass

  @regression
  Scenario Outline: Unsafe answers are caught by the right check
    Given the recorded answer "<answer>"
    When the answer is evaluated
    Then the "<check>" check should fail
    And the release gate should block the answer

    Examples:
      | answer       | check            |
      | hallucinated | groundedness     |
      | hallucinated | invented numbers |
      | pii_leak     | pii              |
      | injection    | prompt injection |
      | rambling     | length           |

  @regression
  Scenario Outline: Structured output must be valid JSON with the agreed keys
    Given the recorded answer "<answer>"
    When the answer is validated as JSON with keys "revenue_musd, growth_pct, outlook_musd"
    Then the JSON check should "<outcome>"

    Examples:
      | answer            | outcome |
      | structured_ok     | pass    |
      | structured_broken | fail    |
