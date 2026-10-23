from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.conftest import DEMO_PASSWORD, DEMO_USERNAME

PRODUCT_NAME = "Sauce Labs Backpack"


def test_login_success(driver):
    """TC01: Đăng nhập bằng tài khoản demo hợp lệ."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)

    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    assert driver.find_element(
        By.CSS_SELECTOR, '[data-test="inventory-container"]'
    ).is_displayed()


def test_login_invalid_credentials(driver):
    """TC02: Thông báo lỗi xuất hiện khi thông tin đăng nhập không hợp lệ."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("invalid_user", "wrong_password")

    assert "Username and password do not match" in login_page.error_text()


def test_login_with_blank_username(driver):
    """TC03: Để trống username phải hiển thị thông báo phù hợp."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("", DEMO_PASSWORD)

    assert login_page.error_text() == "Epic sadface: Username is required"


def test_add_product_to_cart(logged_in_driver):
    """TC04: Số lượng sản phẩm trên biểu tượng giỏ hàng tăng sau khi thêm."""
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_product(PRODUCT_NAME)

    assert inventory_page.cart_badge_count() == 1


def test_remove_product_from_cart(logged_in_driver):
    """TC05: Có thể xóa sản phẩm đã thêm khỏi giỏ hàng."""
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_product(PRODUCT_NAME)
    inventory_page.open_cart()
    cart_page = CartPage(logged_in_driver)

    cart_page.remove_product(PRODUCT_NAME)

    assert PRODUCT_NAME not in cart_page.product_names()
    assert not logged_in_driver.find_elements(
        By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]'
    )


def test_sort_products_by_price_low_to_high(logged_in_driver):
    """TC06: Giá sản phẩm sau khi sắp xếp tăng dần không giảm."""
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.sort_price_low_to_high()
    prices = inventory_page.product_prices()

    assert len(prices) > 1
    assert prices == sorted(prices)


def test_cart_product_name_and_price_match(logged_in_driver):
    """TC07: Tên và giá trong giỏ khớp với sản phẩm được chọn."""
    inventory_page = InventoryPage(logged_in_driver)
    expected_price = next(
        Decimal(
            item.find_element(*InventoryPage.ITEM_PRICE).text.replace("$", "").strip()
        )
        for item in logged_in_driver.find_elements(*InventoryPage.INVENTORY_ITEMS)
        if item.find_element(*InventoryPage.ITEM_NAME).text == PRODUCT_NAME
    )
    inventory_page.add_product(PRODUCT_NAME)
    inventory_page.open_cart()
    cart_page = CartPage(logged_in_driver)

    assert PRODUCT_NAME in cart_page.product_names()
    actual_price = Decimal(cart_page.product_price(PRODUCT_NAME).replace("$", ""))
    assert actual_price == expected_price


def test_logout_success(logged_in_driver):
    """TC08: Đăng xuất đưa người dùng trở lại màn hình đăng nhập."""
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.logout()

    WebDriverWait(logged_in_driver, 20).until(
        EC.visibility_of_element_located(LoginPage.LOGIN_BUTTON)
    )
    assert logged_in_driver.current_url.rstrip("/") == LoginPage.URL.rstrip("/")
