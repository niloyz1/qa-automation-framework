"""Step definitions for features/web/portfolio.feature (niloyzaman.com)."""

from __future__ import annotations

import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from framework.web.pages import PortfolioPage

scenarios("web/portfolio.feature")


@pytest.fixture
def portfolio(page, settings) -> PortfolioPage:
    return PortfolioPage(page, settings.portfolio_url)


@given("I open the portfolio home page")
def open_home(portfolio):
    portfolio.open()


@when("I run the in-page release suite")
def run_suite(portfolio):
    portfolio.run_release_suite()


@when(parsers.parse('I open the "{tab}" console tab'))
def open_tab(portfolio, tab):
    portfolio.tab(tab).click()


@when(parsers.parse('I evaluate model answer "{letter}"'))
def evaluate_answer(portfolio, letter):
    portfolio.choose_eval_answer(letter)


@when(parsers.parse('I type "{command}" in the terminal'))
def type_command(portfolio, command):
    portfolio.run_terminal_command(command)


@when("I switch the colour theme")
def switch_theme(portfolio, ctx):
    ctx["theme_before"] = portfolio.current_theme()
    portfolio.toggle_theme()


@then(parsers.parse('the main heading should contain "{text}"'))
def heading_contains(portfolio, text):
    expect(portfolio.heading).to_contain_text(text)


@then(parsers.parse('the main navigation should link to "{a}", "{b}" and "{c}"'))
def nav_links(portfolio, a, b, c):
    links = portfolio.section_links()
    assert [a, b, c] == links[:3], f"navigation links were {links}"


@then(parsers.parse('the suite summary should report "{text}"'))
def suite_summary(portfolio, text):
    expect(portfolio.page.locator("#summary")).to_contain_text(text)


@then(parsers.parse('the verdict should be "{verdict}"'))
def verdict_is(portfolio, verdict):
    expect(portfolio.page.locator("#verdict")).to_have_text(verdict)


@then(parsers.parse('the terminal output should contain "{text}"'))
def terminal_contains(portfolio, text):
    expect(portfolio.page.locator("#term-out")).to_contain_text(text)


@then("the theme should change")
def theme_changed(portfolio, ctx):
    after = portfolio.current_theme()
    assert after != ctx["theme_before"], f"theme stayed '{after}'"
