"""
pages/base_page.py
Abstract base class for all Page Objects.

Wraps Selenium's WebDriverWait so every page interaction uses explicit waits.
No time.sleep() calls exist anywhere in this framework.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import Config
from utils.helpers import take_screenshot

if TYPE_CHECKING:
    from selenium.webdriver.common.by import By

# Type alias: a locator is always a (By.*, "selector") tuple
Locator = tuple[str, str]


class BasePage:
    """
    Provides reusable, wait-aware wrappers around common Selenium operations.
    All page classes must inherit from this.
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self._wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self, url: str) -> BasePage:
        self.driver.get(url)
        return self

    def wait_for_url_contains(self, fragment: str, timeout: int | None = None) -> None:
        wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
        wait.until(EC.url_contains(fragment))

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def title(self) -> str:
        return self.driver.title

    # ── Element finders ───────────────────────────────────────────────────────

    def find(self, locator: Locator, timeout: int | None = None) -> WebElement:
        """Wait until the element is present in the DOM, then return it."""
        wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
        return wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: Locator, timeout: int | None = None) -> WebElement:
        """Wait until the element is visible, then return it."""
        wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
        return wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator: Locator, timeout: int | None = None) -> WebElement:
        """Wait until the element is clickable, then return it."""
        wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
        return wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator: Locator, timeout: int | None = None) -> list[WebElement]:
        """Wait until at least one element is present, then return all matches."""
        wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def is_visible(self, locator: Locator, timeout: int = 3) -> bool:
        """Return True if the element becomes visible within *timeout* seconds."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ── Interactions ──────────────────────────────────────────────────────────

    def click(self, locator: Locator) -> None:
        self.find_clickable(locator).click()

    def type_text(self, locator: Locator, text: str) -> None:
        """Clear any existing value, then type *text* into the field."""
        element = self.find_clickable(locator)
        element.clear()
        element.send_keys(text)

    # ── Data extraction ───────────────────────────────────────────────────────

    def get_text(self, locator: Locator) -> str:
        return self.find_visible(locator).text.strip()

    def get_texts(self, locator: Locator) -> list[str]:
        """Return the visible text of every matched element."""
        return [el.text.strip() for el in self.find_all(locator)]

    def get_attribute(self, locator: Locator, attribute: str) -> str:
        return self.find(locator).get_attribute(attribute) or ""

    # ── Utilities ─────────────────────────────────────────────────────────────

    def screenshot(self, name: str) -> str:
        """Save a screenshot to the reports directory and return its path."""
        return take_screenshot(self.driver, name)
