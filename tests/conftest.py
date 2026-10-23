import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

DEMO_USERNAME = "standard_user"
DEMO_PASSWORD = "secret_sauce"


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Chạy Chrome ở chế độ không mở cửa sổ trình duyệt.",
    )


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    try:
        browser.set_page_load_timeout(30)
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(DEMO_USERNAME, DEMO_PASSWORD)
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    InventoryPage(driver)
    return driver
