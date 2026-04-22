"""
utils/config.py
Central configuration loaded from environment variables with safe defaults.
Override any value by exporting the corresponding env var before running pytest.

    export BROWSER=firefox HEADLESS=false pytest tests/
"""

import os
from pathlib import Path


class Config:
    # ── Target application ───────────────────────────────────────────────────
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")

    # ── Browser settings ─────────────────────────────────────────────────────
    BROWSER: str = os.getenv("BROWSER", "chrome").lower()
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    WINDOW_WIDTH: int = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT: int = int(os.getenv("WINDOW_HEIGHT", "1080"))

    # ── Wait strategy ────────────────────────────────────────────────────────
    # Always use explicit waits (WebDriverWait). Implicit wait stays at 0.
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    # ── Test credentials (Sauce Demo public demo site) ───────────────────────
    STANDARD_USER: str = os.getenv("TEST_USERNAME", "standard_user")
    STANDARD_PASS: str = os.getenv("TEST_PASSWORD", "secret_sauce")
    LOCKED_USER: str = os.getenv("LOCKED_USER", "locked_out_user")

    # ── Reporting ────────────────────────────────────────────────────────────
    REPORTS_DIR: Path = Path(os.getenv("REPORTS_DIR", "reports"))
    SCREENSHOT_ON_FAILURE: bool = (
        os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    )
