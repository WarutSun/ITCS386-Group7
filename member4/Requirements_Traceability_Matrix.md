# Requirements Traceability Matrix (RTM)

**Project:** ITCS386 Project 2 — Group 7  
**System:** WooCommerce Shop  
**Source:** [Group 7 GitHub — `main`](https://github.com/WarutSun/ITCS386-Group7)  
**Reviewed:** 19 November 2026

> **Note:** `REQ-*` identifiers below are proposed RTM IDs derived from the team's test cases. They have **not** been verified against an official requirements specification. Match them to the assignment/SRS before final submission. `PASS` reflects recorded test evidence; `FAIL` indicates an observed deviation; `PARTIAL` indicates incomplete evidence; `NOT VERIFIED` means no conclusive recorded execution result.

## 1. Test coverage summary

| Area | Test cases | Member | Recorded result |
|---|---|---|---|
| Manual System | ST01 Product Purchase | 1 | Documented PASS (some steps evidenced by later follow-ups) |
| Manual System | ST02 Coupon Purchase | 4 | Steps 1–3, 5–10 PASS; step 4 not verified in document |
| Manual System | ST03 Stock/Cart | 3 | **14 PASS, 2 FAIL** (ST03-D01/D02) |
| Automated UI | ST01 | 1 | **2 runs PASS** |
| Automated UI | ST02 | 4 | **2 runs PASS** |
| Automated UI | ST03 | 3 | Full scenario PASS; two known defect tests XFAIL (runs 1 and 3) |
| API | ADD-01–06, UPDATE-01–06 | 2 | **12 PASS** |
| API | GET products, `per_page=5` | 5 | Script exists; result NOT VERIFIED |
| Performance | Average Load | 2 | PASS (p95 and HTTP failure rate) |
| Performance | Stress | 5 | **FAIL p95**, PASS HTTP failure rate |
| Performance | Soak | 5 | PASS (both thresholds) |
| Performance | Spike | 5 | PASS (both thresholds) |

## 2. Functional requirements and traceability

| Requirement ID | Expected system behavior | Manual Test ID / Result | Automated UI Test / Result | Owner | Evidence | Overall |
|---|---|---|---|---|---|---|
| REQ-F01 | Staff creates/publishes product at correct price and stock | ST01 1–2 PASS; ST03 1–2 PASS | ST01 and ST03 PASS | M1, M3 | [ST01](member1/README.md), [ST03](member3/System%20testing/ST03_stock_and_cart_validation.md) | PASS |
| REQ-F02 | Customer finds/views product with correct price and stock | ST01 3 PASS; ST03 3–4 PASS | ST01 and ST03 PASS | M1, M3 | [ST01](member1/README.md), [ST03](member3/System%20testing/ST03_stock_and_cart_validation.md) | PASS |
| REQ-F03 | Valid cart add shows correct quantity and subtotal | ST01 4 PASS; ST03 9 PASS | ST01 and ST03 PASS | M1, M3 | [ST01](member1/README.md), [ST03](member3/System%20testing/ST03_stock_and_cart_validation.md) | PASS |
| REQ-F04 | Back navigation from checkout retains cart | ST01 5 PASS (follow-up) | ST01 PASS ×2 | M1 | [ST01](member1/README.md) | PASS |
| REQ-F05 | Missing required checkout field is validated | ST01 6 PASS (follow-up) | ST01 PASS ×2 | M1 | [ST01](member1/README.md) | PASS |
| REQ-F06 | Cash-on-delivery checkout produces correct order confirmation and total | ST01 7; ST02 6–7; ST03 12 PASS | ST01, ST02, ST03 PASS | M1, M3, M4 | [ST01](member1/README.md), [ST02](member4/SystemTest/ST02.md), [ST03](member3/System%20testing/ST03_stock_and_cart_validation.md) | PASS |
| REQ-F07 | Staff order shows matching item, total, Processing status | ST01 8; ST02 8; ST03 13 PASS | ST01, ST02, ST03 PASS | M1, M3, M4 | [ST01](member1/README.md), [ST02](member4/SystemTest/ST02.md), [ST03](member3/System%20testing/ST03_stock_and_cart_validation.md) | PASS |
| REQ-F08 | Order reduces inventory by purchased quantity | ST01 9 (10→9); ST03 14 (5→3) PASS; ST02 8 notes 20→19 | ST01 and ST03 PASS | M1, M3, M4 | [ST01](member1/README.md), [ST03](member3/System%20testing/ST03_stock_and_cart_validation.md), [ST02](member4/SystemTest/ST02.md) | PASS |
| REQ-F09 | Staff can save Completed status; customer sees matching state | ST01 10–11; ST02 9–10; ST03 15–16 PASS | ST01, ST02, ST03 PASS | M1, M3, M4 | [ST01](member1/README.md), [ST02](member4/SystemTest/ST02.md), [ST03](member3/System%20testing/ST03_stock_and_cart_validation.md) | PASS |
| REQ-F10 | Staff creates a valid 10% coupon | ST02 2 PASS | ST02 PASS ×2 | M4 | [Manual](member4/SystemTest/ST02.md), [Automated](member4/AutomatedUI/test_coupon_checkout.py) | PASS |
| REQ-F11 | Invalid coupon rejected without changing total | ST02 4 **NOT VERIFIED** (placeholders) | ST02 PASS ×2 (asserts notice and unchanged total) | M4 | [Manual](member4/SystemTest/ST02.md), [Automated](member4/AutomatedUI/test_coupon_checkout.py) | **PARTIAL** |
| REQ-F12 | Valid coupon gives THB 20 discount: 200→180 | ST02 5 PASS | ST02 PASS ×2 | M4 | [Manual](member4/SystemTest/ST02.md), [Run 1](member4/AutomatedUI/evidence/run-1/result.txt) | PASS |
| REQ-F13 | Discounted total persists through checkout, order and customer history | ST02 6–10 PASS (order #702) | ST02 PASS ×2 (orders #737 and #740) | M4 | [Manual](member4/SystemTest/ST02.md), [Run 2](member4/AutomatedUI/evidence/run-2/result.txt) | PASS |
| REQ-F14 | Quantity above product stock is rejected | ST03 5 PASS | ST03 main flow PASS | M3 | [ST03](member3/System%20testing/ST03_stock_and_cart_validation.md) | PASS |
| REQ-F15 | Zero quantity is rejected, never silently changed to 1 | ST03 6 **FAIL**, defect D01 | Known defect test XFAIL | M3 | [ST03 / D01](member3/System%20testing/ST03_stock_and_cart_validation.md) | **FAIL** |
| REQ-F16 | Negative quantity does not add item | ST03 7 PASS (no feedback noted) | ST03 main flow PASS | M3 | [ST03](member3/System%20testing/ST03_stock_and_cart_validation.md) | PASS (feedback caveat) |
| REQ-F17 | Non-numeric or blank quantity is rejected, never silently changed to 1 | ST03 8 **FAIL**, defect D02 | Known defect test XFAIL | M3 | [ST03 / D02](member3/System%20testing/ST03_stock_and_cart_validation.md) | **FAIL** |
| REQ-F18 | Cart quantity respects stock cap and corrected total | ST03 10–11 PASS | ST03 main flow PASS | M3 | [ST03](member3/System%20testing/ST03_stock_and_cart_validation.md) | PASS |

## 3. API requirements and traceability

| Requirement ID | API input / expected behavior | Test ID | Recorded result | Owner | Source |
|---|---|---|---|---|---|
| REQ-A01 | Add existing product, quantity 2 | ADD-01 | PASS — HTTP 201, quantity 2 | M2 | [API evidence and specification](member2/README.md) |
| REQ-A02 | Reject Add Item without product ID | ADD-02 | PASS — HTTP 400 | M2 | [API README](member2/README.md) |
| REQ-A03 | Reject negative Add Item quantity | ADD-03 | PASS — HTTP 400 | M2 | [API README](member2/README.md) |
| REQ-A04 | Reject zero Add Item quantity | ADD-04 | PASS — HTTP 400 | M2 | [API README](member2/README.md) |
| REQ-A05 | Reject nonexistent product ID | ADD-05 | PASS — HTTP 400 | M2 | [API README](member2/README.md) |
| REQ-A06 | Cap Add Item quantity above maximum to 9999 | ADD-06 | PASS — HTTP 201, capped to 9999 | M2 | [API README](member2/README.md) |
| REQ-A07 | Update existing cart quantity 1→3 | UPDATE-01 | PASS — HTTP 200 | M2 | [API README](member2/README.md) |
| REQ-A08 | Reject Update Item without cart key | UPDATE-02 | PASS — HTTP 409 | M2 | [API README](member2/README.md) |
| REQ-A09 | Reject invalid cart key | UPDATE-03 | PASS — HTTP 409 | M2 | [API README](member2/README.md) |
| REQ-A10 | Reject negative quantity update; preserve original quantity 1 | UPDATE-04 | PASS — HTTP 400 | M2 | [API README](member2/README.md) |
| REQ-A11 | Reject zero quantity update; preserve original quantity 1 | UPDATE-05 | PASS — HTTP 400 | M2 | [API README](member2/README.md) |
| REQ-A12 | Reject above-maximum update; preserve original quantity 1 | UPDATE-06 | PASS — HTTP 400 | M2 | [API README](member2/README.md) |
| REQ-A13 | GET `/products?per_page=5` returns ≤5 items with required fields | `test_per_page_5` | **NOT VERIFIED** — code exists, no test-run evidence found | M5 | [API script](member5/api_testing/test_products.py) |

**Scope distinction:** The Add Item Store API in ADD-04 rejects zero quantity, while the separate product-page/form workflow in ST03-D01 silently adds one item for submitted zero quantity. They test different paths; API success does not resolve the UI/form defect.

## 4. Performance requirements and traceability

All profiles use the [shared shopper workload](member5/performance_testing/workload.js): product list, product search, add to cart and remove from cart. No checkout occurs during these load profiles.

| Requirement ID | Profile | Configuration | Threshold | Recorded evidence | Result | Owner |
|---|---|---|---|---|---|---|
| REQ-P01 | [Average Load](member2/performance_testing/average_load.js) | 30 s→5 VUs, 2 min→10 VUs, 30 s→0 | p95 < 1000 ms; HTTP failure rate < 5% | p95 **174.39 ms**, failures **0%**, requests **1290** ([README](member2/README.md)) | **PASS / PASS** | M2 |
| REQ-P02 | [Stress](member5/performance_testing/stress.js) | 5→10→20→30→40 VUs (30 s stages), 20 s ramp-down | p95 < 1000 ms; failures < 1% | p95 **2186.92 ms**, failures **0%**, requests **2148** ([JSON](member5/performance_testing/stress-summary.json)) | **FAIL p95 / PASS failures** | M5 |
| REQ-P03 | [Soak](member5/performance_testing/soak.js) | 30 s→10 VUs; 3 min at 10; 30 s→0 | p95 < 1000 ms; failures < 1% | p95 **209.63 ms**, failures **0%**, requests **2478** ([JSON](member5/performance_testing/soak-summary.json)) | **PASS / PASS** | M5 |
| REQ-P04 | [Spike](member5/performance_testing/spike.js) | 5 VUs baseline; spike to 20; return to 5 | p95 < 1000 ms; failures < 1% | p95 **513.27 ms**, failures **0%**, requests **1180** ([JSON](member5/performance_testing/spike-summary.json)) | **PASS / PASS** | M5 |

**Interpretation of k6 exported JSON:** In these files a threshold object's Boolean is a *breached threshold flag* (`true` = breached, `false` = not breached). A `http_req_failed` metric value of 0 means **zero failed-request rate**; do not treat the metric's `fails` field as the count of failed HTTP requests. Stress exceeds the p95 target while having 0% HTTP failures.

## 5. Defects and follow-up items

| Item | Finding | Status / next action |
|---|---|---|
| ST03-D01 | Zero quantity submitted through product form was accepted as 1 | **Open defect**; keep manual failure and automation XFAIL linked |
| ST03-D02 | Non-numeric/blank quantity was accepted as 1 without warning | **Open defect**; keep manual failure and automation XFAIL linked |
| ST02 manual step 4 | Missing actual invalid code, observed warning and final cart total in `ST02.md` | **Not verified in manual document**; inspect saved screenshot and complete step |
| Member 5 Products API | `test_products.py` exists without result evidence found | Add actual run log if required |
| Official requirement mapping | RTM IDs derived from test cases | Cross-reference official assignment/SRS requirement IDs before submission |
| ST01 mail notification | Manual order notes showed mail-function issue | Observation only; investigate if email delivery is in requirements scope |

## 6. Evidence index

- [Member 1 — ST01 Manual and Automated UI](member1/README.md); [Selenium test](member1/AutomatedUI/test_st01_product_purchase.py).
- [Member 2 — API Test Cases and Average Load](member2/README.md); [API add script](member2/api_testing/test_add_item.py); [API update script](member2/api_testing/test_update_item.py).
- [Member 3 — ST03 Manual Defects](member3/System%20testing/ST03_stock_and_cart_validation.md); [Automated UI Logs](member3/UI%20testing/README.md); [Team runner](member3/run_ui_suite.py).
- [Member 4 — ST02 Manual](member4/SystemTest/ST02.md); [Selenium script](member4/AutomatedUI/test_coupon_checkout.py); [Run 1](member4/AutomatedUI/evidence/run-1/result.txt); [Run 2](member4/AutomatedUI/evidence/run-2/result.txt).
- [Member 5 — Product API](member5/api_testing/test_products.py); [Stress](member5/performance_testing/stress-summary.json); [Soak](member5/performance_testing/soak-summary.json); [Spike](member5/performance_testing/spike-summary.json).

## 7. Submission checklist

- [x] Link ST01, ST02, ST03 manual tests to functional requirements.
- [x] Link recorded automated UI results, including confirmed defects.
- [x] Include all 12 Member 2 API cases plus Member 5 product API case.
- [x] Include all 4 performance profiles with recorded threshold results.
- [ ] Verify invalid-coupon manual step 4 in `member4/SystemTest/ST02.md`.
- [ ] Attach Member 5 product API execution result if required.
- [ ] Map derived requirement IDs to official course specification if supplied.
- [ ] Review with team and commit this Markdown file to repository root.

---

*This matrix records evidence present in the reviewed GitHub repository as of 19 November 2026. Preparing the matrix does not constitute a fresh test execution.*
