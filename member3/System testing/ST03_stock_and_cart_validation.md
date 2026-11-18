# ST03: Stock and cart validation

| Field | Value |
|---|---|
| Test case ID | ST03 |
| Title | Stock and cart validation, from staff product setup to customer purchase and staff verification |
| Objective | Verify that the shop rejects an excessive quantity and invalid quantities (0, negative, non-numeric), accepts a corrected valid quantity, completes a purchase, and reduces stock by exactly the purchased quantity. Staff and customer must see consistent results. |
| Preconditions | 1. Shop reachable at http://157.85.102.236/shop/ <br> 2. Staff account `itcs386-g07` (Shop manager) can log in at /shop/wp-admin/ (password from the accounts sheet, never written here) <br> 3. Cash on delivery is the only payment method <br> 4. Customer acts as a guest (not logged in) |
| Test data | Product `G07 Stock Test 20261117-2208` (id 779), simple, regular price 199 THB, manage stock = yes, stock 5. Quantities: 6 (above stock), 0, -1, `abc`, then 2 (valid); in the cart: 6, then 2. Customer (fictional): Test G07, 1 Test Road, Bangkok, province Bangkok (TH-10), postcode 10200, phone 0800000000, email `g07.st03.20261117-2208@example.com`. |
| Tested by and date | `<Member 3 name>` with Claude (browser assistant) / 17 Nov 2026, 22:08-22:20 (UTC+7). Result: order #780 |

Two levels of validation are checked for steps 5-8: the browser (HTML `min=1 max=<stock>` on the quantity field, what a normal user meets) and the server (the same form submitted with the browser limits removed, what any client can send).

| Step | Action | Input data | Expected result | Actual result | Pass or fail |
|---|---|---|---|---|---|
| 1 | Staff logs in to /shop/wp-admin/ | itcs386-g07 + password | Dashboard opens | Dashboard opened as "ITCS386 Group 07" | Pass |
| 2 | Staff creates a simple product with stock management and publishes it | Name, price 199, Inventory: track stock, quantity 5 | "Product published" notice; stock 5 saved | "Product published." shown; product id 779, stock 5, price 199 | Pass |
| 3 | Customer (guest) searches for the product name | `G07 Stock Test 20261117-2208` | Product is found | Single match, the shop opened the product page directly (redirect) | Pass |
| 4 | Customer views the product page | - | Name, price 199 THB, in stock | "G07 Stock Test 20261117-2208", ฿199.00, "5 in stock"; quantity field min 1, max 5 | Pass |
| 5 | Customer enters a quantity above stock and clicks Add to cart | 6 | Rejected; cart stays empty | Browser blocked the submit: "Value must be less than or equal to 5." Server (limits removed): "You cannot add that amount of "G07 Stock Test 20261117-2208" to the cart because there is not enough stock (5 remaining)." Cart empty | Pass |
| 6 | Customer enters zero and clicks Add to cart | 0 | Rejected with a message; cart stays empty | Browser blocked: "Value must be greater than or equal to 1." Server (limits removed): **1 item added** with "has been added to your cart" | Fail (defect ST03-D01) |
| 7 | Customer enters a negative quantity and clicks Add to cart | -1 | Rejected with a message; cart unchanged | Browser blocked: "Value must be greater than or equal to 1." Server (limits removed): nothing added, no message shown | Pass (no feedback message, noted) |
| 8 | Customer types text into the quantity field and clicks Add to cart | `abc` | Rejected with a message; cart unchanged | A number field cannot hold `abc`, so it becomes empty and the browser allows the submit. **1 item added** with "has been added to your cart" | Fail (defect ST03-D02) |
| 9 | Customer empties the cart, adds a valid quantity | 2 | Cart: 1 line, quantity 2, total 398 THB | Notice "2 × "G07 Stock Test 20261117-2208" have been added to your cart."; cart quantity 2, total ฿398.00 | Pass |
| 10 | In the cart, customer raises the quantity above stock | 6 | Not allowed above stock | Block cart changed the value to 5 automatically (max 5), total ฿995.00; no message shown | Pass |
| 11 | Customer corrects the cart quantity | 2 | Quantity 2, total 398 THB | Quantity 2, total ฿398.00 | Pass |
| 12 | Customer checks out with Cash on delivery | Fictional billing data above | Order placed; confirmation shows order number, product × 2, total 398, COD | "Order received. Thank you. Your order has been received." Order # 780, Total ฿398.00, Payment: Cash on delivery, line "G07 Stock Test 20261117-2208 × 2 ฿398.00" | Pass |
| 13 | Staff opens order #780 in the admin | Order 780 | One line: the G07 product × 2, total 398, customer email matches | Status Processing, Customer: Guest, item "G07 Stock Test 20261117-2208 ฿199.00 × 2 ฿398.00", Order Total ฿398.00, email g07.st03.20261117-2208@example.com | Pass |
| 14 | Staff checks remaining stock | Product 779, Inventory tab | Stock 3 (5 - 2) | Quantity 3 (storefront also shows "3 in stock") | Pass |
| 15 | Staff marks the order Completed | Status = Completed, Update | Status Completed | "Order updated."; status Completed; note "Order status changed from Processing to Completed." | Pass |
| 16 | Customer reloads the order confirmation page | - | Consistent order information, now completed | "Order completed. Thank you. Your order has been fulfilled.", Order # 780, ฿398.00 | Pass |

**Summary:** 14 pass, 2 fail (steps 6 and 8). Stock control works (excess quantity rejected, stock reduced from 5 to 3). Invalid quantities 0 and text are silently turned into 1 item.

## Evidence (`screenshots/`)
| File | Step |
|---|---|
| ST03_step05_server_rejects_excess.jpg | 5 (server message; taken after the order, so it says "3 remaining") |
| ST03_D02_empty_quantity_added_as_1.jpg | 8 / defect ST03-D02 |
| ST03_step13_15_admin_order_completed.jpg | 13 and 15 |
| ST03_step14_admin_stock_3.jpg | 14 |
| ST03_step16_customer_order_completed.jpg | 12 and 16 |

Screenshots for steps 1-4 and 9-11 come from the automated run (`../UI testing/evidence/`), which repeats the same steps with fresh data.

## Defect reports

| Field | ST03-D01 |
|---|---|
| Title | Quantity 0 is added to the cart as 1 instead of being rejected |
| Severity | Low (the browser blocks it for normal users; any client that skips the browser check gets the wrong result) |
| Steps to reproduce | 1. Open any G07 simple product page as a guest. 2. Remove the `min` attribute of the quantity field (DevTools) or send the form with `quantity=0`. 3. Click Add to cart. |
| Expected result | Request rejected with a validation message; cart unchanged |
| Actual result | 1 item added, success notice "... has been added to your cart." |
| Evidence | Observed 17 Nov 2026 22:10 on product 779 (cart quantity became 1) |

| Field | ST03-D02 |
|---|---|
| Title | Non-numeric quantity is added to the cart as 1 without any message |
| Severity | Low-medium (reachable by a normal user, no browser block) |
| Steps to reproduce | 1. Open a G07 simple product page as a guest. 2. Type `abc` in the quantity field (the field becomes empty). 3. Click Add to cart. |
| Expected result | Validation message such as "Please enter a quantity"; cart unchanged |
| Actual result | 1 item added, success notice "... has been added to your cart." |
| Evidence | screenshots/ST03_D02_empty_quantity_added_as_1.jpg |

## Traceability row (for the matrix owner)
| Feature | Covered by ST03 steps |
|---|---|
| Staff: create product, manage stock | 1, 2 |
| Customer: search | 3 |
| Customer: product detail (price, stock) | 4 |
| Cart: add item, quantity validation (excess, zero, negative, text) | 5-9 |
| Cart: change quantity | 10, 11 |
| Checkout: cash on delivery, order confirmation | 12, 16 |
| Staff: view order | 13 |
| Stock reduced after order | 14 |
| Staff: change order status | 15 |
