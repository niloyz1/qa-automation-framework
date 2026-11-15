"""Step definitions for features/web/login.feature and features/web/shopping.feature (saucedemo.com)."""

from __future__ import annotations

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from framework.config import load_data
from framework.web.pages import CartPage, CheckoutPage, InventoryPage, LoginPage

scenarios("web/login.feature", "web/shopping.feature")

USERS = load_data("users.yaml")


# --- Page fixtures ---------------------------------------------------------


@pytest.fixture
def login_page(page, settings) -> LoginPage:
    return LoginPage(page, settings.saucedemo_url)


@pytest.fixture
def inventory(page, settings) -> InventoryPage:
    return InventoryPage(page, settings.saucedemo_url)


@pytest.fixture
def cart(page, settings) -> CartPage:
    return CartPage(page, settings.saucedemo_url)


@pytest.fixture
def checkout(page, settings) -> CheckoutPage:
    return CheckoutPage(page, settings.saucedemo_url)


# --- Given -----------------------------------------------------------------


@given("I am on the login page")
def on_login_page(login_page):
    login_page.open()


@given(parsers.parse('I am logged in as the "{role}" user'))
def logged_in(login_page, inventory, role):
    login_page.open()
    login_page.login(USERS["users"][role], USERS["password"])
    inventory.expect_loaded()


@given(parsers.parse('I have added "{product}" to the cart'))
def have_added(inventory, product):
    inventory.add_to_cart(product)


# --- When ------------------------------------------------------------------


@when(parsers.parse('I log in as the "{role}" user'))
def log_in_as(login_page, role):
    login_page.login(USERS["users"][role], USERS["password"])


@when(parsers.re(r'I log in with username "(?P<username>[^"]*)" and password "(?P<password>[^"]*)"'))
def log_in_with(login_page, username, password):
    login_page.login(username, password)


@when(parsers.parse('I add "{product}" to the cart'))
def add_to_cart(inventory, product):
    inventory.add_to_cart(product)


@when(parsers.parse('I remove "{product}" from the cart'))
def remove_from_cart(inventory, product):
    inventory.remove_from_cart(product)


@when(parsers.parse('I sort products by "{order}"'))
def sort_by(inventory, order):
    inventory.sort_by(order)


@when("I check out with my shipping details")
def checkout_with_details(inventory, cart, checkout):
    shopper = USERS["shopper"]
    inventory.go_to_cart()
    cart.checkout()
    checkout.fill_information(shopper["first_name"], shopper["last_name"], shopper["postal_code"])


@when("I check out without a first name")
def checkout_without_first_name(inventory, cart, checkout):
    shopper = USERS["shopper"]
    inventory.go_to_cart()
    cart.checkout()
    checkout.fill_information("", shopper["last_name"], shopper["postal_code"])


@when("I finish the order")
def finish_order(checkout):
    checkout.finish()


# --- Then ------------------------------------------------------------------


@then("I should see the products page")
def products_page(inventory):
    inventory.expect_loaded()


@then(parsers.parse('I should see the login error "{message}"'))
def login_error(login_page, message):
    login_page.expect_error(message)


@then(parsers.parse("the cart badge should show {count:d}"))
def cart_badge(inventory, count):
    inventory.expect_cart_count(count)


@then(parsers.parse('the products should be sorted by "{order}"'))
def products_sorted(inventory, order):
    order = order.lower()
    if order.startswith("name"):
        names = inventory.product_names()
        assert names == sorted(names, reverse="z to a" in order), names
    else:
        prices = inventory.product_prices()
        assert prices == sorted(prices, reverse="high to low" in order), prices


@then(parsers.parse("the item total should be {total:f}"))
def item_total(checkout, total):
    assert checkout.item_total() == pytest.approx(total), f"item total was {checkout.item_total()}"


@then("I should see the order confirmation")
def order_confirmation(checkout):
    checkout.expect_complete()


@then(parsers.parse('I should see the checkout error "{message}"'))
def checkout_error(checkout, message):
    checkout.expect_error(message)
