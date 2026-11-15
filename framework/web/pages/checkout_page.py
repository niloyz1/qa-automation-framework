"""saucedemo.com checkout pages (information, overview, complete)."""

from __future__ import annotations

import allure
from playwright.sync_api import expect

from framework.web.pages.base_page import BasePage


class CheckoutPage(BasePage):
    path = "/checkout-step-one.html"

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        with allure.step("Fill in shipping information"):
            self.by_test_id("firstName").fill(first_name)
            self.by_test_id("lastName").fill(last_name)
            self.by_test_id("postalCode").fill(postal_code)
            self.by_test_id("continue").click()

    def item_total(self) -> float:
        text = self.by_test_id("subtotal-label").inner_text()  # "Item total: $39.98"
        return float(text.split("$")[1])

    def finish(self) -> None:
        self.by_test_id("finish").click()

    def expect_complete(self) -> None:
        expect(self.by_test_id("complete-header")).to_have_text("Thank you for your order!")

    def expect_error(self, text: str) -> None:
        expect(self.by_test_id("error")).to_contain_text(text)
