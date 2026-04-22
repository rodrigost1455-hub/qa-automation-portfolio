"""
utils/driver_factory.py
Creates and configures WebDriver instances.

Selenium 4.6+ ships with Selenium Manager, which automatically resolves and
downloads the correct browser driver binary — no webdriver-manager required.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from utils.config import Config


class DriverFactory:
    """Factory for creating configured WebDriver instances."""

    @staticmethod
    def create_driver(
        browser: str | None = None,
        headless: bool | None = None,
    ) -> WebDriver:
        """
        Return a fully configured WebDriver.

        Args:
            browser: 'chrome' or 'firefox' (falls back to Config.BROWSER).
            headless: Run without UI when True (falls back to Config.HEADLESS).
        """
        browser = (browser or Config.BROWSER).lower()
        headless = Config.HEADLESS if headless is None else headless

        creators = {
            "chrome": DriverFactory._chrome,
            "firefox": DriverFactory._firefox,
        }
        if browser not in creators:
            raise ValueError(
                f"Unsupported browser '{browser}'. Choose from: {list(creators)}"
            )

        driver = creators[browser](headless)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        # Explicit waits are used throughout the framework; implicit wait is OFF.
        driver.implicitly_wait(0)
        return driver

    # ── Private browser builders ─────────────────────────────────────────────

    @staticmethod
    def _chrome(headless: bool) -> WebDriver:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(
            f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}"
        )
        # Suppress automation banners and unnecessary logging
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        return webdriver.Chrome(options=options)

    @staticmethod
    def _firefox(headless: bool) -> WebDriver:
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument(f"--width={Config.WINDOW_WIDTH}")
        options.add_argument(f"--height={Config.WINDOW_HEIGHT}")
        return webdriver.Firefox(options=options)
