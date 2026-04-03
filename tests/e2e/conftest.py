"""
tests/e2e/conftest.py
Shared fixtures and configuration for Playwright E2E tests.
Uses pytest-playwright (sync API).
"""
import re
import pytest
from playwright.sync_api import Page, expect


# ── Base URLs — adjust if your local servers run on different ports ──────────
BASE_URL_8D  = "http://localhost:3001"   # 8D QMS (React + Node.js)
BASE_URL_FA  = "http://localhost:8000"   # FA Report System (FastAPI)


# ── Session-scoped URL fixtures ──────────────────────────────────────────────
@pytest.fixture(scope="session")
def base_url_8d() -> str:
    return BASE_URL_8D


@pytest.fixture(scope="session")
def base_url_fa() -> str:
    return BASE_URL_FA


# ── Shared data fixtures ─────────────────────────────────────────────────────
@pytest.fixture
def valid_8d_payload() -> dict:
    """Minimum valid payload to create a new 8D non-conformance report."""
    return {
        "report_number": "E2E-TEST-001",
        "customer":      "General Motors",
        "part_number":   "L1M8-10C666-GF",
        "part_name":     "PHEV BEC Gen4",
        "description":   "Short circuit detected in BEC connector during EOL test",
        "quantity":      12,
    }


@pytest.fixture
def second_8d_payload() -> dict:
    """Second payload — used for list and filtering tests."""
    return {
        "report_number": "E2E-TEST-002",
        "customer":      "Ford Motor Company",
        "part_number":   "7370-2573-8W",
        "part_name":     "Wiring Harness Assy",
        "description":   "Open circuit on pin 14 detected after thermal cycling",
        "quantity":      5,
    }


# ── Helper: navigate to app and wait for it to be ready ─────────────────────
@pytest.fixture
def app_page(page: Page, base_url_8d: str):
    """
    Pre-navigated Page fixture — goes to the 8D app and waits for it to load.
    Use this instead of raw 'page' when you need the app already open.
    """
    page.goto(base_url_8d)
    page.wait_for_load_state("networkidle", timeout=15_000)
    return page
