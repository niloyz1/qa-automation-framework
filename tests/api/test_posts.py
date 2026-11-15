"""Step definitions for features/api/posts.feature."""

from __future__ import annotations

import json

import pytest
from jsonschema import validate
from pytest_bdd import parsers, scenarios, then, when

from framework.api.client import ApiClient
from framework.config import DATA_DIR

scenarios("api/posts.feature")


def _schema(name: str) -> dict:
    return json.loads((DATA_DIR / "schemas" / f"{name}.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def api(settings) -> ApiClient:
    return ApiClient(settings.api_url)


@when(parsers.parse('I request GET "{path}"'), target_fixture="response")
def get(api, path):
    return api.get(path)


@when(parsers.parse('I create a post titled "{title}" with body "{body}"'), target_fixture="response")
def create_post(api, title, body):
    return api.post("/posts", json={"title": title, "body": body, "userId": 1})


@then(parsers.parse("the response status should be {status:d}"))
def status_is(response, status):
    assert response.status_code == status, f"expected {status}, got {response.status_code}: {response.text[:200]}"


@then(parsers.parse('the response should match the "{name}" schema'))
def matches_schema(response, name):
    validate(response.json(), _schema(name))


@then(parsers.parse('every item should match the "{name}" schema'))
def every_item_matches(response, name):
    items = response.json()
    assert items, "expected a non-empty list"
    schema = _schema(name)
    for item in items:
        validate(item, schema)


@then(parsers.parse('every item should have "{field}" equal to {value:d}'))
def every_item_field(response, field, value):
    wrong = [item for item in response.json() if item[field] != value]
    assert not wrong, f"{len(wrong)} items had {field} != {value}"


@then(parsers.parse("the response should be faster than {ms:d} ms"))
def faster_than(response, ms):
    assert response.elapsed_ms < ms, f"took {response.elapsed_ms} ms (budget {ms} ms)"


@then(parsers.parse('the response field "{field}" should be "{value}"'))
def field_is(response, field, value):
    assert response.json()[field] == value


@then(parsers.parse('the response should contain a new "{field}"'))
def has_new_id(response, field):
    assert isinstance(response.json().get(field), int), response.json()
