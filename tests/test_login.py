"""
tests/test_login.py
Selenium tests for the Sauce Demo login page using the Page Object Model.

Target: https://www.saucedemo.com
Covers: valid credentials, invalid credentials, locked account, field validation,
        error banner dismissal.
"""

import pytest

from pages.login_page import LoginPage
from utils.config import Config


class TestLoginHappyPath:
    """Valid credential flows that should result in successful authentication."""

    def test_valid_login_redirects_to_inventory(self, login_page: LoginPage) -> None:
        """Standard user with correct credentials lands on the products page."""
        login_page.navigate()
        login_page.login(Config.STANDARD_USER, Config.STANDARD_PASS)
        login_page.wait_for_url_contains("inventory")

        assert "inventory.html" in login_page.current_url

    def test_page_title_is_correct_on_load(self, login_page: LoginPage) -> None:
        """The login page must carry a non-empty, meaningful document title."""
        login_page.navigate()

        assert login_page.title, "Page title must not be empty"
        assert "swag" in login_page.title.lower(), (
            f"Expected 'swag' in title, got: {login_page.title!r}"
        )

    def test_no_error_banner_on_initial_load(self, login_page: LoginPage) -> None:
        """Error banner must be absent before any login attempt."""
        login_page.navigate()

        assert not login_page.is_error_displayed()


class TestLoginErrorStates:
    """Invalid credential flows — all should surface an actionable error message."""

    def test_wrong_credentials_show_mismatch_error(self, login_page: LoginPage) -> None:
        """Unrecognised username/password combination triggers a clear error."""
        login_page.navigate()
        login_page.login("invalid_user", "wrong_password")

        assert login_page.is_error_displayed()
        assert "Username and password do not match" in login_page.get_error_message()

    def test_locked_out_user_shows_locked_message(self, login_page: LoginPage) -> None:
        """A locked account must produce a 'locked out' error, not a generic one."""
        login_page.navigate()
        login_page.login(Config.LOCKED_USER, Config.STANDARD_PASS)

        error = login_page.get_error_message()
        assert "locked out" in error.lower(), (
            f"Expected 'locked out' in error message, got: {error!r}"
        )

    def test_empty_username_shows_required_error(self, login_page: LoginPage) -> None:
        """Submitting with no username must request the username field."""
        login_page.navigate()
        login_page.login("", Config.STANDARD_PASS)

        assert "Username is required" in login_page.get_error_message()

    def test_empty_password_shows_required_error(self, login_page: LoginPage) -> None:
        """Submitting with no password must request the password field."""
        login_page.navigate()
        login_page.login(Config.STANDARD_USER, "")

        assert "Password is required" in login_page.get_error_message()

    def test_both_fields_empty_shows_username_error_first(
        self, login_page: LoginPage
    ) -> None:
        """When both fields are blank the username error takes precedence."""
        login_page.navigate()
        login_page.login("", "")

        assert "Username is required" in login_page.get_error_message()


class TestLoginErrorDismissal:
    """The error banner can be closed independently of any navigation."""

    def test_error_banner_dismisses_on_close_click(self, login_page: LoginPage) -> None:
        """Clicking × on the error banner makes it disappear."""
        login_page.navigate()
        login_page.login("bad_user", "bad_pass")

        assert login_page.is_error_displayed(), "Error banner should be visible after bad login"
        login_page.dismiss_error()
        assert not login_page.is_error_displayed(), "Error banner should be gone after dismissal"

    def test_after_dismissal_user_remains_on_login_page(
        self, login_page: LoginPage
    ) -> None:
        """Dismissing the error must not trigger any navigation."""
        login_page.navigate()
        login_page.login("bad_user", "bad_pass")
        login_page.dismiss_error()

        assert login_page.is_on_login_page()
