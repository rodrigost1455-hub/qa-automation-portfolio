"""
conftest.py
Root-level pytest configuration: shared fixtures for every test suite.

Selenium fixtures  ── driver, login_page, search_page, form_page
Schema fixtures    ── valid_report_payload, ntf_report_payload (legacy unit tests)
Hooks              ── auto-screenshot on test failure, report directory setup
"""

import uuid
from datetime import date

import pytest

from pages.form_page import FormPage
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from utils.config import Config
from utils.driver_factory import DriverFactory
from utils.helpers import take_screenshot


# ── Pytest hook: capture test outcome so fixtures can detect failure ──────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    # Attach the outcome to the test item for access inside fixtures
    setattr(item, f"rep_{rep.when}", rep)


# ── Session-wide setup ────────────────────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def ensure_reports_directory():
    """Guarantee the reports/ directory exists before any test runs."""
    Config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ── Selenium WebDriver ────────────────────────────────────────────────────────

@pytest.fixture
def driver(request):
    """
    Provision a WebDriver instance for a single test.

    Teardown: captures a screenshot on failure (if SCREENSHOT_ON_FAILURE is set),
    then quits the driver to release browser resources.
    """
    drv = DriverFactory.create_driver()
    yield drv

    # Screenshot before quit so the browser window is still open
    if Config.SCREENSHOT_ON_FAILURE:
        call_outcome = getattr(request.node, "rep_call", None)
        if call_outcome is not None and call_outcome.failed:
            path = take_screenshot(drv, request.node.name)
            print(f"\n[Screenshot on failure] {path}")

    drv.quit()


# ── Page Object fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def login_page(driver) -> LoginPage:
    return LoginPage(driver)


@pytest.fixture
def search_page(driver) -> SearchPage:
    return SearchPage(driver)


@pytest.fixture
def form_page(driver) -> FormPage:
    return FormPage(driver)


# ── Legacy schema/API fixtures (unit & integration test suites) ───────────────

@pytest.fixture
def today():
    return date.today()


@pytest.fixture
def valid_report_payload():
    return {
        "report_number":      "2506-001",
        "title":              "Warranty Plant Return",
        "request_date":       date.today(),
        "part_name":          "PHEV BEC GEN 4",
        "part_number":        "L1M8 10C666 GF",
        "yazaki_part_number": "7370-2573-8W",
        "prepared_by_name":   "Rodrigo Santana",
        "is_ntf":             False,
        "reuse_images":       False,
    }


@pytest.fixture
def ntf_report_payload(valid_report_payload):
    return {
        **valid_report_payload,
        "report_number":   "2506-002",
        "is_ntf":          True,
        "reuse_images":    True,
        "source_report_id": str(uuid.uuid4()),
    }
