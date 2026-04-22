"""
tests/test_search.py
Selenium tests for the Sauce Demo product inventory page using the Page Object Model.

Target: https://www.saucedemo.com/inventory.html
Covers: product listing, sort by name (A→Z / Z→A), sort by price (low→high /
        high→low), add-to-cart badge update.

All tests require an authenticated session.  The `authenticated` fixture handles
login before each test; the driver fixture (conftest.py) handles teardown.
"""

import pytest

from pages.login_page import LoginPage
from pages.search_page import SearchPage
from utils.config import Config

EXPECTED_PRODUCT_COUNT = 6


@pytest.fixture(autouse=True)
def authenticated(driver) -> None:
    """Log in as the standard user before every test in this module."""
    login = LoginPage(driver)
    login.navigate()
    login.login(Config.STANDARD_USER, Config.STANDARD_PASS)
    login.wait_for_url_contains("inventory")


class TestProductListing:
    """Basic inventory page render checks."""

    def test_inventory_displays_correct_product_count(
        self, search_page: SearchPage
    ) -> None:
        """Sauce Demo exposes exactly 6 products on a fresh session."""
        assert search_page.get_product_count() == EXPECTED_PRODUCT_COUNT

    def test_all_product_names_are_non_empty(self, search_page: SearchPage) -> None:
        """Every product must carry a non-blank display name."""
        names = search_page.get_product_names()
        assert len(names) == EXPECTED_PRODUCT_COUNT
        assert all(name.strip() for name in names), "Found a product with an empty name"

    def test_all_product_prices_are_positive(self, search_page: SearchPage) -> None:
        """Every listed price must be a positive dollar amount."""
        prices = search_page.get_product_prices()
        assert len(prices) == EXPECTED_PRODUCT_COUNT
        assert all(price > 0 for price in prices), f"Non-positive price detected: {prices}"

    def test_page_title_reads_products(self, search_page: SearchPage) -> None:
        """The inventory page header must say 'Products'."""
        assert search_page.get_page_title() == "Products"


class TestProductSorting:
    """Sorting interactions and resulting order correctness."""

    def test_sort_name_a_to_z_produces_ascending_order(
        self, search_page: SearchPage
    ) -> None:
        search_page.sort_by(SearchPage.SortOption.NAME_A_TO_Z)
        names = search_page.get_product_names()

        assert names == sorted(names), (
            f"Names not in A→Z order.\n  Got:      {names}\n"
            f"  Expected: {sorted(names)}"
        )

    def test_sort_name_z_to_a_produces_descending_order(
        self, search_page: SearchPage
    ) -> None:
        search_page.sort_by(SearchPage.SortOption.NAME_Z_TO_A)
        names = search_page.get_product_names()

        assert names == sorted(names, reverse=True), (
            f"Names not in Z→A order.\n  Got:      {names}\n"
            f"  Expected: {sorted(names, reverse=True)}"
        )

    def test_sort_price_low_to_high_produces_ascending_order(
        self, search_page: SearchPage
    ) -> None:
        search_page.sort_by(SearchPage.SortOption.PRICE_LOW_HIGH)
        prices = search_page.get_product_prices()

        assert prices == sorted(prices), (
            f"Prices not in low→high order.\n  Got:      {prices}\n"
            f"  Expected: {sorted(prices)}"
        )

    def test_sort_price_high_to_low_produces_descending_order(
        self, search_page: SearchPage
    ) -> None:
        search_page.sort_by(SearchPage.SortOption.PRICE_HIGH_LOW)
        prices = search_page.get_product_prices()

        assert prices == sorted(prices, reverse=True), (
            f"Prices not in high→low order.\n  Got:      {prices}\n"
            f"  Expected: {sorted(prices, reverse=True)}"
        )


class TestCartInteraction:
    """Add-to-cart interactions reflected in the cart badge."""

    def test_add_first_product_increments_cart_badge(
        self, search_page: SearchPage
    ) -> None:
        """Adding one item must make the cart badge display '1'."""
        initial_count = search_page.get_cart_item_count()
        search_page.add_product_to_cart(index=0)
        updated_count = search_page.get_cart_item_count()

        assert updated_count == initial_count + 1, (
            f"Cart badge expected {initial_count + 1}, got {updated_count}"
        )

    def test_add_two_products_cart_badge_shows_two(
        self, search_page: SearchPage
    ) -> None:
        """Adding two items sequentially must accumulate the badge to 2."""
        search_page.add_product_to_cart(index=0)
        search_page.add_product_to_cart(index=1)

        assert search_page.get_cart_item_count() == 2
