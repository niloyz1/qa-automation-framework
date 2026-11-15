"""Step definitions for features/llm/answer_quality.feature."""

from __future__ import annotations

import allure
from pytest_bdd import given, parsers, scenarios, then, when

from framework.config import load_data
from framework.llm import evaluators as ev

scenarios("llm/answer_quality.feature")

CASES = load_data("llm_cases.yaml")
MAX_WORDS = 60


@given(parsers.parse('the source document "{name}"'), target_fixture="source")
def source_document(name):
    text = CASES["sources"][name]
    allure.attach(text, name=f"source: {name}", attachment_type=allure.attachment_type.TEXT)
    return text


@given(parsers.parse('the recorded answer "{name}"'), target_fixture="answer")
def recorded_answer(name):
    text = CASES["answers"][name]["text"].strip()
    allure.attach(text, name=f"answer: {name}", attachment_type=allure.attachment_type.TEXT)
    return text


@when("the answer is evaluated", target_fixture="results")
def evaluate(answer, source):
    results = {
        "groundedness": ev.check_groundedness(answer, source),
        "invented numbers": ev.check_no_invented_numbers(answer, source),
        "pii": ev.check_pii(answer),
        "prompt injection": ev.check_prompt_injection(answer),
        "length": ev.check_length(answer, MAX_WORDS),
    }
    allure.attach(
        "\n".join(f"{name:<17} {result}" for name, result in results.items()),
        name="evaluation scorecard",
        attachment_type=allure.attachment_type.TEXT,
    )
    return results


@when(parsers.parse('the answer is validated as JSON with keys "{keys}"'), target_fixture="json_result")
def validate_json(answer, keys):
    return ev.check_json_schema(answer, [k.strip() for k in keys.split(",")])


@then("every check should pass")
def all_pass(results):
    failed = {name: str(r) for name, r in results.items() if not r.passed}
    assert not failed, f"checks failed: {failed}"


@then(parsers.parse('the "{check}" check should fail'))
def check_fails(results, check):
    assert not results[check].passed, f"'{check}' should have flagged this answer but returned {results[check]}"


@then("the release gate should block the answer")
def gate_blocks(results):
    assert any(not r.passed for r in results.values()), "release gate let an unsafe answer through"


@then(parsers.parse('the JSON check should "{outcome}"'))
def json_outcome(json_result, outcome):
    assert json_result.passed is (outcome == "pass"), str(json_result)
