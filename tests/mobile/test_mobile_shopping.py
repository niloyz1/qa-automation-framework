"""Step definitions for features/mobile/shopping.feature (Android + iOS)."""

from __future__ import annotations

import allure
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from framework.config import ROOT
from framework.mobile.screens import CartScreen, CatalogScreen, ProductScreen

scenarios("mobile/shopping.feature")


@pytest.fixture
def platform_name(request) -> str:
    return request.config.getoption("--platform")


@pytest.fixture
def driver(request, settings, platform_name):
    app = ROOT / settings.mobile[platform_name]["app"]
    if not app.exists():
        pytest.skip(f"{platform_name} app not found at {app}. Run: python scripts/get_apps.py {platform_name}")
    from framework.mobile.driver import create_driver  # imported lazily so web/API runs don't need Appium

    try:
        drv = create_driver(platform_name, settings)
    except Exception as exc:  # Appium server or device not running
        pytest.skip(f"Appium session could not start ({exc.__class__.__name__}). See README > Mobile setup.")
    yield drv
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        allure.attach(
            drv.get_screenshot_as_png(), name="failure screenshot", attachment_type=allure.attachment_type.PNG
        )
        allure.attach(drv.page_source, name="UI hierarchy", attachment_type=allure.attachment_type.XML)
    drv.quit()


@pytest.fixture
def catalog(driver, platform_name):
    return CatalogScreen(driver, platform_name)


@pytest.fixture
def product(driver, platform_name):
    return ProductScreen(driver, platform_name)


@pytest.fixture
def cart(driver, platform_name):
    return CartScreen(driver, platform_name)


@given("the app is open on the catalog screen")
def app_open(catalog):
    assert catalog.is_displayed()


@when(parsers.parse('I open the product "{name}"'))
def open_product(catalog, name):
    catalog.open_product(name)


@when("I add the product to the cart")
def add_product(product):
    product.add_to_cart()


@when("I open the cart")
def open_cart(cart):
    cart.open()


@then(parsers.parse('the catalog should list "{name}"'))
def catalog_lists(catalog, name):
    assert name in catalog.product_names()


@then(parsers.parse('the cart badge should show "{count}"'))
def badge_shows(cart, count):
    assert cart.badge_count() == count


@then("I should be able to proceed to checkout")
def can_checkout(cart):
    assert cart.has_checkout()
