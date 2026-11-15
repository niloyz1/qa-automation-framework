"""Root fixtures and hooks shared by every suite."""

from __future__ import annotations

import os
import platform
from pathlib import Path

import pytest

from framework.config import ROOT, get_settings


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--platform",
        action="store",
        default=os.environ.get("MOBILE_PLATFORM", "android"),
        choices=("android", "ios"),
        help="Mobile platform for @mobile tests (default: android)",
    )


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture
def ctx() -> dict:
    """Per-scenario scratch space for passing values between Given/When/Then steps."""
    return {}


# --- Reporting -------------------------------------------------------------


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Expose each phase's result on the test item so fixtures can react to failures."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


def pytest_sessionfinish(session: pytest.Session) -> None:
    """Write environment details shown on the Allure report's overview page."""
    results = Path(session.config.getoption("--alluredir", default=None) or ROOT / "reports/allure-results")
    if not results.is_absolute():
        results = ROOT / results
    results.mkdir(parents=True, exist_ok=True)
    s = get_settings()
    browser = session.config.getoption("--browser", default=None) if hasattr(session.config.option, "browser") else None
    lines = {
        "Environment": s.env,
        "Python": platform.python_version(),
        "OS": f"{platform.system()} {platform.release()}",
        "Browser": ", ".join(browser) if isinstance(browser, list) and browser else "chromium",
        "Mobile platform": session.config.getoption("--platform"),
        "Portfolio URL": s.portfolio_url,
        "Shop URL": s.saucedemo_url,
        "API URL": s.api_url,
        "CI": "GitHub Actions" if os.environ.get("GITHUB_ACTIONS") else "local",
    }
    (results / "environment.properties").write_text(
        "\n".join(f"{k.replace(' ', '.')}={v}" for k, v in lines.items()), encoding="utf-8"
    )
    categories = ROOT / "config" / "allure-categories.json"
    if categories.exists():
        (results / "categories.json").write_text(categories.read_text(encoding="utf-8"), encoding="utf-8")
