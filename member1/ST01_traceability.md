# Member 1 coverage rows for the group matrix

| Feature | ST01 steps | Evidence / limits |
|---|---|---|
| Staff product creation | 1-2 | Product 491 published; initial price and stock verified on guest page |
| Product details | 3 | Correct name, THB 199, stock 10 in original run |
| Cart add and quantity/total | 4 | One mug, quantity 1, THB 199 |
| Checkout back navigation | 5 + dated follow-up | Cart preserved after browser Back; follow-up screenshot |
| Required billing field validation | 6 + dated follow-up | Blank First name rejected with visible message |
| Checkout/COD and confirmation | 7-8 | Order 807, mug × 1, THB 199, COD |
| Staff order viewing | 9 | Order/customer/item/total match |
| Stock reduction | 10 | Order note records 10 → 9 |
| Staff order completion | 11 | Saved Completed status and update notice |
| Guest post-completion view | 12 + dated follow-up | Order completed; same order, item and total after email verification |
| Notification emails | Environment observation | Send failure logged; inbox delivery not tested |

Not claimed by this manual case: catalog sorting/filtering, categories, coupon behavior, customer registration/login, My Account order history, staff customer listing, or product deletion. Other scenario owners assign these features as appropriate. The Selenium test includes product search, but that coverage remains unverified until execution passes.
