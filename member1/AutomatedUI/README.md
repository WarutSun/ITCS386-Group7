# ST01 automated UI test — two live runs passed

## Actual status

Two complete live Selenium runs passed on 19 November 2026 at approximately 00:53–00:54 Bangkok: **2 passed in 75.26 seconds**. Run 1: product 1146, order 1147. Run 2: product 1148, order 1149. Both verified validation, back navigation, checkout, stock 10→9, and saved Completed status in staff and guest views.

Full log: `verification-20261119-005315.txt`. Terminal screenshot: `evidence/2-passed-terminal.jpg`. Per-run screenshots and result JSONs are in `evidence/run-1-20261119-005315-29eabd/` and `evidence/run-2-20261119-005356-951bc1/`.

This submission contains the successful evidence only. Earlier debugging attempts remain in the backup folder.

## Install and run on macOS

Open Terminal in this `AutomatedUI` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_st01.py
```

The runner asks for the Group 7 **browser login password** without displaying it. It is not the Shop API password. Chrome is the default; install Chrome before running. Selenium Manager obtains a matching driver when needed.

## Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:BROWSER = 'edge'
python run_st01.py
```

Use Chrome or Edge; the environment variable is `BROWSER=chrome` or `BROWSER=edge`. Set `SHOP_USERNAME` only if it differs from `itcs386-g07`. `SHOP_BASE_URL` defaults to the course HTTP shop URL. `HEADLESS=1` is optional; leave it unset while troubleshooting so you can see the browser.

Do not bypass browser security warnings in the test code or disable browser protections. If the browser displays a warning, handle it yourself only if appropriate for your course setup; if lab access remains blocked, report the blocker and use an instructor-approved working environment.

## What the test checks

1. Staff login and a freshly published simple product: THB 199, stock 10, no backorders.
2. Guest opens the staff-created product permalink and verifies name, price and stock.
3. One item in the cart, quantity 1 and THB 199.
4. Checkout followed by browser Back preserves the same cart.
5. Blank First name triggers validation and prevents order confirmation.
6. Corrected fictional data and COD create one order with matching product, email, quantity and total.
7. Staff sees Processing and the same order information; remaining stock is 9.
8. Staff saves Completed, reopens the order to verify persistence, and the guest refreshes to see Order completed with unchanged details.

The manual report documents the original guest run and separately dated follow-ups. The automation repeats the same guest flow with unique timestamp/UUID data, separate staff/guest browsers, explicit waits and page-result assertions. It never edits another group's data. Two complete passes, not successful collection alone, are required to claim repeatability.

## Evidence and presentation commands

```bash
# Check imports and collect both cases without contacting the lab:
python run_st01.py --collect-only

# Full two-run verification:
python run_st01.py

# One full scenario for a short live demonstration:
python run_st01.py -k run-1
```

Screenshots and a result JSON are saved in `evidence/run-<repeat>-<unique-id>/`. The complete output is saved in `run-logs/`. A failed attempt also captures the current browser pages. Keep failures and fixes documented; do not describe a missing/blocked run as a pass.

The suite leaves its G07 products/orders in place for evidence; it does not delete them. Coordinate functional runs with the group. This is not a load test.

## Integration with Member 3's runner

Copy `member1/` beside the existing `member3/` and `member4/` folders. Member 3's supplied runner already looks for `member1/AutomatedUI`. Use their shared credential environment variables for the combined suite. Their ST02 code currently uses Edge directly, so `BROWSER=chrome` does not change ST02; that is for the owner to resolve if the combined suite is run on macOS.
