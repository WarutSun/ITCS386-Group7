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

## What still prevents a complete automation claim

The Selenium test is implemented and both cases collect successfully, but its fresh browser was blocked before login (`ERR_BLOCKED_BY_CLIENT`). The first execution failed with a timeout; the second did not run. Run `python run_st01.py` in `AutomatedUI` on a working browser environment and obtain two full passes before claiming automated repeatability. The real failure evidence is included.

The lab also logged email-send errors for the original order. These are documented as a suspected environment configuration issue, separate from the passing order/stock/status checks.

## Before submission

1. Add your real name to the test report's tester field.
2. Complete and preserve the two successful Selenium runs, or accurately disclose the remaining blocker.
3. Give `ST01_traceability.md` to the matrix owner and your README/results to the coordinator.
4. Keep the required final course structure: `project phase 2/README.md`, `API testing/`, `System testing/`, `UI testing/`, `Performance testing/`. For final consolidation, put this manual folder under `System testing/ST01` and this automation folder under `UI testing/ST01`; adjust document links when moving them.

Nothing in this package has been pushed to GitHub. The work is based on the ZIP supplied in this chat; it does not overwrite later teammate changes.
