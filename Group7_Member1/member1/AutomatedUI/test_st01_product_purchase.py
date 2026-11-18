"""ST01: staff setup, guest purchase, validation, back navigation, completion.

Two parameterized runs create fresh G07 products and one COD order each.
Uses the team's observed classic product editor and WooCommerce Block locators.
"""
import json
import os
import re
import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from urllib.parse import quote_plus, urlparse
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

BASE = os.getenv("SHOP_BASE_URL", "http://157.85.102.236/shop").rstrip("/")
HERE = Path(__file__).resolve().parent
WAIT = 30


def visible(driver, selector):
    return WebDriverWait(driver, WAIT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))


def click(driver, selector):
    element = WebDriverWait(driver, WAIT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    element.click()


def fill(driver, selector, value):
    element = visible(driver, selector)
    element.click()
    element.send_keys(Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL, "a")
    element.send_keys(Keys.BACKSPACE)
    if value:
        element.send_keys(value)
    element.send_keys(Keys.TAB)
    assert element.get_attribute("value") == value


def money(text):
    match = re.search(r"\d[\d,]*(?:\.\d+)?", text)
    assert match, f"No amount in {text!r}"
    return Decimal(match.group().replace(",", ""))


def make_driver():
    browser = os.getenv("BROWSER", "chrome")
    assert browser in ("chrome", "edge"), "BROWSER must be chrome or edge"
    options = webdriver.ChromeOptions() if browser == "chrome" else webdriver.EdgeOptions()
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1100")
    driver = (webdriver.Chrome if browser == "chrome" else webdriver.Edge)(options=options)
    driver.set_page_load_timeout(45)
    return driver


def cart_assertions(driver, name):
    visible(driver, ".wc-block-cart-items__row")
    rows = driver.find_elements(By.CSS_SELECTOR, ".wc-block-cart-items__row")
    assert len(rows) == 1 and name in rows[0].text
    assert rows[0].find_element(By.CSS_SELECTOR, "input[type=number]").get_attribute("value") == "1"
    assert money(visible(driver, ".wc-block-components-totals-footer-item .wc-block-formatted-money-amount").text) == Decimal("199")


def confirmation(driver, name, email, order_id=None, completed=False):
    status = visible(driver, ".wc-block-order-confirmation-status").text
    assert ("Order completed" if completed else "Order received") in status
    values = {}
    for item in driver.find_elements(By.CSS_SELECTOR, ".wc-block-order-confirmation-summary-list-item"):
        key = item.find_element(By.CSS_SELECTOR, ".wc-block-order-confirmation-summary-list-item__key").text.strip()
        values[key] = item.find_element(By.CSS_SELECTOR, ".wc-block-order-confirmation-summary-list-item__value").text.strip()
    assert money(values["Total:"]) == Decimal("199")
    assert values["Email:"] == email
    assert values["Payment:"] == "Cash on delivery"
    if order_id:
        assert values["Order #:"] == order_id
    rows = driver.find_elements(By.CSS_SELECTOR, "tr.order_item")
    assert len(rows) == 1 and name in rows[0].text and "× 1" in rows[0].text
    return values["Order #:"]


# Goal: repeat the complete manual ST01 guest scenario, including a blocked blank
# first name and back navigation, then verify saved completion on both sides.
@pytest.mark.parametrize("repeat", [1, 2], ids=["run-1", "run-2"])
def test_st01_product_purchase(repeat):
    password = os.getenv("SHOP_PASSWORD")
    assert password, "Set SHOP_PASSWORD to the Group 7 browser password (not API password)"
    started = datetime.now(ZoneInfo("Asia/Bangkok"))
    run_id = started.strftime("%Y%m%d-%H%M%S") + "-" + uuid4().hex[:6]
    name = f"G07_ST01_TestMug_{run_id}"
    email = f"g07.st01.{run_id}@example.com"
    folder = HERE / "evidence" / f"run-{repeat}-{run_id}"
    folder.mkdir(parents=True)
    result = {"run_id": run_id, "started_bangkok": started.isoformat(), "repeat": repeat,
              "product_name": name, "email": email, "status": "RUNNING", "steps": []}
    drivers = []

    def shot(driver, label):
        assert driver.save_screenshot(str(folder / f"{label}.png"))
        result["steps"].append({"step": label, "status": "PASS",
                                "at_bangkok": datetime.now(ZoneInfo("Asia/Bangkok")).isoformat()})
        print(f"ST01 {repeat}: {label}", flush=True)

    try:
        staff = make_driver(); drivers.append(staff)
        guest = make_driver(); drivers.append(guest)
        staff.get(f"{BASE}/wp-admin/")
        fill(staff, "#user_login", os.getenv("SHOP_USERNAME", "itcs386-g07"))
        fill(staff, "#user_pass", password)
        click(staff, "#wp-submit")
        visible(staff, "#wpadminbar")
        assert "/wp-admin/" in staff.current_url
        shot(staff, "01-staff-login")

        staff.get(f"{BASE}/wp-admin/post-new.php?post_type=product")
        fill(staff, "#title", name)
        fill(staff, "#_regular_price", "199")
        click(staff, "a[href='#inventory_product_data']")
        if not visible(staff, "#_manage_stock").is_selected():
            click(staff, "#_manage_stock")
        fill(staff, "#_stock", "10")
        Select(visible(staff, "#_backorders")).select_by_value("no")
        click(staff, "#publish")
        WebDriverWait(staff, WAIT).until(lambda d: "Product published" in d.find_element(By.TAG_NAME, "body").text)
        product_id = re.search(r"post=(\d+)", staff.current_url).group(1)
        result["product_id"] = product_id
        click(staff, "a[href='#inventory_product_data']")
        assert visible(staff, "#_stock").get_attribute("value") == "10"
        shot(staff, "02-published-product-stock")

        guest.get(f"{BASE}/?s={quote_plus(name)}&post_type=product")
        WebDriverWait(guest, WAIT).until(lambda d: "/product/" in d.current_url or d.find_elements(By.PARTIAL_LINK_TEXT, name))
        if "/product/" not in guest.current_url:
            guest.find_element(By.PARTIAL_LINK_TEXT, name).click()
        assert name in visible(guest, "h1.wp-block-post-title").text
        assert money(visible(guest, ".wp-block-woocommerce-product-price").text) == Decimal("199")
        assert visible(guest, "p.stock").text == "10 in stock"
        shot(guest, "03-guest-product")
        click(guest, "form.cart button.single_add_to_cart_button")
        visible(guest, ".woocommerce-message, .wc-block-components-notice-banner")
        guest.get(f"{BASE}/cart/")
        cart_assertions(guest, name)
        shot(guest, "04-cart")
        click(guest, "a.wc-block-cart__submit-button")
        visible(guest, "#email")
        guest.back()
        cart_assertions(guest, name)
        shot(guest, "05-back-navigation-cart")
        click(guest, "a.wc-block-cart__submit-button")

        fill(guest, "#email", email)
        fields = {"first_name": "", "last_name": "TestCustomer", "address_1": "1 Test Road",
                  "city": "Bangkok", "postcode": "10200"}
        for field, value in fields.items():
            fill(guest, f"#billing-{field}", value)
        Select(visible(guest, "#billing-state")).select_by_value("TH-10")
        assert "Cash on delivery" in guest.find_element(By.TAG_NAME, "body").text
        click(guest, "button.wc-block-components-checkout-place-order-button")
        WebDriverWait(guest, WAIT).until(lambda d:
            d.find_element(By.ID, "billing-first_name").get_attribute("aria-invalid") == "true"
            or bool(d.find_element(By.ID, "billing-first_name").get_property("validationMessage"))
            or any(e.is_displayed() and "first name" in e.text.lower()
                   for e in d.find_elements(By.CSS_SELECTOR, ".wc-block-components-validation-error")))
        assert "/order-received/" not in guest.current_url
        assert visible(guest, "#billing-first_name").get_attribute("value") == ""
        shot(guest, "06-required-first-name-error")

        fill(guest, "#billing-first_name", "G07")
        assert money(visible(guest, ".wc-block-components-totals-footer-item .wc-block-formatted-money-amount").text) == Decimal("199")
        shot(guest, "07-corrected-checkout")
        click(guest, "button.wc-block-components-checkout-place-order-button")
        WebDriverWait(guest, WAIT).until(EC.url_contains("/order-received/"))
        order_id = confirmation(guest, name, email)
        result["order_id"] = order_id
        shot(guest, "08-order-confirmation")

        order_url = f"{BASE}/wp-admin/admin.php?page=wc-orders&action=edit&id={order_id}"
        staff.get(order_url)
        visible(staff, "#order_status")
        rows = staff.find_elements(By.CSS_SELECTOR, "#order_line_items tr.item")
        assert len(rows) == 1 and name in rows[0].text and "× 1" in rows[0].text
        assert email in staff.find_element(By.TAG_NAME, "body").text
        assert Select(staff.find_element(By.ID, "order_status")).first_selected_option.get_attribute("value") == "wc-processing"
        total_row = staff.find_element(By.XPATH, "//table[contains(@class,'wc-order-totals')]//tr[.//td[contains(normalize-space(),'Order Total')]]")
        assert money(total_row.find_element(By.CSS_SELECTOR, ".amount").text) == Decimal("199")
        shot(staff, "09-staff-processing")
        notes = [e.text for e in staff.find_elements(By.CSS_SELECTOR, ".order_notes li") if "failed to send" in e.text]
        result["mail_failure_notes"] = notes

        staff.get(f"{BASE}/wp-admin/post.php?post={product_id}&action=edit")
        click(staff, "a[href='#inventory_product_data']")
        assert visible(staff, "#_stock").get_attribute("value") == "9"
        shot(staff, "10-stock-nine")

        staff.get(order_url)
        selector = visible(staff, "#order_status")
        Select(selector).select_by_value("wc-completed")
        click(staff, "button[name='save']")
        WebDriverWait(staff, WAIT).until(lambda d: "Order updated" in d.find_element(By.TAG_NAME, "body").text)
        staff.get(order_url)
        assert Select(visible(staff, "#order_status")).first_selected_option.get_attribute("value") == "wc-completed"
        shot(staff, "11-staff-completed-saved")
        guest.refresh()
        confirmation(guest, name, email, order_id, completed=True)
        shot(guest, "12-guest-completed")
        result.update(status="PASS", total_thb="199.00", initial_stock=10, final_stock=9)
    except Exception as exc:
        result["status"] = "FAIL"
        # Do not write credentials, session URLs or order keys into exception logs.
        result["error_type"] = type(exc).__name__
        for i, driver in enumerate(drivers):
            try:
                driver.save_screenshot(str(folder / f"FAILED-browser-{i}.png"))
                result[f"failure_page_{i}"] = urlparse(driver.current_url).path
            except Exception:
                pass
        raise
    finally:
        result["finished_bangkok"] = datetime.now(ZoneInfo("Asia/Bangkok")).isoformat()
        (folder / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        for driver in drivers:
            driver.quit()
