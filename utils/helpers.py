"""
utils/helpers.py
Shared helper utilities: screenshot capture, logging setup, test data generators.
"""

import logging
import uuid
from datetime import datetime
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from utils.config import Config


def setup_logger(name: str = __name__) -> logging.Logger:
    """Return a logger that writes ISO-8601 timestamps and level labels."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    return logging.getLogger(name)


def take_screenshot(driver: WebDriver, test_name: str) -> str:
    """
    Capture a PNG screenshot and save it to the reports directory.

    Returns the absolute path of the saved file.
    """
    Config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = test_name.replace("/", "_").replace("::", "__")
    filename = Config.REPORTS_DIR / f"{safe_name}_{timestamp}.png"
    driver.save_screenshot(str(filename))
    return str(filename)


def generate_test_id(prefix: str = "TEST") -> str:
    """Generate a short unique identifier for dynamic test data."""
    return f"{prefix}-{str(uuid.uuid4())[:8].upper()}"


def build_url(path: str = "") -> str:
    """Construct a full URL from the configured base and a relative path."""
    return f"{Config.BASE_URL.rstrip('/')}/{path.lstrip('/')}"
