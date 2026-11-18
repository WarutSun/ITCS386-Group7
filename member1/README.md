# Member 1 - ST01 product purchase

This package contains **only Member 1's work**. Teammates' source files are not included or changed. It can be copied into the team's ZIP/repository beside member3, member4 and member5.

## Start here

- [Manual test report and results](SystemTest/ST01_product_purchase.md)
- [Manual evidence index](SystemTest/evidence/original-manual/README.md)
- [New follow-up evidence](SystemTest/evidence/follow-up-20261118/README.md)
- [Automated UI test and run instructions](AutomatedUI/README.md)
- [Two-minute presentation notes](ST01_presentation_notes.md)
- [My feature coverage rows](ST01_traceability.md)

## What is complete

The user's original manual screenshots show product **491**, a THB **199** mug with initial stock **10**, and COD order **807** for one mug. Staff notes show stock **10 to 9**, and the saved staff status is **Completed**.

Interactive follow-up on 18 November confirmed and captured: back navigation preserves the cart, blank First name shows `Please enter a valid first name`, the temporary follow-up cart was emptied, and the guest view of order 807 says **Order completed** with the same THB 199 total. No additional order was placed during these follow-ups.

## Automated verification complete

Two complete live Selenium runs passed on 19 November 2026 at approximately 00:53–00:54 Bangkok: **2 passed in 75.26 seconds**. Run 1: product 1146, order 1147. Run 2: product 1148, order 1149. Both verified validation, back navigation, checkout, stock 10→9, and saved Completed status in staff and guest views.

Full log: `AutomatedUI/verification-20261119-005315.txt`. Terminal screenshot: `AutomatedUI/evidence/2-passed-terminal.jpg`. Per-run screenshots and result JSONs are in `AutomatedUI/evidence/run-1-20261119-005315-29eabd/` and `AutomatedUI/evidence/run-2-20261119-005356-951bc1/`.

The lab also logged email-send errors for the original order. These are documented as a suspected environment configuration issue, separate from the passing order/stock/status checks.

## Before submission

1. Add your real name to the test report's tester field.
2. Include the saved two-pass log, terminal screenshot, and both successful evidence folders.
3. Give `ST01_traceability.md` to the matrix owner and your README/results to the coordinator.
4. Keep the required final course structure: `project phase 2/README.md`, `API testing/`, `System testing/`, `UI testing/`, `Performance testing/`. For final consolidation, put this manual folder under `System testing/ST01` and this automation folder under `UI testing/ST01`; adjust document links when moving them.

Nothing in this package has been pushed to GitHub. The work is based on the ZIP supplied in this chat; it does not overwrite later teammate changes.
