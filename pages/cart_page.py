from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:
    CART_ITEMS = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    ITEM_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    ITEM_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-test="cart-list"]')
            )
        )

    def product_names(self):
        return [
            item.find_element(*self.ITEM_NAME).text
            for item in self.driver.find_elements(*self.CART_ITEMS)
        ]

    def product_price(self, product_name):
        for item in self.driver.find_elements(*self.CART_ITEMS):
            if item.find_element(*self.ITEM_NAME).text == product_name:
                return item.find_element(*self.ITEM_PRICE).text
        raise AssertionError(f"Không tìm thấy sản phẩm trong giỏ: {product_name}")

    def remove_product(self, product_name):
        for item in self.driver.find_elements(*self.CART_ITEMS):
            if item.find_element(*self.ITEM_NAME).text == product_name:
                button = item.find_element(By.CSS_SELECTOR, "button")
                # Xác nhận giỏ đã cập nhật bằng cách chờ dòng sản phẩm biến mất.
                self.driver.execute_script("arguments[0].click()", button)
                self.wait.until(lambda _: not self.product_names())
                return
        raise AssertionError(f"Không tìm thấy sản phẩm để xóa: {product_name}")
