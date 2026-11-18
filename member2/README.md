# Member 2 — API and Average Load Testing

## ITCS386 Project 2 — Group 7

### Responsibilities

Member 2 is responsible for:

1. API testing for `POST /cart/add-item`
2. API testing for `POST /cart/update-item`
3. Average-load performance testing using k6
4. Sharing the common performance workload with Member 5

---

# 1. Test Environment

## System Under Test

WooCommerce Shop

```text
http://157.85.102.236/shop/
```

WooCommerce Store API base URL:

```text
http://157.85.102.236/shop/wp-json/wc/store/v1
```

## API Test Product

A dedicated Group 7 product was created to avoid interfering with products used by other groups or other Group 7 test scenarios.

| Field | Value |
|---|---|
| Product ID | `778` |
| Product Name | `G07-M2-API-Test-Product` |
| Regular Price | 100 THB |
| Purchasable | Yes |
| In Stock | Yes |

## Tools

- Python 3.13.2
- pytest 9.1.1
- requests 2.32.5
- k6 2.3.0

---

# 2. API Testing

The API tests were implemented with Python, pytest, and the `requests` library.

Two WooCommerce Store API operations were tested:

```text
POST /cart/add-item
POST /cart/update-item
```

Each test creates a fresh cart and obtains its own `Cart-Token`. This reduces dependencies between test cases and makes the tests repeatable.

The tests verify both HTTP status codes and important response fields such as product ID, quantity, cart item key, error code, and final cart state.

---

# 3. Input Space Partitioning

The API input space was divided into several partitions:

- Valid input
- Missing required input
- Invalid input
- Lower boundary
- Nonexistent identifier
- Upper boundary / above maximum

This allows the tests to cover normal behavior as well as invalid and boundary conditions.

---

# 4. API Operation 1 — Add Item

## Endpoint

```text
POST /cart/add-item
```

Purpose: add a product to a customer's cart.

Test file:

```text
api_testing/test_add_item.py
```

## Test Cases

| ID | Partition | Input | Expected / Verified Behavior | Actual Status | Result |
|---|---|---|---|---|---|
| ADD-01 | Valid | Product 778, quantity 2 | Product is added with quantity 2 | 201 | PASS |
| ADD-02 | Missing input | Product ID omitted | Request is rejected | 400 | PASS |
| ADD-03 | Invalid input | Quantity = -1 | Negative quantity is rejected | 400 | PASS |
| ADD-04 | Lower boundary | Quantity = 0 | Zero quantity is rejected | 400 | PASS |
| ADD-05 | Invalid identifier | Product ID = 99999999 | Nonexistent product is rejected | 400 | PASS |
| ADD-06 | Above maximum | Requested quantity = 10000 | Quantity is capped at maximum 9999 | 201 | PASS |

## Important Observations

### ADD-01 — Valid Add

The API successfully added product `778` with quantity `2`.

```text
HTTP Status: 201
Quantity: 2
```

### ADD-02 — Missing Product ID

The API returned:

```text
HTTP Status: 400
Error code: woocommerce_rest_cart_invalid_product
```

The request was rejected because no valid product ID was supplied.

### ADD-03 and ADD-04 — Invalid Quantity

For negative and zero quantities, the API returned:

```text
HTTP Status: 400
Error code: woocommerce_rest_product_invalid_quantity
```

The API does not allow a product to be added with a quantity less than or equal to zero.

### ADD-05 — Nonexistent Product

Using product ID `99999999` returned:

```text
HTTP Status: 400
Error code: woocommerce_rest_cart_invalid_product
```

### ADD-06 — Above Maximum

The product reported a maximum cart quantity of:

```text
9999
```

The test requested:

```text
10000
```

Instead of rejecting the request, the Add Item API accepted it and capped the quantity at:

```text
9999
```

Observed result:

```text
HTTP Status: 201
Requested quantity: 10000
Actual quantity: 9999
```

The test therefore verifies the observed capping behavior.

---

# 5. API Operation 2 — Update Item

## Endpoint

```text
POST /cart/update-item
```

Purpose: change the quantity of an existing cart item.

Test file:

```text
api_testing/test_update_item.py
```

For tests that require an existing item, the test first adds product `778`, retrieves the generated cart item `key`, and then performs the update.

## Test Cases

| ID | Partition | Input | Expected / Verified Behavior | Actual Status | Result |
|---|---|---|---|---|---|
| UPDATE-01 | Valid | Quantity 1 → 3 | Quantity changes to 3 | 200 | PASS |
| UPDATE-02 | Missing input | Missing item key | Request is rejected | 409 | PASS |
| UPDATE-03 | Invalid identifier | Invalid item key | Request is rejected | 409 | PASS |
| UPDATE-04 | Invalid input | Quantity = -1 | Update rejected; quantity remains 1 | 400 | PASS |
| UPDATE-05 | Lower boundary | Quantity = 0 | Update rejected; quantity remains 1 | 400 | PASS |
| UPDATE-06 | Above maximum | Quantity = 10000 | Update rejected; quantity remains 1 | 400 | PASS |

## Important Observations

### UPDATE-01 — Valid Update

The product was initially added with quantity `1` and then updated to quantity `3`.

```text
HTTP Status: 200
Original quantity: 1
Updated quantity: 3
```

### UPDATE-02 and UPDATE-03 — Invalid Cart Item Key

Both missing and nonexistent item keys returned:

```text
HTTP Status: 409
Error code: woocommerce_rest_cart_invalid_key
Message: Cart item does not exist.
```

### UPDATE-04 and UPDATE-05 — Invalid Quantity

For quantities `-1` and `0`, the API returned:

```text
HTTP Status: 400
Error code: invalid_quantity
```

The existing cart item remained unchanged at quantity `1`.

### UPDATE-06 — Above Maximum

Maximum allowed quantity:

```text
9999
```

Requested quantity:

```text
10000
```

The Update Item API rejected the request:

```text
HTTP Status: 400
Error code: invalid_quantity
```

The original quantity remained `1`.

This differs from the Add Item API, which capped an above-maximum quantity to `9999`.

---

# 6. API Test Execution

## Run Add Item Tests

From the `member2` directory:

```powershell
python -m pytest api_testing/test_add_item.py -v
```

## Run Update Item Tests

```powershell
python -m pytest api_testing/test_update_item.py -v
```

## Run Both API Suites

```powershell
python -m pytest api_testing/test_add_item.py api_testing/test_update_item.py -v
```

## Full API Test Result

The final combined execution produced:

```text
12 passed in 3.85s
```

All 12 API test cases passed in the recorded full run.

Evidence:

```text
evidence/API-FULL-RUN/API-FULL-RUN-12-PASSED.JPG
```

Additional evidence is stored under:

```text
evidence/ADD/
evidence/ADD-FULL-RUN/
evidence/UPDATE/
evidence/UPDATE-FULL-RUN/
```

---

# 7. Performance Testing — Average Load

## Tool

Grafana k6

## Shared Workload

The Average Load test reuses the common performance workload maintained with Member 5:

```text
../member5/performance_testing/workload.js
```

The Average Load profile is defined in:

```text
performance_testing/average_load.js
```

The common workload represents repeated customer activity using browsing, searching, and cart operations.

No checkout or order creation is performed during the performance test.

---

# 8. Average Load Profile

The final Average Load profile uses `ramping-vus`.

Stages:

| Stage | Duration | Target VUs |
|---|---:|---:|
| Warm-up | 30 seconds | 5 |
| Average load | 2 minutes | 10 |
| Ramp-down | 30 seconds | 0 |

Maximum virtual users:

```text
10 VUs
```

Total configured test duration:

```text
3 minutes
```

## Thresholds

```javascript
http_req_duration: ['p(95)<1000']
http_req_failed: ['rate<0.05']
```

The response-time threshold requires 95% of HTTP requests to complete within 1 second.

The error-rate threshold requires the HTTP request failure rate to remain below 5%.

These thresholds are team-defined performance criteria for the test profile.

---

# 9. Smoke Test Result

Before running the Average Load profile, a small smoke test was executed with:

```text
1 VU
10 seconds
```

Observed results:

| Metric | Result |
|---|---:|
| Checks | 9 / 9 passed |
| HTTP failure rate | 0.00% |
| Average response time | 113.95 ms |
| p95 response time | 164.05 ms |
| Maximum response time | 185.99 ms |
| Iterations | 3 |
| vus_max | 1 |

Both configured thresholds passed.

---

# 10. Final Average Load Result

The final Average Load test reached up to 10 concurrent virtual users.

Observed results:

| Metric | Result |
|---|---:|
| Checks | 960 / 960 passed |
| Check success rate | 100.00% |
| HTTP requests | 1,290 |
| HTTP failures | 0 / 1,290 |
| HTTP failure rate | 0.00% |
| Average response time | 108.62 ms |
| Median response time | 93.93 ms |
| p90 response time | 155.93 ms |
| p95 response time | 174.39 ms |
| Maximum response time | 304.96 ms |
| Iterations | 320 |
| Interrupted iterations | 0 |
| Maximum VUs | 10 |

## Threshold Results

### Response Time

Required:

```text
p95 < 1000 ms
```

Observed:

```text
p95 = 174.39 ms
```

Result:

```text
PASS
```

### HTTP Failure Rate

Required:

```text
failure rate < 5%
```

Observed:

```text
failure rate = 0.00%
```

Result:

```text
PASS
```

---

# 11. Average Load Analysis

The tested Average Load profile passed both defined performance thresholds.

At a workload reaching 10 concurrent virtual users:

- All 960 checks succeeded.
- None of the 1,290 HTTP requests were reported as failed.
- p95 response time was 174.39 ms.
- Maximum observed HTTP request duration was 304.96 ms.
- No iterations were interrupted.

The p95 response time remained well below the 1-second threshold.

The smoke test produced a p95 of 164.05 ms, while the Average Load test produced a p95 of 174.39 ms. This is an increase of approximately 10.34 ms, or about 6.3%.

Within the tested range, increasing the workload up to 10 VUs therefore caused only a small increase in p95 response time and did not produce HTTP request failures.

This result does **not** mean that 10 VUs is the maximum capacity of the system. It only demonstrates that the system met the defined thresholds under the tested Average Load profile.

A higher-load Stress Test is required to identify where response time exceeds 1 second or where errors begin to occur.

---

# 12. Running the Average Load Test

From the `member2` directory:

```powershell
k6 run performance_testing/average_load.js
```

The recorded Average Load evidence is stored under:

```text
evidence/AVERAGE-LOAD/
```

including:

```text
AVERAGE-LOAD-PASSED.JPG
average-load-results.txt
```

---

# 13. Evidence Structure

```text
evidence/
├── ADD/
│   ├── ADD-01-PASSED.JPG
│   ├── ADD-02-PASSED.JPG
│   ├── ADD-03-PASSED.JPG
│   ├── ADD-04-PASSED.JPG
│   ├── ADD-05-PASSED.JPG
│   └── ADD-06-PASSED.JPG
│
├── ADD-FULL-RUN/
│   └── ADD-FULL-RUN-PASSED.JPG
│
├── API-FULL-RUN/
│   └── API-FULL-RUN-12-PASSED.JPG
│
├── UPDATE/
│   ├── UPDATE-01-PASSED.JPG
│   ├── UPDATE-02-PASSED.JPG
│   ├── UPDATE-03-PASSED.JPG
│   ├── UPDATE-04-PASSED.JPG
│   ├── UPDATE-05-PASSED.JPG
│   └── UPDATE-06-PASSED.JPG
│
├── UPDATE-FULL-RUN/
│   └── UPDATE-FULL-RUN-PASSED.JPG
│
└── AVERAGE-LOAD/
    ├── AVERAGE-LOAD-PASSED.JPG
    └── average-load-results.txt
```

---

# 14. Summary

Member 2 completed two automated API operation suites and one Average Load performance test.

## API Testing

```text
Add Item:       6 / 6 PASS
Update Item:    6 / 6 PASS
Total:         12 / 12 PASS
```

The API tests cover valid, missing, invalid, and boundary input partitions.

## Average Load

```text
Maximum tested VUs:       10
HTTP requests:            1,290
Checks passed:            960 / 960
HTTP failure rate:        0.00%
Average response time:    108.62 ms
p95 response time:        174.39 ms
Maximum response time:    304.96 ms
```

Both Average Load thresholds passed.

No API test failures or HTTP request failures remained in the recorded final runs.