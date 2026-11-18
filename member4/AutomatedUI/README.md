# ST02 automated UI test

This Selenium/pytest test follows the manual coupon-purchase case ST02. One command runs it twice, with a new Group 07 product, coupon, fictional email address and order per run. It asserts displayed prices, the invalid-coupon notice, the 10% discount, checkout confirmation, staff order status and customer order history. Screenshots and a short result file go to `evidence/run-*/` after each run. A failure also captures the current page.

## Run on Windows PowerShell

Use Python 3.10+ and Microsoft Edge. From this `ST02` folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:SHOP_USERNAME = 'itcs386-g07'
$env:SHOP_PASSWORD = '<Group 07 browser login password>'
python -m pytest -q -s test_coupon_checkout.py
```

Selenium Manager normally locates a matching browser driver. If its download is blocked, install the official matching Edge WebDriver and put it on `PATH`. The `SHOP_PASSWORD` variable is the **browser login password**, not the Shop API password. Never commit credentials or a `.env` file. Set `SHOP_BASE_URL` only if the instructor changes the shop URL. Optional: `$env:HEADLESS = '1'` for a headless run.

## Evidence and integration

- Move the resulting `evidence/run-*` folders into the group's `project phase 2/UI testing/ST02/` folder and commit the screenshots and a captured full pytest output (e.g. `python -m pytest -q -s test_coupon_checkout.py *> ui-run.txt`). Review images for contact details before sharing.
- Each run **publishes a product and coupon and places one COD order** on the shared course server. Coordinate with the team before executing. Do not run this as a performance test; it is a functional UI test.
- The test assumes the course's classic WordPress product/coupon editors and WooCommerce block cart/checkout. If a locator fails, inspect the visible element on the course site and update that locator. Do not replace explicit waits with fixed sleeps.
- Each test creates its own data and does not edit or remove demo data or other groups' records. The two parameterized attempts must both pass before reporting repeatability.
- The automated run is **not yet verified against the live site** in this handoff. Record actual results, failures, and any defect only after running it.
