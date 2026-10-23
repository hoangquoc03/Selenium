from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class InventoryPage:
    INVENTORY_ITEMS = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    ITEM_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    ITEM_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    SORT_SELECT = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_ITEMS))

    def add_product(self, product_name):
        for item in self.driver.find_elements(*self.INVENTORY_ITEMS):
            name = item.find_element(*self.ITEM_NAME).text
            if name == product_name:
                button = item.find_element(By.CSS_SELECTOR, "button")
                # Phát click cho nút React và xác nhận bằng badge sau thao tác.
                self.driver.execute_script("arguments[0].click()", button)
                self.wait.until(EC.visibility_of_element_located(self.CART_BADGE))
                return
        raise AssertionError(f"Không tìm thấy sản phẩm: {product_name}")

    def cart_badge_count(self):
        badge = self.wait.until(EC.visibility_of_element_located(self.CART_BADGE))
        return int(badge.text)

    def open_cart(self):
        cart_link = self.wait.until(EC.element_to_be_clickable(self.CART_LINK))
        # Gọi handler React trực tiếp vì liên kết giỏ hàng không có thuộc tính href.
        self.driver.execute_script("arguments[0].click()", cart_link)
        self.wait.until(EC.url_contains("cart.html"))

    def sort_price_low_to_high(self):
        Select(self.driver.find_element(*self.SORT_SELECT)).select_by_value("lohi")

    def product_prices(self):
        self.wait.until(EC.visibility_of_all_elements_located(self.INVENTORY_ITEMS))
        return [
            Decimal(
                item.find_element(*self.ITEM_PRICE).text.replace("$", "").strip()
            )
            for item in self.driver.find_elements(*self.INVENTORY_ITEMS)
        ]

    def logout(self):
        menu_button = self.wait.until(EC.element_to_be_clickable(self.MENU_BUTTON))
        self.driver.execute_script("arguments[0].click()", menu_button)
        logout_link = (By.CSS_SELECTOR, '[data-test="logout-sidebar-link"]')
        link = self.wait.until(EC.element_to_be_clickable(logout_link))
        # Mục Logout cũng là nút React được dựng dưới dạng thẻ a không có href.
        self.driver.execute_script("arguments[0].click()", link)
