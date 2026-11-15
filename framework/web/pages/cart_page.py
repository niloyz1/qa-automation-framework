"""saucedemo.com cart page."""

from __future__ import annotations

from playwright.sync_api import expect

from framework.web.pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    @property
    def items(self):
        return self.by_test_id("inventory-item")

    def item_names(self) -> list[str]:
        return self.by_test_id("inventory-item-name").all_inner_texts()

    def expect_items(self, names: list[str]) -> None:
        expect(self.by_test_id("inventory-item-name")).to_have_text(names)

    def checkout(self) -> None:
        self.by_test_id("checkout").click()
