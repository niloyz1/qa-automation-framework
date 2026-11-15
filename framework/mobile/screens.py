"""Screen objects for the Sauce Labs "My Demo App" (Android + iOS).

One class per screen, with locators per platform kept side by side, so a
locator change is a one-line fix and the step definitions never change.

Locator sources: the app's open-source layouts (Android) and its own XCUITest
page objects and storyboards (iOS).
"""

from __future__ import annotations

import re

import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ANDROID_PKG = "com.saucelabs.mydemoapp.android:id/"

# (strategy, value) per platform. Android uses resource ids; iOS uses accessibility identifiers.
LOCATORS: dict[str, dict[str, tuple[str, str]]] = {
    "catalog_screen": {
        "android": (AppiumBy.ID, ANDROID_PKG + "productRV"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "Catalog-screen"),
    },
    "product_names": {
        "android": (AppiumBy.ID, ANDROID_PKG + "titleTV"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "Product Name"),
    },
    "product_images": {
        # Android opens a product by tapping its image; the title text is not clickable.
        "android": (AppiumBy.ID, ANDROID_PKG + "productIV"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "Product Name"),
    },
    "add_to_cart": {
        "android": (AppiumBy.ID, ANDROID_PKG + "cartBt"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "AddToCart"),
    },
    "cart_badge": {
        "android": (AppiumBy.ID, ANDROID_PKG + "cartTV"),
        # 'N Items' only: the cart screen also holds a hidden "No Items" label for the empty state.
        "ios": (AppiumBy.IOS_PREDICATE, "type == 'XCUIElementTypeStaticText' AND label MATCHES '[0-9]+ Items'"),
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

    def scroll_to(self, key: str) -> None:
        """Bring an element on screen first; Android doesn't render views below the fold."""
        strategy, value = self.locator(key)
        if self.platform == "android" and strategy == AppiumBy.ID:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                "new UiScrollable(new UiSelector().scrollable(true))"
                f'.scrollIntoView(new UiSelector().resourceId("{value}"))',
            )

    @staticmethod
    def text_of(element) -> str:
        return (element.text or element.get_attribute("label") or "").strip()

    def screenshot(self, name: str) -> None:
        allure.attach(self.driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)


class CatalogScreen(BaseScreen):
    def is_displayed(self) -> bool:
        return self.find("catalog_screen").is_displayed()

    def product_names(self) -> list[str]:
        return [self.text_of(e) for e in self.find_all("product_names")]

    def open_product(self, name: str) -> None:
        """Open the first product whose name starts with `name`.

        Prefix matching keeps scenarios platform-neutral: the same product is
        'Sauce Labs Backpack' on Android and 'Sauce Labs Backpack - Black' on iOS.
        """
        with allure.step(f"Open product '{name}'"):
            names = self.product_names()
            matches = [i for i, n in enumerate(names) if n.startswith(name)]
            assert matches, f"no product starting with '{name}' in {names}"
            self.driver.find_elements(*self.locator("product_images"))[matches[0]].click()


class ProductScreen(BaseScreen):
    def add_to_cart(self) -> None:
        with allure.step("Tap Add To Cart"):
            self.scroll_to("add_to_cart")
            self.tap("add_to_cart")


class CartScreen(BaseScreen):
    def item_count(self) -> int:
        """Android shows the count on the header badge; iOS shows 'N Items' on the cart screen."""
        if self.platform == "ios":
            self.open()
        text = self.text_of(self.find("cart_badge"))
        match = re.search(r"\d+", text)
        assert match, f"no item count in '{text}'"
        return int(match.group())

    def open(self) -> None:
        with allure.step("Open the cart"):
            self.tap("cart_icon")

    def has_checkout(self) -> bool:
        return self.find("checkout_button").is_displayed()
