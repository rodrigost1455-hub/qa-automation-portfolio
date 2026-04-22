"""
pages/form_page.py
Page Object for the Sauce Demo checkout form (3-step flow).

Step 1 — Cart:           /cart.html
Step 2 — Customer Info:  /checkout-step-one.html
Step 3 — Order Overview: /checkout-step-two.html
Step 4 — Confirmation:   /checkout-complete.html
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from utils.config import Config


class FormPage(BasePage):
    """Encapsulates the entire Sauce Demo checkout form flow."""

    # ── Page URLs ─────────────────────────────────────────────────────────────
    CART_URL     = f"{Config.BASE_URL}/cart.html"
    STEP_ONE_URL = f"{Config.BASE_URL}/checkout-step-one.html"
    STEP_TWO_URL = f"{Config.BASE_URL}/checkout-step-two.html"
    COMPLETE_URL = f"{Config.BASE_URL}/checkout-complete.html"

    # ── Locators — Cart ───────────────────────────────────────────────────────
    _CHECKOUT_BUTTON = (By.ID, "checkout")

    # ── Locators — Step 1 (Customer Info) ────────────────────────────────────
    _FIRST_NAME    = (By.ID, "first-name")
    _LAST_NAME     = (By.ID, "last-name")
    _POSTAL_CODE   = (By.ID, "postal-code")
    _CONTINUE_BTN  = (By.ID, "continue")
    _CANCEL_BTN    = (By.ID, "cancel")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # ── Locators — Step 2 (Overview) ─────────────────────────────────────────
    _FINISH_BTN        = (By.ID, "finish")
    _ORDER_TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")

    # ── Locators — Step 3 (Confirmation) ─────────────────────────────────────
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    _COMPLETE_TEXT   = (By.CLASS_NAME, "complete-text")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ── Navigation helpers ────────────────────────────────────────────────────

    def navigate_to_cart(self) -> FormPage:
        self.open(self.CART_URL)
        return self

    # ── Cart actions ──────────────────────────────────────────────────────────

    def proceed_to_checkout(self) -> FormPage:
        self.click(self._CHECKOUT_BUTTON)
        return self

    # ── Step 1 actions ────────────────────────────────────────────────────────

    def fill_customer_info(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ) -> FormPage:
        self.type_text(self._FIRST_NAME, first_name)
        self.type_text(self._LAST_NAME, last_name)
        self.type_text(self._POSTAL_CODE, postal_code)
        return self

    def continue_to_overview(self) -> FormPage:
        self.click(self._CONTINUE_BTN)
        return self

    def cancel_checkout(self) -> FormPage:
        self.click(self._CANCEL_BTN)
        return self

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self._ERROR_MESSAGE, timeout=4)

    # ── Step 2 actions ────────────────────────────────────────────────────────

    def finish_order(self) -> FormPage:
        self.click(self._FINISH_BTN)
        return self

    def get_order_total(self) -> str:
        return self.get_text(self._ORDER_TOTAL_LABEL)

    # ── Step 3 queries ────────────────────────────────────────────────────────

    def get_completion_header(self) -> str:
        return self.get_text(self._COMPLETE_HEADER)

    def get_completion_text(self) -> str:
        return self.get_text(self._COMPLETE_TEXT)

    # ── Field visibility checks ───────────────────────────────────────────────

    def is_first_name_field_present(self) -> bool:
        return self.is_visible(self._FIRST_NAME)

    def is_last_name_field_present(self) -> bool:
        return self.is_visible(self._LAST_NAME)

    def is_postal_code_field_present(self) -> bool:
        return self.is_visible(self._POSTAL_CODE)
