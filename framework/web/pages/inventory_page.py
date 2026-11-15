"""saucedemo.com product list (inventory) page."""

from __future__ import annotations

import re

import allure
from playwright.sync_api import expect

from framework.web.pages.base_page import BasePage

SORT_OPTIONS = {
    "name (a to z)": "az",
    "name (z to a)": "za",
    "price (low to high)": "lohi",
    "price (high to low)": "hilo",
}


def _slug(product_name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack'.

    Mirrors the site's own rule (whitespace -> '-', lowercase), so names with
    punctuation such as 'Test.allTheThings() T-Shirt (Red)' map correctly too.
    """
    return re.sub(r"\s+", "-", product_name).lower()


class InventoryPage(BasePage):
    path = "/inventory.html"

    @property
    def title(self):
        return self.by_test_id("title")

    @property
    def items(self):
        return self.by_test_id("inventory-item")

    @property
    def cart_badge(self):
        return self.by_test_id("shopping-cart-badge")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(r"/inventory\.html$"))
        expect(self.title).to_have_text("Products")

    def add_to_cart(self, product_name: str) -> None:
        with allure.step(f"Add '{product_name}' to the cart"):
            self.by_test_id(f"add-to-cart-{_slug(product_name)}").click()

    def remove_from_cart(self, product_name: str) -> None:
        with allure.step(f"Remove '{product_name}' from the cart"):
            self.by_test_id(f"remove-{_slug(product_name)}").click()

    def sort_by(self, label: str) -> None:
        with allure.step(f"Sort products by {label}"):
            self.by_test_id("product-sort-container").select_option(SORT_OPTIONS[label.lower()])

    def product_names(self) -> list[str]:
        return self.by_test_id("inventory-item-name").all_inner_texts()

    def product_prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.by_test_id("inventory-item-price").all_inner_texts()]

    def expect_cart_count(self, count: int) -> None:
        if count == 0:
            expect(self.cart_badge).to_have_count(0)
        else:
            expect(self.cart_badge).to_have_text(str(count))

    def go_to_cart(self) -> None:
        self.by_test_id("shopping-cart-link").click()
