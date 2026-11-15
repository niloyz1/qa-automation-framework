"""Web fixtures: browser context settings, timeouts, and failure evidence for the report."""

from __future__ import annotations

import allure
import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1366, "height": 900}, "locale": "en-US"}


@pytest.fixture(autouse=True)
def _web_page_setup(request, page, settings):
    """Apply timeouts, then attach a screenshot and the URL to the report if the scenario fails."""
    page.set_default_timeout(settings.default_timeout_ms)
    page.set_default_navigation_timeout(settings.navigation_timeout_ms)
    yield
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        try:
            allure.attach(
                page.screenshot(full_page=True), name="failure screenshot", attachment_type=allure.attachment_type.PNG
            )
            allure.attach(page.url, name="failure URL", attachment_type=allure.attachment_type.URI_LIST)
        except Exception:  # page may already be closed; evidence is best-effort
            pass
