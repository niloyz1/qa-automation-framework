"""saucedemo.com login page."""

from __future__ import annotations

import allure
from playwright.sync_api import expect

from framework.web.pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    @property
    def username(self):
        return self.by_test_id("username")

    @property
    def password(self):
        return self.by_test_id("password")

    @property
    def login_button(self):
        return self.by_test_id("login-button")

    @property
    def error(self):
        return self.by_test_id("error")

    def login(self, username: str, password: str) -> None:
        with allure.step(f"Log in as '{username}'"):
            self.username.fill(username)
            self.password.fill(password)
            self.login_button.click()

    def expect_error(self, text: str) -> None:
        expect(self.error).to_contain_text(text)
