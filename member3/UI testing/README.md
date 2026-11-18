# UI testing (Group 7, Member 3)

Selenium WebDriver + pytest tests for the WooCommerce shop at http://157.85.102.236/shop/.
`conftest.py` and `locators.py` are shared so ST01 (Member 1) and ST02 (Member 4) can add
`test_st01_*.py` and `test_st02_*.py` next to ST03 and the whole suite runs with one command.

## Run (Windows PowerShell, same setup as member4/AutomatedUI)
```powershell
py -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt     # Microsoft Edge is used by default
$env:SHOP_USERNAME = 'itcs386-g07'
$env:SHOP_PASSWORD = '<row 07, "Password (shop + hotel)">'   # browser login, never commit it
python -m pytest -v -rA "member3/UI testing"   # ST03 only, from the repo root
python member3/run_ui_suite.py                 # whole UI suite: ST01 + ST02 + ST03
```
Optional: `$env:BROWSER = 'chrome'`, `$env:HEADLESS = '1'`. macOS/Linux: `export SHOP_PASSWORD=...`.

ST03 alone should end with `1 passed, 2 xfailed`.
- `test_st03_stock_and_cart_validation` is the full ST03 scenario (16 manual steps) and must pass on every run.
- The two `xfail` tests are the known defects ST03-D01 and ST03-D02 (see the manual case). They are
  `strict`, so if the shop gets fixed they show up as failures and the defect report should be closed.

## Team UI suite (Member 3 integration task)
`member3/run_ui_suite.py` collects every scenario folder (`member1/AutomatedUI`, `member4/AutomatedUI`,
`member3/UI testing`) into one pytest run, skips a folder that is not pushed yet and saves the full
output to `member3/ui-suite-<date-time>.txt`. Agreed common setup:
- Selenium + pytest, Microsoft Edge by default, env vars `SHOP_USERNAME` / `SHOP_PASSWORD` / `SHOP_BASE_URL` / `HEADLESS`.
- Test file names must be unique across folders (`test_st01_*.py`, `test_coupon_checkout.py`, `test_st03_*.py`).
- Each test creates its own G07 data with a date-time suffix, so the suite can be run again at any time.
- Each owner fixes their own test; the integrator reports the failing step and the evidence.

## Rules for every scenario owner
- One file per manual case: `test_stNN_<topic>.py`, a goal docstring on each test.
- In this folder: fixtures in `conftest.py` (`run_id`, `staff_driver`, `customer_driver`, `wait`, `shot`), settings in `ui_common.py`.
- Put locators in `locators.py`. All were checked on the live shop on 17 Nov 2026
  (classic product editor, HPOS order screen, block cart/checkout/confirmation).
- Put `run_id` into every product name, coupon code and email (`G07 ... 20261119-140212`), so
  a second run never collides with the first.
- Assert what the page shows, use explicit waits (no `sleep`).
- Block cart notes: there is no "Update cart" button (type the number and leave the field);
  quantities above stock are capped silently.

## What ST03 shows
Staff creates `G07 Stock Test <run_id>` with stock 5. A guest is blocked by the browser at 6, 0 and -1,
the server rejects 6 with "not enough stock (5 remaining)" and ignores -1. A valid 2 goes in the cart,
6 in the cart is capped at 5, it is corrected to 2 and bought with cash on delivery (total 398 THB).
Staff sees the order, stock 3, marks it Completed, and the customer page then shows "Order completed".

## Evidence
`evidence/<run_id>/` gets one screenshot per checkpoint from `shot(...)`, so two runs stay in separate folders.
Run log (fill after each run, two runs with fresh data are required):

| Date/time (UTC+7) | Run | Result | Evidence |
|---|---|---|---|
| 18 Nov 2026 19:44 | 1 | `1 passed, 2 xfailed` in 68.6 s: full ST03 scenario passed, defects D01/D02 confirmed | run-logs/run1_20261118.txt, evidence/20261118-194456, -194550, -194557 |
| 18 Nov 2026 19:46 | 2 (fresh data) | Main scenario **passed** again with new data. The two defect tests stopped in setup: "Product published" did not appear within 30 s on the shared server. | run-logs/run2_20261118.txt, evidence/20261118-194640 |
| 18 Nov 2026 19:49 | 3 (fresh data, publish wait raised to 90 s) | `1 passed, 2 xfailed` in 68.9 s | run-logs/run3_20261118.txt, evidence/20261118-194956, -195051, -195057 |

Failure analysis, run 2: a test mistake (the wait was too short for the shared server), not a defect in the shop.
The two XFAIL results in runs 1 and 3 are the known system defects ST03-D01 and ST03-D02 (see `../System testing/ST03_stock_and_cart_validation.md`).
Each run created its own product `G07 Stock Test <run_id>`, guest email `g07.st03.<run_id>@example.com` and one COD order, so no run reused another run's data.
