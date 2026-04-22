"""
pages/login_page.py
Page Object for the Sauce Demo login screen.

URL: https://www.saucedemo.com
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.config import Config


class LoginPage(BasePage):
    """Encapsulates all interactions with the Sauce Demo login page."""

    URL: str = Config.BASE_URL

    # ── Locators ──────────────────────────────────────────────────────────────
    _USERNAME_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")
    _LOGIN_BUTTON   = (By.ID, "login-button")
    _ERROR_BANNER   = (By.CSS_SELECTOR, "[data-test='error']")
    _ERROR_CLOSE    = (By.CSS_SELECTOR, ".error-button")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ── Actions ───────────────────────────────────────────────────────────────

    def navigate(self) -> LoginPage:
        self.open(self.URL)
        return self

    def enter_username(self, username: str) -> LoginPage:
        self.type_text(self._USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> LoginPage:
        self.type_text(self._PASSWORD_INPUT, password)
        return self

    def submit(self) -> LoginPage:
        self.click(self._LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str) -> LoginPage:
        """Convenience method: fill credentials and submit the form."""
        self.enter_username(username)
        self.enter_password(password)
        self.submit()
        return self

    def dismiss_error(self) -> LoginPage:
        """Click the × button to close the error banner."""
        self.click(self._ERROR_CLOSE)
        return self

    # ── Assertions / queries ──────────────────────────────────────────────────

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_BANNER)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self._ERROR_BANNER, timeout=4)

    def is_on_login_page(self) -> bool:
        return self.URL in self.current_url
