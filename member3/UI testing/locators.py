"""All page locators in one place. If the shop theme or WooCommerce version differs,
fix them here only. Verify each one once in the browser DevTools before the first run.
All locators were checked on the live shop during the manual run of ST03 on 17 Nov 2026:
classic product editor, HPOS order screen, block cart, block checkout and block order confirmation."""
from selenium.webdriver.common.by import By

# --- staff (wp-admin) ---
LOGIN_USER = (By.ID, "user_login")
LOGIN_PASS = (By.ID, "user_pass")
LOGIN_SUBMIT = (By.ID, "wp-submit")
PRODUCT_TITLE = (By.ID, "title")
PRODUCT_PRICE = (By.ID, "_regular_price")
INVENTORY_TAB = (By.CSS_SELECTOR, ".inventory_options a")
MANAGE_STOCK = (By.ID, "_manage_stock")
STOCK_QTY = (By.ID, "_stock")
PUBLISH = (By.ID, "publish")
PRODUCT_PUBLISHED_NOTICE = (By.CSS_SELECTOR, "#message.updated, .notice-success")
ORDER_STATUS_SELECT = (By.ID, "order_status")
ORDER_SAVE = (By.CSS_SELECTOR, "button.save_order, input.save_order")
ORDER_ITEM_ROWS = (By.CSS_SELECTOR, "#order_line_items tr.item")

# --- customer (storefront) --- verified on the live shop (17 Nov 2026)
# product page (classic add-to-cart form inside a block theme)
PRODUCT_PAGE_TITLE = (By.CSS_SELECTOR, "h1.wp-block-post-title")
PRODUCT_PAGE_PRICE = (By.CSS_SELECTOR, ".wp-block-woocommerce-product-price")  # first match = this product
PRODUCT_PAGE_STOCK = (By.CSS_SELECTOR, "p.stock")  # e.g. "5 in stock"
QTY_INPUT = (By.CSS_SELECTOR, "form.cart input.qty")  # type=number, dynamic id, name=quantity
ADD_TO_CART = (By.CSS_SELECTOR, "form.cart button.single_add_to_cart_button")
# search with a single match redirects straight to /shop/product/<slug>/; several matches show a list
SEARCH_RESULT_LINK = (By.CSS_SELECTOR, "li.product a, .wc-block-product a")
NOTICE = (By.CSS_SELECTOR, ".woocommerce-error, .woocommerce-message, .woocommerce-info, "
                           ".wc-block-components-notice-banner")
# block cart: NO "Update cart" button, quantity changes apply automatically
CART_EMPTY = (By.CSS_SELECTOR, ".wp-block-woocommerce-empty-cart-block")
CART_LINES = (By.CSS_SELECTOR, ".wc-block-cart-items__row")
CART_QTY_INPUT = (By.CSS_SELECTOR, ".wc-block-components-quantity-selector__input")
CART_TOTAL = (By.CSS_SELECTOR, ".wc-block-components-totals-footer-item .wc-block-formatted-money-amount")
CHECKOUT_BTN = (By.CSS_SELECTOR, "a.wc-block-cart__submit-button")
# block checkout
EMAIL = (By.ID, "email")
BILLING = {
    "first_name": (By.ID, "billing-first_name"),
    "last_name": (By.ID, "billing-last_name"),
    "address_1": (By.ID, "billing-address_1"),
    "city": (By.ID, "billing-city"),
    "postcode": (By.ID, "billing-postcode"),
    "phone": (By.ID, "billing-phone"),
}
BILLING_STATE = (By.ID, "billing-state")  # real <select>, use Select(...).select_by_value("TH-10")
PAYMENT_COD = (By.ID, "radio-control-wc-payment-method-options-cod")
PLACE_ORDER = (By.CSS_SELECTOR, "button.wc-block-components-checkout-place-order-button")
# block order confirmation page
CONFIRM_STATUS = (By.CSS_SELECTOR, ".wc-block-order-confirmation-status")  # "Order received" / "Order completed"
CONFIRM_SUMMARY_ITEMS = (By.CSS_SELECTOR, ".wc-block-order-confirmation-summary-list-item")
CONFIRM_SUMMARY_KEY = (By.CSS_SELECTOR, ".wc-block-order-confirmation-summary-list-item__key")
CONFIRM_SUMMARY_VALUE = (By.CSS_SELECTOR, ".wc-block-order-confirmation-summary-list-item__value")
CONFIRM_PRODUCT_ROWS = (By.CSS_SELECTOR, "tr.order_item")
