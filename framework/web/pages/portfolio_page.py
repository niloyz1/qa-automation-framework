"""niloyzaman.com: the author's own portfolio, used as a real-world test target."""

from __future__ import annotations

import allure
from playwright.sync_api import expect

from framework.web.pages.base_page import BasePage


class PortfolioPage(BasePage):
    path = "/index.html"

    @property
    def heading(self):
        return self.page.get_by_role("heading", level=1)

    @property
    def nav(self):
        return self.page.get_by_role("navigation", name="Main navigation")

    def tab(self, name: str):
        return self.page.get_by_role("tab", name=name)

    def section_links(self) -> list[str]:
        return [h for h in self.nav.locator('a[href^="#"]').evaluate_all("els => els.map(e => e.hash)")]

    def run_release_suite(self) -> None:
        with allure.step("Run the in-page release suite"):
            # The suite auto-runs once on scroll; clicking guarantees a fresh, complete run.
            button = self.page.locator("#run")
            expect(button).to_be_enabled(timeout=15000)
            button.click()
            expect(button).to_be_enabled(timeout=15000)

    def suite_summary(self) -> str:
        return self.page.locator("#summary").inner_text()

    def choose_eval_answer(self, letter: str) -> None:
        with allure.step(f"Evaluate model answer {letter}"):
            self.page.get_by_role("radio", name=f"Answer {letter}").click()
            expect(self.page.locator("#verdict")).not_to_be_empty(timeout=10000)

    def verdict(self) -> str:
        return self.page.locator("#verdict").inner_text()

    def run_terminal_command(self, command: str) -> None:
        with allure.step(f"Type '{command}' in the terminal"):
            box = self.page.locator("#term-input")
            box.fill(command)
            box.press("Enter")

    def terminal_output(self) -> str:
        return self.page.locator("#term-out").inner_text()

    def toggle_theme(self) -> None:
        self.page.locator(".theme-toggle").first.click()

    def current_theme(self) -> str:
        return self.page.evaluate(
            "document.documentElement.dataset.theme || "
            "(matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')"
        )
