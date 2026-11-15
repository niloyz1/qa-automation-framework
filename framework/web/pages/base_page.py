"""Base page object: shared navigation, waits, and reporting helpers."""

from __future__ import annotations

import allure
from playwright.sync_api import Locator, Page, expect


class BasePage:
    #: Path relative to the site's base URL, e.g. "/inventory.html"
    path: str = "/"

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    @property
    def url(self) -> str:
        return f"{self.base_url}{self.path}"

    def open(self) -> BasePage:
        with allure.step(f"Open {self.__class__.__name__} ({self.url})"):
            self.page.goto(self.url, wait_until="domcontentloaded")
        return self

    def by_test_id(self, test_id: str) -> Locator:
        """Prefer stable data-test attributes over CSS structure."""
        return self.page.locator(f'[data-test="{test_id}"]')

    def expect_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(f"{self.base_url}{fragment}" if fragment.startswith("/") else fragment)

    def attach_screenshot(self, name: str = "screenshot") -> None:
        allure.attach(self.page.screenshot(full_page=True), name=name, attachment_type=allure.attachment_type.PNG)
