# ST03: manual-to-UI mapping 

## Manual step to automated step

| Manual step | What the UI test does | Assertion on the page |
|---|---|---|
| 1-2 Staff creates product, stock 5 | `staff_login`, `staff_create_product` | publish notice shown, product id read from URL |
| 3-4 Customer searches, opens product | `?s=<name>`, follows redirect or first result | title contains name, price = 199 |
| 5-7 Quantity 6, 0, -1 | types each value, clicks Add to cart; then sends 6 and -1 without browser limits | browser validation message; server banner "not enough stock (5 remaining)"; cart empty |
| 6, 8 Zero (server) and `abc` | two `xfail(strict=True)` tests | document defects ST03-D01 and ST03-D02 |
| 9 Valid quantity 2 | `type_qty("2")` + Add to cart | cart = [2], total = 398 |
| 10 Raise to 6 in cart | `set_cart_qty(6)` | cart capped at 5, total 995 |
| 11 Correct to 2 | `set_cart_qty(2)` | cart = [2], total = 398 |
| 12 Checkout COD | fills block checkout, Place Order | order number shown, total 398, payment COD, 1 product line |
| 13 Staff opens order | `open_admin_order(order_no)` | 1 item with product name, customer email present |
| 14 Remaining stock | product edit page, Inventory tab | stock = 3 |
| 15 Mark Completed | order status = wc-completed, save | "Order updated", status Completed |
| 16 Customer view afterward | refresh confirmation | "Order completed", total 398 |

## Why it passes on a second run
Every run builds its data from `run_id` (date-time): product `G07 Stock Test 20261119-1402xx`, email `g07.st03.20261119-1402xx@example.com`. Nothing from run 1 is reused, so run 2 cannot collide.

## Talk outline (about 2 minutes)
1. (20 s) ST03 goal: stock and cart validation, staff to customer to staff. Unusual data: 6 above stock, 0, -1, text.
2. (30 s) Show this mapping table: each manual step has a matching automated step and a page assertion.
3. (50 s) Live run (expect `1 passed, 2 xfailed`): `python -m pytest -v "member3/UI testing"`. Point at the invalid-quantity steps and the confirmation total.
4. (10 s) Mention the two defects found (0 and text become 1 item) and that they are tracked as strict xfail.
5. (10 s) Show evidence of the second run: run log in README plus the `evidence/` screenshots with a different run_id.

Backup if the live run fails (shared server): play the recording of the earlier full run.
