"""
tests/test_form.py
Selenium tests for the Sauce Demo checkout form (3-step flow) using the POM.

Target: https://www.saucedemo.com
Covers: form field visibility, required-field validation, happy-path checkout,
        cancel navigation, and end-to-end order completion.

The `setup_cart` fixture authenticates and pre-loads the cart with one item so
every checkout test starts from a consistent state.
"""

import pytest

from pages.form_page import FormPage
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from utils.config import Config


@pytest.fixture(autouse=True)
def setup_cart(driver) -> None:
    """Authenticate and add one product to the cart before each test."""
    login = LoginPage(driver)
    login.navigate()
    login.login(Config.STANDARD_USER, Config.STANDARD_PASS)
    login.wait_for_url_contains("inventory")

    products = SearchPage(driver)
    products.add_product_to_cart(index=0)


class TestCheckoutFormFields:
    """Verify that step-one of checkout renders the correct input fields."""

    def test_all_required_fields_are_present(self, form_page: FormPage) -> None:
        """First Name, Last Name, and Postal Code fields must all be visible."""
        form_page.navigate_to_cart()
        form_page.proceed_to_checkout()

        assert form_page.is_first_name_field_present(), "First Name field not visible"
        assert form_page.is_last_name_field_present(), "Last Name field not visible"
        assert form_page.is_postal_code_field_present(), "Postal Code field not visible"

    def test_checkout_url_is_step_one(self, form_page: FormPage) -> None:
        """Clicking Checkout from the cart navigates to step-one."""
        form_page.navigate_to_cart()
        form_page.proceed_to_checkout()
        form_page.wait_for_url_contains("checkout-step-one")

        assert "checkout-step-one" in form_page.current_url


class TestCheckoutFormValidation:
    """Required-field validation on the customer info step."""

    def test_empty_submit_shows_first_name_error(self, form_page: FormPage) -> None:
        """Submitting with all fields blank must ask for First Name."""
        form_page.navigate_to_cart()
        form_page.proceed_to_checkout()
        form_page.continue_to_overview()

        assert form_page.is_error_displayed()
        assert "First Name is required" in form_page.get_error_message()

    def test_missing_last_name_shows_last_name_error(
        self, form_page: FormPage
    ) -> None:
        """Filling only First Name must ask for Last Name."""
        form_page.navigate_to_cart()
        form_page.proceed_to_checkout()
        form_page.fill_customer_info("John", "", "")
        form_page.continue_to_overview()

        assert "Last Name is required" in form_page.get_error_message()

    def test_missing_postal_code_shows_zip_error(self, form_page: FormPage) -> None:
        """Filling name but not zip must ask for the postal code."""
        form_page.navigate_to_cart()
        form_page.proceed_to_checkout()
        form_page.fill_customer_info("John", "Doe", "")
        form_page.continue_to_overview()

        assert "Postal Code is required" in form_page.get_error_message()


class TestCheckoutNavigation:
    """Navigation flows within the checkout funnel."""

    def test_cancel_from_step_one_returns_to_cart(
        self, form_page: FormPage
    ) -> None:
        """Cancel on the info step must route back to the cart."""
        form_page.navigate_to_cart()
        form_page.proceed_to_checkout()
        form_page.cancel_checkout()
        form_page.wait_for_url_contains("cart")

        assert "cart.html" in form_page.current_url

    def test_valid_info_advances_to_overview(self, form_page: FormPage) -> None:
        """Completing all fields correctly must advance to the order overview."""
        form_page.navigate_to_cart()
        form_page.proceed_to_checkout()
        form_page.fill_customer_info("Jane", "Doe", "90210")
        form_page.continue_to_overview()
        form_page.wait_for_url_contains("checkout-step-two")

        assert "checkout-step-two" in form_page.current_url

    def test_overview_displays_order_total(self, form_page: FormPage) -> None:
        """The order overview must show a total price label."""
        form_page.navigate_to_cart()
        form_page.proceed_to_checkout()
        form_page.fill_customer_info("Jane", "Doe", "90210")
        form_page.continue_to_overview()

        total = form_page.get_order_total()
        assert "Total:" in total, f"Expected 'Total:' in order summary, got: {total!r}"


class TestCheckoutCompletion:
    """Full end-to-end order placement through to confirmation."""

    def test_completed_order_shows_thank_you_header(
        self, form_page: FormPage
    ) -> None:
        """Finishing a valid order must show a 'Thank you' confirmation header."""
        form_page.navigate_to_cart()
        form_page.proceed_to_checkout()
        form_page.fill_customer_info("Alice", "Smith", "12345")
        form_page.continue_to_overview()
        form_page.finish_order()
        form_page.wait_for_url_contains("checkout-complete")

        header = form_page.get_completion_header()
        assert "Thank you for your order" in header, (
            f"Unexpected completion header: {header!r}"
        )

    def test_completion_page_url_is_correct(self, form_page: FormPage) -> None:
        """The post-order URL must point to the checkout-complete page."""
        form_page.navigate_to_cart()
        form_page.proceed_to_checkout()
        form_page.fill_customer_info("Bob", "Jones", "54321")
        form_page.continue_to_overview()
        form_page.finish_order()
        form_page.wait_for_url_contains("checkout-complete")

        assert "checkout-complete.html" in form_page.current_url
