"""Appium driver factory for Android (UiAutomator2) and iOS (XCUITest)."""

from __future__ import annotations

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

from framework.config import ROOT, Settings


def create_driver(platform: str, settings: Settings) -> webdriver.Remote:
    mobile = settings.mobile
    platform = platform.lower()
    if platform == "android":
        cfg = mobile["android"]
        options = UiAutomator2Options()
        options.device_name = cfg["device_name"]
        options.app = str(ROOT / cfg["app"])
        options.app_package = cfg["app_package"]
        options.app_activity = cfg["app_activity"]
        options.app_wait_activity = "*"
        options.auto_grant_permissions = True
        options.new_command_timeout = 120
    elif platform == "ios":
        cfg = mobile["ios"]
        options = XCUITestOptions()
        options.device_name = cfg["device_name"]
        options.platform_version = cfg["platform_version"]
        options.app = str(ROOT / cfg["app"])
        options.bundle_id = cfg["bundle_id"]
        options.auto_accept_alerts = True
        options.new_command_timeout = 120
        options.wda_launch_timeout = 240000
    else:
        raise ValueError(f"Unsupported platform '{platform}' (use android or ios)")
    return webdriver.Remote(mobile["appium_url"], options=options)
