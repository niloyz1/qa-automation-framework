"""Screen objects for the Sauce Labs "My Demo App" (Android + iOS).

One class per screen, with locators per platform kept side by side, so a
locator change is a one-line fix and the step definitions never change.
"""

from __future__ import annotations

import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ANDROID_PKG = "com.saucelabs.mydemoapp.android:id/"

# (strategy, value) per platform. Android uses resource ids; iOS uses accessibility ids.
LOCATORS: dict[str, dict[str, tuple[str, str]]] = {
    "catalog_title": {
        "android": (AppiumBy.ID, ANDROID_PKG + "productTV"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "Products"),
    },
    "product_names": {
        "android": (AppiumBy.ID, ANDROID_PKG + "titleTV"),
        "ios": (AppiumBy.IOS_PREDICATE, "type == 'XCUIElementTypeStaticText' AND name BEGINSWITH 'Sauce Labs'"),
    },
    "detail_price": {
        "android": (AppiumBy.ID, ANDROID_PKG + "priceTV"),
        "ios": (AppiumBy.IOS_PREDICATE, "type == 'XCUIElementTypeStaticText' AND label BEGINSWITH '$'"),
    },
    "add_to_cart": {
        "android": (AppiumBy.ID, ANDROID_PKG + "cartBt"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "Add To Cart"),
    },
    "cart_badge": {
        "android": (AppiumBy.ID, ANDROID_PKG + "cartTV"),
        "ios": (AppiumBy.IOS_PREDICATE, "name == 'Cart-tab-item'"),
    },
    "cart_icon": {
        "android": (AppiumBy.ID, ANDROID_PKG + "cartIV"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "Cart-tab-item"),
    },
    "checkout_button": {
        "android": (AppiumBy.ID, ANDROID_PKG + "cartBt"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "ProceedToCheckout"),
    },
}


class BaseScreen:
    def __init__(self, driver, platform: str, timeout: int = 20) -> None:
        self.driver = driver
        self.platform = platform
        self.wait = WebDriverWait(driver, timeout)

    def locator(self, key: str) -> tuple[str, str]:
        return LOCATORS[key][self.platform]

    def find(self, key: str):
        return self.wait.until(EC.presence_of_element_located(self.locator(key)))

    def find_all(self, key: str):
        self.find(key)
        return self.driver.find_elements(*self.locator(key))

    def tap(self, key: str) -> None:
        self.wait.until(EC.element_to_be_clickable(self.locator(key))).click()

    def tap_text(self, text: str) -> None:
        if self.platform == "android":
            selector = (
                f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{text}"))'
            )
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector).click()
        else:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, text).click()

    def screenshot(self, name: str) -> None:
        allure.attach(self.driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)


class CatalogScreen(BaseScreen):
    def is_displayed(self) -> bool:
        return self.find("catalog_title").is_displayed()

    def product_names(self) -> list[str]:
        return [e.text for e in self.find_all("product_names")]

    def open_product(self, name: str) -> None:
        with allure.step(f"Open product '{name}'"):
            self.tap_text(name)


class ProductScreen(BaseScreen):
    def price(self) -> str:
        return self.find("detail_price").text

    def add_to_cart(self) -> None:
        with allure.step("Tap Add To Cart"):
            self.tap("add_to_cart")


class CartScreen(BaseScreen):
    def badge_count(self) -> str:
        badge = self.find("cart_badge")
        return badge.text if self.platform == "android" else (badge.get_attribute("value") or "")

    def open(self) -> None:
        self.tap("cart_icon")

    def has_checkout(self) -> bool:
        return self.find("checkout_button").is_displayed()
