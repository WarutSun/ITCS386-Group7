# ST01 - Product purchase across staff and guest views

## Case and execution details

| Field | Value |
|---|---|
| Objective | Staff publishes a G07 product; a guest buys one unit; staff verifies the order and saves Completed; guest confirmation is checked again |
| Preconditions | Course WooCommerce lab reachable; Group 7 staff access; separate staff and guest sessions; fictional customer data; COD enabled |
| Test data | Product `G07_ST01_TestMug_20261116_01`, ID **491**, simple product, THB **199.00**, initial stock **10**; quantity **1** |
| Customer data actually used | Guest; billing name `TestCustomer1 TestCustomer1`; `g07.st01.20261118@example.com`; 1 Test Road, Bangkok, Bangkok, 10200 |
| Tested by | Group 7 Member 1 (user), guided in chat; follow-up browser checks performed by Codex. Insert the student's name before submission |
| Dates | Product/cart evidence: 16 November 2026, approximately 00:51-00:56 Bangkok. Checkout/order evidence: 18 November 2026, approximately 00:12-00:36 Bangkok |
| Resulting order | **807**, COD, THB **199.00**, saved **Completed** |
| Evidence basis | Screenshots supplied by the user, plus explicit user confirmation of required-field validation. No missing observation is inferred from later success |

The server displays 17 November for an order captured on 18 November Bangkok time. Preserve both displayed server timestamps and local capture times; the offset is consistent with different time zones, not proof of a date defect.

## Manual execution

Evidence paths below are relative to `evidence/original-manual/`.

| Step | Action and input | Expected result | Actual result | Result | Evidence |
|---|---|---|---|---|---|
| 1 | Staff signs in with Group 7 account | Staff panel opens under Group 07 | Product editor shows `ITCS386 Group 07` | Pass | 01-product-published.png |
| 2 | Publish the named product at THB 199, stock 10 | Product published with intended data | Published notice and ID 491; guest page confirms THB 199 and 10 in stock | Pass | 01-product-published.png; 02-guest-product-price-stock.png |
| 3 | Guest opens the staff-created product's storefront page | Correct product name, price and stock are visible | Correct product page captured in Incognito | Pass (product view; does not claim search coverage) | 02-guest-product-price-stock.png |
| 4 | Add quantity 1 and open cart | One correct item, quantity 1, subtotal THB 199 | Correct item, quantity 1, estimated total THB 199 | Pass | 03-cart.png |
| 5 | Open checkout, go back, inspect cart, resume checkout | Same item and quantity remain; no duplicate | User said “I think yes”; no returned-cart screenshot supplied | Unverified in original manual run | Follow-up required; automated evidence is separate |
| 6 | Fill valid fictional data except leave First name blank; attempt checkout | Required-field error prevents completion | User explicitly confirmed an error appeared before filling First name; exact message/screenshot not supplied | Pass by tester statement; screenshot missing | User confirmation in chat |
| 7 | Correct First name and review COD summary | Valid values accepted; THB 199 total | Later confirmation shows actual billing name and THB 199; corrected form not captured | Supported by confirmation; form screenshot missing | 04-checkout-guest.png (before entry); 05-order-807-confirmation.png |
| 8 | Place one COD order | Confirmation shows correct order details | Order 807, correct mug × 1, THB 199, fictional email, COD | Pass | 05-order-807-confirmation.png |
| 9 | Staff opens order 807 | Same item, quantity, email, total and Processing status | All match the customer confirmation | Pass | 06-order-807-processing.png |
| 10 | Inspect stock note | Exactly one unit deducted | Note records stock 10 → 9 for this product | Pass (order-note evidence) | 07-stock-and-mail-notes.png |
| 11 | Change order 807 to Completed; click Update | Persisted Completed status | `Order updated.` notice and Completed status visible | Pass | 08-order-807-completed.png |
| 12 | Guest refreshes original order confirmation | Same order/total, with completion feedback where supported | No post-completion guest screenshot supplied for order 807 | Not verified in original manual run | Follow-up required; do not substitute another order's screenshot |

## Scope correction

The preparation draft assumed a registered customer and My Account. This execution used **guest checkout**, as shown in both checkout and staff screenshots. Therefore the final customer check uses the original guest confirmation page rather than claiming the guest has a My Account order history. The automated scenario follows this corrected guest flow with new data.

The original manual record had evidence gaps. The separately dated follow-up below now supplies the missing back-navigation, required-field error and guest-completion evidence. These checks do not change what was captured during the original run. The Selenium suite in `../AutomatedUI/` remains a separate deliverable and has not passed end-to-end in this environment.

## Observation ST01-ENV-01 - order email send failure

- Reproduction observed: complete the COD checkout, then inspect staff order notes for order 807.
- Expected, if email notification is in scope: configured order notifications can be sent.
- Actual: both “Processing order” and “New order” notifications record `Could not instantiate mail function`.
- Evidence: `evidence/original-manual/07-stock-and-mail-notes.png`.
- Impact: notification sending fails; order creation, totals, stock reduction and staff completion still succeeded.
- Classification: **suspected test-environment mail configuration issue**, not a proven WooCommerce code defect. The fictional example.com address is not a real inbox; inbox delivery was not tested. Ask the instructor whether notifications are expected in this lab. Do not change shared mail settings.

## Executed follow-up - 18 November 2026, approximately 19:24-19:30 Bangkok

Performed interactively through Chrome Incognito using the existing product. No new order was placed, and order 807 was not modified.

| Check | Actions | Actual result | Result | Evidence in `evidence/follow-up-20261118/` |
|---|---|---|---|---|
| Back navigation | Add one mug, open checkout, press browser Back | Exactly one line, quantity 1 and THB 199 remained | Pass | 01-back-navigation.jpg |
| Required First name | Reopen checkout; keep the other fictional billing details valid; clear First name; click Place Order | `Please enter a valid first name` appeared; checkout remained on screen without confirmation | Pass | 02-first-name-validation.jpg |
| Cleanup | Restore the fictional first name, return to cart and remove the follow-up item | `Your cart is currently empty!` displayed | Pass | 03-cart-cleaned.jpg |
| Guest completion | Open original guest order 807 confirmation; enter its fictional email at the requested verification form | `Order completed`; `Thank you. Your order has been fulfilled.`; order 807, mug × 1, THB 199, matching email and COD | Pass | 04-order-807-guest-completed.jpg |

**Conclusion:** the manual purchase flow and the three follow-up checks pass for the observations listed. The email-send failure remains an environment observation. Screenshots are original captures, not generated or reconstructed evidence. This does not claim Selenium repeatability.

## Links

- [Original evidence index](evidence/original-manual/README.md)
- [ST01 UI test](../AutomatedUI/test_st01_product_purchase.py)
- [UI run instructions and actual status](../AutomatedUI/README.md)
