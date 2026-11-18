# Latest verification — 19 November 2026

Two complete live Selenium runs passed on 19 November 2026 at approximately 00:53–00:54 Bangkok: **2 passed in 75.26 seconds**. Run 1: product 1146, order 1147. Run 2: product 1148, order 1149. Both verified validation, back navigation, checkout, stock 10→9, and saved Completed status in staff and guest views.

Full log: `verification-20261119-005315.txt`. Terminal screenshot: `evidence/2-passed-terminal.jpg`. Per-run screenshots and result JSONs are in `evidence/run-1-20261119-005315-29eabd/` and `evidence/run-2-20261119-005356-951bc1/`.

Fixes: save and reopen the draft before publishing; retry draft saving on the same form; tolerate replaced elements during publication; wait for loaded cart and payment content before assertions. No assertions were removed.

