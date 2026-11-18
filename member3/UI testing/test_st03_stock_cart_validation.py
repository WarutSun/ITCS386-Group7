"""UI automation of manual case ST03 (stock and cart validation).
Step numbers in comments match ../System testing/ST03_stock_and_cart_validation.md.
Run:  pytest test_st03_stock_cart_validation.py -v

test_st03_stock_and_cart_validation  : the full scenario, must pass on every run.
test_st03_defect_*                   : known defects ST03-D01/D02, marked xfail(strict=True).
                                        They report XFAIL while the defect exists and turn
                                        into a failure (XPASS) once the shop is fixed.
"""
import re
import sys
from datetime import datetime

import pytest
from selenium.common.exceptions import (ElementClickInterceptedException, StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

import locators as L
from ui_common import BASE, STAFF_PASSWORD, STAFF_USER, make_driver, open_page

STOCK = 5
PRICE = 199
VALID_QTY = 2


# ---------------- helpers ----------------
def click(el):
    """Scroll the element to the middle of the window, then click. The fixed WordPress
    toolbar (and sticky headers) can cover an element at the top edge; if something still
    covers it, fall back to a JavaScript click on the same element."""
    drv = el.parent
    drv.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
    try:
        el.click()
    except ElementClickInterceptedException:
        drv.execute_script("arguments[0].click();", el)


def money(text):
    """'฿398.00' -> 398.0"""
    m = re.search(r"[\d,]+(?:\.\d+)?", text.replace("\xa0", " "))
    return float(m.group(0).replace(",", ""))


def js_select(drv, locator, value):
    """Set a <select> that wp-admin wraps with select2, and fire the jQuery change event."""
    el = drv.find_element(*locator)
    drv.execute_script(
        "arguments[0].value = arguments[1];"
        "if (window.jQuery) { jQuery(arguments[0]).trigger('change'); }"
        "else { arguments[0].dispatchEvent(new Event('change', {bubbles: true})); }", el, value)


def cart_quantities(drv, wait):
    """Open the block cart and return the quantity of every line ([] for an empty cart).
    The block cart puts both the 'filled' and the 'empty' layouts in the page and shows one
    after its JavaScript loads the cart, so wait for a *visible* line or a *visible* empty
    message instead of just checking that the elements exist."""
    drv.get(f"{BASE}/cart/")

    def loaded(d):
        lines = [e for e in d.find_elements(*L.CART_QTY_INPUT) if e.is_displayed()]
        if lines:
            return ("filled", lines)
        if any(e.is_displayed() for e in d.find_elements(*L.CART_EMPTY)):
            return ("empty", [])
        return False
    state, lines = WebDriverWait(drv, 30, ignored_exceptions=(StaleElementReferenceException,)).until(loaded)
    if state == "empty":  # make sure the empty layout is final and items do not arrive a moment later
        try:
            state, lines = WebDriverWait(drv, 4, ignored_exceptions=(StaleElementReferenceException,)).until(
                lambda d: loaded(d) if loaded(d) and loaded(d)[0] == "filled" else False)
        except TimeoutException:
            return []
    return [int(e.get_attribute("value")) for e in lines]


def cart_total(drv):
    return money(drv.find_element(*L.CART_TOTAL).text)


def set_cart_qty(drv, wait, qty):
    """Block cart has no Update button: type the number, leave the field, the cart updates itself."""
    el = wait(drv).until(EC.visibility_of_element_located(L.CART_QTY_INPUT))
    select_all = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
    el.send_keys(select_all, "a")
    el.send_keys(str(qty), Keys.TAB)


def type_qty(drv, wait, product_url, text):
    """Open the product page and type text into the quantity field like a user."""
    drv.get(product_url)
    q = wait(drv).until(EC.visibility_of_element_located(L.QTY_INPUT))
    q.clear()
    q.send_keys(text)
    return q


def browser_message(drv, el):
    """HTML5 validation of the quantity field: '' when the value is accepted."""
    drv.execute_script("arguments[0].checkValidity();", el)
    return el.get_property("validationMessage")


def submit_without_browser_limits(drv, wait, product_url, value):
    """Send the add-to-cart form with min/max removed, to see what the server does."""
    drv.get(product_url)
    q = wait(drv).until(EC.visibility_of_element_located(L.QTY_INPUT))
    drv.execute_script("arguments[0].removeAttribute('min'); arguments[0].removeAttribute('max');"
                       "arguments[0].value = arguments[1];", q, value)
    btn = drv.find_element(*L.ADD_TO_CART)
    click(btn)
    wait(drv).until(EC.staleness_of(btn))  # wait for the page reload after the POST


def notice_text(drv, wait):
    return wait(drv).until(EC.visibility_of_element_located(L.NOTICE)).text


def staff_login(drv, wait):
    print("Opening wp-admin. If the browser shows an http warning page, click Continue in that window.")
    open_page(drv, f"{BASE}/wp-admin/",
              lambda d: d.find_elements(*L.LOGIN_USER) or d.find_elements(By.ID, "wpadminbar"))
    if drv.find_elements(*L.LOGIN_USER):
        wait(drv).until(EC.visibility_of_element_located(L.LOGIN_USER)).send_keys(STAFF_USER)
        drv.find_element(*L.LOGIN_PASS).send_keys(STAFF_PASSWORD)
        click(drv.find_element(*L.LOGIN_SUBMIT))
        wait(drv, 60).until(lambda d: d.find_elements(By.ID, "wpadminbar") or d.find_elements(By.ID, "login_error"))
    assert not drv.find_elements(By.ID, "login_error"), "WordPress rejected the login: check SHOP_PASSWORD"
    assert "/wp-admin" in drv.current_url, f"unexpected page after login: {drv.current_url}"


def staff_create_product(drv, wait, name, stock=STOCK):
    """Staff creates a published simple product with managed stock. Returns (id, permalink)."""
    drv.get(f"{BASE}/wp-admin/post-new.php?post_type=product")
    wait(drv).until(EC.visibility_of_element_located(L.PRODUCT_TITLE)).send_keys(name)
    drv.find_element(*L.PRODUCT_PRICE).send_keys(str(PRICE))
    click(drv.find_element(*L.INVENTORY_TAB))
    box = wait(drv).until(EC.element_to_be_clickable(L.MANAGE_STOCK))
    if not box.is_selected():
        click(box)
    qty = wait(drv).until(EC.visibility_of_element_located(L.STOCK_QTY))
    qty.clear()
    qty.send_keys(str(stock))
    click(drv.find_element(*L.PUBLISH))
    # The shared server can be slow: wait (up to 90 s) for WordPress to land on the saved
    # product's edit page (post.php?post=<id>) and show its "Product published" notice.
    WebDriverWait(drv, 90, ignored_exceptions=(StaleElementReferenceException,)).until(
        lambda d: re.search(r"post\.php\?post=\d+", d.current_url)
        and any(n.is_displayed() and "published" in n.text.lower()
                for n in d.find_elements(*L.PRODUCT_PUBLISHED_NOTICE)))
    m = re.search(r"post=(\d+)", drv.current_url)
    assert m, f"could not read product id from {drv.current_url}"
    link = drv.execute_script("var a=document.querySelector('#sample-permalink a'); return a ? a.href : null;")
    return int(m.group(1)), link


def staff_stock(drv, wait, product_id):
    drv.get(f"{BASE}/wp-admin/post.php?post={product_id}&action=edit")
    click(wait(drv).until(EC.element_to_be_clickable(L.INVENTORY_TAB)))
    return int(wait(drv).until(EC.visibility_of_element_located(L.STOCK_QTY)).get_attribute("value"))


def open_admin_order(drv, wait, order_id):
    """HPOS order screen (used by this shop), legacy URL as a fallback."""
    drv.get(f"{BASE}/wp-admin/admin.php?page=wc-orders&action=edit&id={order_id}")
    try:
        wait(drv, 10).until(EC.presence_of_element_located(L.ORDER_STATUS_SELECT))
    except TimeoutException:
        drv.get(f"{BASE}/wp-admin/post.php?post={order_id}&action=edit")
        wait(drv).until(EC.presence_of_element_located(L.ORDER_STATUS_SELECT))


def confirmation_summary(drv):
    """{'Order #:': '780', 'Total:': '฿398.00', 'Payment:': 'Cash on delivery', ...}"""
    out = {}
    for item in drv.find_elements(*L.CONFIRM_SUMMARY_ITEMS):
        out[item.find_element(*L.CONFIRM_SUMMARY_KEY).text.strip()] = \
            item.find_element(*L.CONFIRM_SUMMARY_VALUE).text.strip()
    return out


# ---------------- main scenario ----------------
def test_st03_stock_and_cart_validation(staff_driver, customer_driver, wait, shot, run_id):
    """Goal: quantities above stock, zero and negative never reach the cart; a corrected
    quantity of 2 is bought with COD; staff sees the order, stock goes from 5 to 3,
    the order is completed and the customer sees "Order completed"."""
    staff, cust = staff_driver, customer_driver
    name = f"G07 Stock Test {run_id}"
    email = f"g07.st03.{run_id}@example.com"

    # Steps 1-2: staff creates the product with stock 5
    staff_login(staff, wait)
    product_id, _ = staff_create_product(staff, wait, name)
    shot(staff, "s02_product_created")

    # Steps 3-4: guest searches; one match redirects straight to the product page
    open_page(cust, f"{BASE}/?s={name.replace(' ', '+')}&post_type=product",
              lambda d: "/product/" in d.current_url or d.find_elements(*L.SEARCH_RESULT_LINK))
    if "/product/" not in cust.current_url:
        click(cust.find_element(*L.SEARCH_RESULT_LINK))
    assert name in wait(cust).until(EC.visibility_of_element_located(L.PRODUCT_PAGE_TITLE)).text
    assert money(cust.find_element(*L.PRODUCT_PAGE_PRICE).text) == PRICE
    assert cust.find_element(*L.PRODUCT_PAGE_STOCK).text.strip() == f"{STOCK} in stock"
    product_url = cust.current_url
    shot(cust, "s04_product_page")

    # Steps 5-7 (browser level): the field refuses 6, 0 and -1, so nothing is sent
    for qty, word in [("6", "less than or equal to 5"), ("0", "greater than or equal to 1"),
                      ("-1", "greater than or equal to 1")]:
        q = type_qty(cust, wait, product_url, qty)
        click(cust.find_element(*L.ADD_TO_CART))
        assert word in browser_message(cust, q), f"browser accepted quantity {qty}"
        shot(cust, f"s05_07_browser_blocks_{qty}")
    assert cart_quantities(cust, wait) == []

    # Step 5 (server level): 6 sent without browser limits is rejected with a stock message
    submit_without_browser_limits(cust, wait, product_url, "6")
    assert "not enough stock (5 remaining)" in notice_text(cust, wait)
    shot(cust, "s05_server_rejects_6")
    # Step 7 (server level): -1 adds nothing
    submit_without_browser_limits(cust, wait, product_url, "-1")
    assert cart_quantities(cust, wait) == []

    # Step 9: valid quantity 2
    q = type_qty(cust, wait, product_url, str(VALID_QTY))
    click(cust.find_element(*L.ADD_TO_CART))
    assert "have been added to your cart" in notice_text(cust, wait)
    assert cart_quantities(cust, wait) == [VALID_QTY]
    assert cart_total(cust) == PRICE * VALID_QTY
    shot(cust, "s09_cart_2")

    # Step 10: 6 in the cart is capped at the stock (5), never above
    set_cart_qty(cust, wait, 6)
    wait(cust).until(lambda d: cart_total(d) == PRICE * STOCK)
    assert cart_quantities(cust, wait) == [STOCK]
    shot(cust, "s10_cart_capped_5")

    # Step 11: correct the cart back to 2
    set_cart_qty(cust, wait, VALID_QTY)
    wait(cust).until(lambda d: cart_total(d) == PRICE * VALID_QTY)
    assert cart_quantities(cust, wait) == [VALID_QTY]
    shot(cust, "s11_cart_corrected")

    # Step 12: checkout with cash on delivery, fictional data
    cust.get(f"{BASE}/checkout/")
    em = wait(cust).until(EC.visibility_of_element_located(L.EMAIL))
    em.clear()
    em.send_keys(email)
    fields = {"first_name": "Test", "last_name": "G07", "address_1": "1 Test Road",
              "city": "Bangkok", "postcode": "10200", "phone": "0800000000"}
    for key, value in fields.items():
        el = wait(cust).until(EC.visibility_of_element_located(L.BILLING[key]))
        el.clear()
        el.send_keys(value)
    Select(cust.find_element(*L.BILLING_STATE)).select_by_value("TH-10")
    cod = wait(cust).until(EC.presence_of_element_located(L.PAYMENT_COD))
    cust.execute_script("arguments[0].click();", cod)
    shot(cust, "s12_checkout_filled")
    click(wait(cust).until(EC.element_to_be_clickable(L.PLACE_ORDER)))
    wait(cust, 30).until(EC.url_contains("/order-received/"))
    assert "Order received" in wait(cust).until(EC.visibility_of_element_located(L.CONFIRM_STATUS)).text
    summary = confirmation_summary(cust)
    order_no = summary["Order #:"]
    assert money(summary["Total:"]) == PRICE * VALID_QTY
    assert summary["Payment:"] == "Cash on delivery"
    assert summary["Email:"] == email
    rows = cust.find_elements(*L.CONFIRM_PRODUCT_ROWS)
    assert len(rows) == 1 and name in rows[0].text and f"× {VALID_QTY}" in rows[0].text
    shot(cust, "s12_order_received")

    # Step 13: staff sees the order
    open_admin_order(staff, wait, order_no)
    items = staff.find_elements(*L.ORDER_ITEM_ROWS)
    assert len(items) == 1 and name in items[0].text and f"× {VALID_QTY}" in items[0].text
    assert email in staff.page_source
    shot(staff, "s13_admin_order")

    # Step 14: remaining stock 5 - 2 = 3
    assert staff_stock(staff, wait, product_id) == STOCK - VALID_QTY
    shot(staff, "s14_stock_3")

    # Step 15: staff marks the order Completed
    open_admin_order(staff, wait, order_no)
    js_select(staff, L.ORDER_STATUS_SELECT, "wc-completed")
    save = staff.find_element(*L.ORDER_SAVE)
    click(save)
    wait(staff).until(EC.staleness_of(save))
    assert "Order updated" in wait(staff).until(EC.visibility_of_element_located(L.PRODUCT_PUBLISHED_NOTICE)).text
    assert Select(staff.find_element(*L.ORDER_STATUS_SELECT)).first_selected_option \
        .get_attribute("value") == "wc-completed"
    shot(staff, "s15_order_completed")

    # Step 16: the customer's confirmation now says the order is completed
    cust.refresh()
    assert "Order completed" in wait(cust).until(EC.visibility_of_element_located(L.CONFIRM_STATUS)).text
    assert money(confirmation_summary(cust)["Total:"]) == PRICE * VALID_QTY
    shot(cust, "s16_customer_completed")


# ---------------- known defects ----------------
@pytest.fixture(scope="module")
def defect_product_url():
    """One G07 product shared by the two defect checks (they only add to a guest cart)."""
    drv = make_driver()
    wait = lambda d, t=30: WebDriverWait(d, t)  # noqa: E731
    try:
        staff_login(drv, wait)
        run = datetime.now().strftime("%Y%m%d-%H%M%S")
        _, link = staff_create_product(drv, wait, f"G07 Stock Defect {run}")
    except AssertionError as exc:  # a setup problem is not the defect: report it as an error
        raise RuntimeError(f"setup failed: {exc}") from exc
    finally:
        drv.quit()
    return link


@pytest.mark.xfail(strict=True, raises=AssertionError, reason="Defect ST03-D01: server adds quantity 0 as 1 item")
def test_st03_defect_d01_zero_quantity_rejected_by_server(customer_driver, wait, shot, defect_product_url):
    """Goal: quantity 0 sent without the browser check must not put anything in the cart."""
    submit_without_browser_limits(customer_driver, wait, defect_product_url, "0")
    shot(customer_driver, "d01_after_submit")
    assert cart_quantities(customer_driver, wait) == []


@pytest.mark.xfail(strict=True, raises=AssertionError, reason="Defect ST03-D02: text quantity is added as 1 item")
def test_st03_defect_d02_text_quantity_rejected(customer_driver, wait, shot, defect_product_url):
    """Goal: typing 'abc' as the quantity must show a validation message and add nothing."""
    q = type_qty(customer_driver, wait, defect_product_url, "abc")
    assert q.get_attribute("value") == ""  # a number field cannot hold text
    btn = customer_driver.find_element(*L.ADD_TO_CART)
    click(btn)
    try:  # if the browser blocked the submit there is no reload; that is the fixed behaviour
        wait(customer_driver, 5).until(EC.staleness_of(btn))
    except TimeoutException:
        pass
    shot(customer_driver, "d02_after_submit")
    assert cart_quantities(customer_driver, wait) == []
