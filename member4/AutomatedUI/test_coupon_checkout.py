"""ST02: staff creates a product/coupon; a shopper completes a discounted order."""

import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pytest
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


BASE = os.environ.get("SHOP_BASE_URL", "http://157.85.102.236/shop").rstrip("/")
ADMIN = f"{BASE}/wp-admin"
WAIT_SECONDS = 30
PRICE = "200"
DISCOUNT = "20"
TOTAL = "180"
APPLY_BUTTON = (By.XPATH,
    "//button[normalize-space(.)='Apply'] | //*[@role='button' and normalize-space(.)='Apply']")


def ready(driver, locator):
    return WebDriverWait(driver, WAIT_SECONDS).until(
        EC.element_to_be_clickable(locator)
    )


def visible(driver, locator):
    return WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located(locator)
    )


def page_contains(driver, value):
    WebDriverWait(driver, WAIT_SECONDS, ignored_exceptions=(StaleElementReferenceException,)).until(
        lambda d: value in d.find_element(By.TAG_NAME, "body").text
    )


def fill(driver, locator, value):
    element = ready(driver, locator)
    # WooCommerce Blocks keeps prefilled values in React state; .clear() can
    # leave that state unchanged and append the new value on the next keystroke.
    element.click()
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(Keys.BACKSPACE)
    element.send_keys(value)
    assert element.get_attribute("value") == value, (
        f"Field {locator} contains {element.get_attribute('value')!r}, expected {value!r}"
    )


def click_centered(driver, locator):
    """Avoid the fixed WordPress toolbar covering a scrolled-to button."""
    element = ready(driver, locator)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    ready(driver, locator).click()


def photo(driver, folder, name):
    folder.mkdir(parents=True, exist_ok=True)
    assert driver.save_screenshot(str(folder / f"{name}.png"))


def login(driver):
    username = os.environ["SHOP_USERNAME"]
    password = os.environ["SHOP_PASSWORD"]  # Browser login, not Shop API password.
    print("Opening Group 07 admin. If Edge shows an HTTP warning, handle it yourself in that window.")
    driver.get(f"{ADMIN}/")
    # A redirect can finish after the initial navigation. Inspect the page,
    # rather than assuming that a URL without wp-login.php means signed in.
    try:
        WebDriverWait(driver, 120).until(
            lambda d: d.find_elements(By.ID, "user_login")
            or d.find_elements(By.ID, "wpadminbar")
        )
    except TimeoutException as exc:
        raise AssertionError(
            "No WordPress login form or admin toolbar appeared. Check the Edge window for an HTTP warning or another blocking page."
        ) from exc
    if driver.find_elements(By.ID, "user_login"):
        fill(driver, (By.ID, "user_login"), username)
        fill(driver, (By.ID, "user_pass"), password)
        ready(driver, (By.ID, "wp-submit")).click()
    WebDriverWait(driver, WAIT_SECONDS).until(
        lambda d: d.find_elements(By.ID, "wpadminbar")
        or d.find_elements(By.ID, "login_error")
    )
    if driver.find_elements(By.ID, "login_error"):
        raise AssertionError("WordPress rejected the browser login; check SHOP_USERNAME and SHOP_PASSWORD.")
    assert "wp-admin" in driver.current_url, f"Unexpected page after login: {driver.current_url}"


def create_product(driver, name, sku):
    driver.get(f"{ADMIN}/post-new.php?post_type=product")
    fill(driver, (By.ID, "title"), name)
    fill(driver, (By.ID, "_regular_price"), PRICE)
    # Match the manual case's initial stock; use a distinct SKU each time.
    ready(driver, (By.CSS_SELECTOR, "a[href='#inventory_product_data']")).click()
    fill(driver, (By.ID, "_sku"), sku)
    stock_management = ready(driver, (By.ID, "_manage_stock"))
    if not stock_management.is_selected():
        stock_management.click()
    fill(driver, (By.ID, "_stock"), "20")
    click_centered(driver, (By.ID, "publish"))
    WebDriverWait(driver, WAIT_SECONDS).until(
        lambda d: "Product published" in d.find_element(By.TAG_NAME, "body").text
        or "Published" in d.find_element(By.ID, "post-status-display").text
    )
    permalink = visible(driver, (By.CSS_SELECTOR, "#sample-permalink a")).get_attribute("href")
    assert "/product/" in urlparse(permalink).path, permalink
    return permalink


def create_coupon(driver, code):
    driver.get(f"{ADMIN}/post-new.php?post_type=shop_coupon")
    fill(driver, (By.ID, "title"), code)
    Select(ready(driver, (By.ID, "discount_type"))).select_by_value("percent")
    fill(driver, (By.ID, "coupon_amount"), "10")
    click_centered(driver, (By.ID, "publish"))
    WebDriverWait(driver, WAIT_SECONDS).until(
        lambda d: "Published" in d.find_element(By.ID, "post-status-display").text
    )


def apply_coupon(driver, code):
    # The heading is an accordion toggle. Only open it when Apply is not visible.
    if not any(e.is_displayed() for e in driver.find_elements(*APPLY_BUTTON)):
        ready(driver, (By.XPATH, "//*[normalize-space()='Add coupons']")).click()
    # Apply is disabled until a code is entered, so only require visibility here.
    apply_button = visible(driver, APPLY_BUTTON)
    # Find the text input in Apply's nearest container, never the cart's quantity input.
    field = apply_button.find_element(
        By.XPATH, "./ancestor::*[.//input[not(@type='number')]][1]//input[not(@type='number')][1]"
    )
    assert field.is_displayed() and field.get_attribute("type") in ("text", "search"), (
        "Coupon field is missing; refusing to type into another cart field"
    )
    field.click()
    field.send_keys(Keys.CONTROL, "a")
    field.send_keys(Keys.BACKSPACE)
    WebDriverWait(driver, WAIT_SECONDS).until(lambda d: field.get_attribute("value") == "")
    field.send_keys(code)
    assert field.get_attribute("value") == code, (
        f"Coupon field contains unexpected value: {field.get_attribute('value')!r}"
    )
    ready(driver, APPLY_BUTTON).click()


def assert_money(driver, amount):
    # Assertion on rendered page text, not on a network response or a click.
    page_contains(driver, f"฿{amount}.00")


def checkout(driver, run_id):
    ready(driver, (By.LINK_TEXT, "Proceed to Checkout")).click()
    visible(driver, (By.CSS_SELECTOR, "form.wc-block-checkout__form, form[aria-label='Checkout']"))
    assert_money(driver, TOTAL)
    assert "Cash on delivery" in driver.find_element(By.TAG_NAME, "body").text
    fill(driver, (By.ID, "email"), f"g07.m4.{run_id}@example.com")
    fill(driver, (By.ID, "billing-first_name"), "G07")
    fill(driver, (By.ID, "billing-last_name"), "Systester")
    fill(driver, (By.ID, "billing-address_1"), "99 Test Road")
    fill(driver, (By.ID, "billing-city"), "Bangkok")
    Select(ready(driver, (By.ID, "billing-state"))).select_by_visible_text("Bangkok")
    fill(driver, (By.ID, "billing-postcode"), "10170")
    return f"g07.m4.{run_id}@example.com"


def get_order_id(driver):
    WebDriverWait(driver, WAIT_SECONDS).until(
        lambda d: re.search(r"/order-received/(\d+)/", d.current_url)
    )
    return re.search(r"/order-received/(\d+)/", driver.current_url).group(1)


def verify_staff_order(driver, order_id, name, code):
    driver.get(f"{ADMIN}/admin.php?page=wc-orders&action=edit&id={order_id}")
    page_contains(driver, f"Order #{order_id}")
    text = driver.find_element(By.TAG_NAME, "body").text.lower()
    assert name.lower() in text
    assert code.lower() in text
    assert "processing" in text
    assert "20.00" in text and "180.00" in text


def complete_staff_order(driver, order_id):
    Select(ready(driver, (By.ID, "order_status"))).select_by_value("wc-completed")
    ready(driver, (By.CSS_SELECTOR, "button[name='save']")).click()
    # Reopen the order so a selected but unsaved dropdown cannot pass the test.
    driver.get(f"{ADMIN}/admin.php?page=wc-orders&action=edit&id={order_id}")
    WebDriverWait(driver, WAIT_SECONDS).until(
        lambda d: Select(d.find_element(By.ID, "order_status")).first_selected_option.get_attribute("value")
        == "wc-completed"
    )


@pytest.mark.parametrize("repeat", [1, 2])
def test_st02_coupon_purchase(repeat):
    # Goal: the full ST02 staff-to-shopper flow passes twice with fresh data,
    # rejects an invalid coupon, and verifies totals and status on the page.
    run_id = datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex[:6]
    name = f"G07-M4-Coupon-Product-{run_id}"
    sku = f"G07-M4-{run_id}"
    code = f"G07M4SAVE{run_id}"
    invalid_code = f"G07M4INVALID{run_id}"
    folder = Path(__file__).resolve().parent / "evidence" / f"run-{repeat}-{run_id}"

    options = Options()
    if os.environ.get("HEADLESS") == "1":
        options.add_argument("--headless=new")
    driver = webdriver.Edge(options=options)
    driver.set_window_size(1440, 1000)
    try:
        login(driver)
        product_url = create_product(driver, name, sku)
        photo(driver, folder, "01-staff-product")
        create_coupon(driver, code)
        photo(driver, folder, "02-staff-coupon")

        driver.get(product_url)
        page_contains(driver, name)
        assert_money(driver, PRICE)
        ready(driver, (By.XPATH, "//button[normalize-space()='Add to cart']")).click()
        page_contains(driver, "has been added to your cart")
        ready(driver, (By.LINK_TEXT, "View cart")).click()
        WebDriverWait(driver, WAIT_SECONDS).until(
            lambda d: urlparse(d.current_url).path.rstrip("/").endswith("/cart")
        )
        page_contains(driver, name)
        assert_money(driver, PRICE)
        photo(driver, folder, "03-cart-before-coupon")

        apply_coupon(driver, invalid_code)
        WebDriverWait(driver, WAIT_SECONDS).until(
            lambda d: any(
                e.is_displayed() and ("coupon" in e.text.lower() or invalid_code.lower() in e.text.lower())
                for e in d.find_elements(By.CSS_SELECTOR, "[role='alert'], .wc-block-components-notice-banner")
            )
        )
        assert_money(driver, PRICE)
        photo(driver, folder, "04-invalid-coupon")

        # A failed WooCommerce Blocks submission can keep the old value in React state.
        # Reload to start the valid coupon check with an empty form.
        driver.refresh()
        page_contains(driver, name)
        assert_money(driver, PRICE)
        apply_coupon(driver, code)
        page_contains(driver, code.lower())
        assert_money(driver, TOTAL)
        assert "20.00" in driver.find_element(By.TAG_NAME, "body").text
        photo(driver, folder, "05-valid-coupon")

        checkout(driver, run_id)
        photo(driver, folder, "06-checkout")
        ready(driver, (By.XPATH, "//button[contains(normalize-space(), 'Place Order')]")).click()
        order_id = get_order_id(driver)
        page_contains(driver, "Thank you. Your order has been received.")
        assert_money(driver, TOTAL)
        photo(driver, folder, "07-confirmation")

        verify_staff_order(driver, order_id, name, code)
        photo(driver, folder, "08-staff-processing")
        complete_staff_order(driver, order_id)
        photo(driver, folder, "09-staff-completed")

        driver.get(f"{BASE}/my-account/orders/")
        row_locator = (By.XPATH, f"//tr[.//a[contains(normalize-space(), '#{order_id}')]]")
        visible(driver, row_locator)
        WebDriverWait(driver, WAIT_SECONDS).until(
            lambda d: "Completed" in d.find_element(*row_locator).text
            and "฿180.00" in d.find_element(*row_locator).text
        )
        photo(driver, folder, "10-customer-orders")
        (folder / "result.txt").write_text(
            f"ST02 repeat {repeat}: PASS\nOrder: #{order_id}\n"
            f"Product: {name}\nCoupon: {code}\nDiscount: THB 20\nTotal: THB 180\n",
            encoding="utf-8",
        )
    except Exception:
        try:
            print("Failure page path:", urlparse(driver.current_url).path)
            photo(driver, folder, "FAILED-current-page")
        except WebDriverException:
            # Keep the original exception when Edge is already closed.
            pass
        raise
    finally:
        try:
            driver.quit()
        except WebDriverException:
            pass
