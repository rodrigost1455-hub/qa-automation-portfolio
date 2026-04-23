"""
pages/search_page.py
Page Object for the Sauce Demo product inventory / search page.

URL: https://www.saucedemo.com/inventory.html
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.base_page import BasePage
from utils.config import Config


class SearchPage(BasePage):
    """Encapsulates product listing, sorting, and cart interactions."""

    URL: str = f"{Config.BASE_URL}/inventory.html"

    # ── Sort option constants ─────────────────────────────────────────────────
    class SortOption:
        NAME_A_TO_Z    = "az"
        NAME_Z_TO_A    = "za"
        PRICE_LOW_HIGH = "lohi"
        PRICE_HIGH_LOW = "hilo"

    # ── Locators ──────────────────────────────────────────────────────────────
    _SORT_DROPDOWN    = (By.CLASS_NAME, "product_sort_container")
    _PRODUCT_NAMES    = (By.CLASS_NAME, "inventory_item_name")
    _PRODUCT_PRICES   = (By.CLASS_NAME, "inventory_item_price")
    _PRODUCT_CARDS    = (By.CLASS_NAME, "inventory_item")
    _ADD_TO_CART_BTNS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    _CART_BADGE       = (By.CLASS_NAME, "shopping_cart_badge")
    _PAGE_TITLE       = (By.CLASS_NAME, "title")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate(self) -> SearchPage:
        self.open(self.URL)
        return self

    # ── Queries ───────────────────────────────────────────────────────────────

    def get_product_names(self) -> list[str]:
        return self.get_texts(self._PRODUCT_NAMES)

    def get_product_prices(self) -> list[float]:
        """Return product prices as floats, e.g. [7.99, 9.99, ...]."""
        raw_prices = self.get_texts(self._PRODUCT_PRICES)
        return [float(p.replace("$", "")) for p in raw_prices]

    def get_product_count(self) -> int:
        return len(self.find_all(self._PRODUCT_CARDS))

    def get_cart_item_count(self) -> int:
        """Return number shown on the cart badge, or 0 if the badge is absent."""
        if self.is_visible(self._CART_BADGE, timeout=3):
            return int(self.get_text(self._CART_BADGE))
        return 0

    def get_page_title(self) -> str:
        return self.get_text(self._PAGE_TITLE)

    # ── Actions ───────────────────────────────────────────────────────────────

    def sort_by(self, option: str) -> SearchPage:
        """Select a sort option using its value attribute."""
        dropdown_element = self.find_clickable(self._SORT_DROPDOWN)
        Select(dropdown_element).select_by_value(option)
        return self

    def add_product_to_cart(self, index: int = 0) -> SearchPage:
        """Click the 'Add to cart' button for the product at *index* and wait
        for the cart badge to confirm the item was added before returning.

        Waiting for the badge count to increment is the most reliable signal
        that the React state transition has completed in the DOM.
        """
        count_before = self.get_cart_item_count()
        buttons = self.find_all(self._ADD_TO_CART_BTNS)
        buttons[index].click()
        # Wait until the cart badge reflects the new item count
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            lambda d: self.get_cart_item_count() > count_before
        )
        return self
