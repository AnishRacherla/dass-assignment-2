# Black-Box Test Report – QuickCart API

## 1. Test Environment

- Base URL under test: `http://localhost:8080/api/v1`
- Test tool: `pytest` + `requests`
- Command used (from `black-box-testing` folder):
  - `pytest -q`
- Authentication / context headers:
  - `X-Roll-Number: 2024101046`
  - `X-User-ID: 1`

## 2. Overall Execution Result

- Total automated black-box tests (current run): **50**
- Pass: **42**
- Fail: **8**
- Failure pattern: Eight scenarios (primarily cart, checkout, wallet, product ID validation, and review text validation) return success or the wrong error code instead of the expected `400 Bad Request`.

Earlier, an initial run failed with connection errors when the API service was not running. That historical environment bug is recorded separately in Section 4 as B1. The results above reflect the latest run with the server up and reachable.

Below, each test case is documented with its intended input, expected output, and justification. Section 4 then lists bug reports for the errors actually observed in the latest run.

---

## 3. Test Case Catalogue

Legend:
- **Method/URL**: HTTP method and path (BASE_URL omitted for brevity).
- **Headers**: Only differences from VALID_HEADERS are noted.
- **Body**: JSON request payload if present.
- **Expected**: Intended HTTP status code and key JSON structure.
- **Justification**: Why this case is important for validating the API.

### 3.1 Global Header / Authentication Tests

**BB-01 – Missing roll number header**
- Method/URL: `GET /products`
- Headers: _none_ (no `X-Roll-Number` or `X-User-ID`)
- Body: _none_
- Expected: `401 Unauthorized` with an error JSON explaining that roll number / auth is missing.
- Justification: Ensures the API does not serve requests without the required identity header and enforces basic access control consistently.

**BB-02 – Invalid roll number format**
- Method/URL: `GET /products`
- Headers: `X-Roll-Number: "abc"`, `X-User-ID: "1"`
- Body: _none_
- Expected: `400 Bad Request` with a clear validation error about the roll number format.
- Justification: Validates that header validation works and that malformed IDs do not get silently accepted.

**BB-03 – Missing user ID header**
- Method/URL: `GET /cart`
- Headers: `X-Roll-Number: "123"` (no `X-User-ID`)
- Body: _none_
- Expected: `400 Bad Request` indicating that the user id header is required.
- Justification: Ensures that user context is mandatory before accessing user-specific resources like the cart.

### 3.2 Products API Tests

**BB-04 – Get products happy path & structure**
- Method/URL: `GET /products`
- Headers: VALID_HEADERS
- Body: _none_
- Expected:
  - Status: `200 OK`.
  - JSON: non-empty list of product objects; each has `product_id`, `name`, `price`, `stock_quantity`, with `price >= 0`.
- Justification: Confirms core catalog endpoint works, returns the correct type (list), and enforces basic product schema and non-negative pricing.

**BB-05 – Invalid product ID**
- Method/URL: `GET /products/999999`
- Headers: VALID_HEADERS
- Body: _none_
- Expected: `404 Not Found` with an error body (e.g., "Product not found").
- Justification: Verifies correct handling of unknown resources and that invalid IDs do not cause 500s or wrong data.

### 3.3 Cart API Tests

**BB-06 – Add to cart (valid request)**
- Method/URL: `POST /cart/add`
- Headers: VALID_HEADERS
- Body: `{ "product_id": 1, "quantity": 2 }`
- Expected: `200 OK` or `201 Created`, with JSON confirming the cart update.
- Justification: Basic positive case for the cart; ensures normal shopping flow works when inputs are valid.

**BB-07 – Quantity zero**
- Method/URL: `POST /cart/add`
- Headers: VALID_HEADERS
- Body: `{ "product_id": 1, "quantity": 0 }`
- Expected: `400 Bad Request` with an error stating that quantity must be at least 1.
- Justification: Boundary test to ensure the API rejects non-sensical quantities and does not create empty cart entries.

**BB-08 – Negative quantity**
- Method/URL: `POST /cart/add`
- Headers: VALID_HEADERS
- Body: `{ "product_id": 1, "quantity": -5 }`
- Expected: `400 Bad Request` with a validation error.
- Justification: Prevents possible abuse and data corruption from negative quantities.

**BB-09 – Invalid product when adding to cart**
- Method/URL: `POST /cart/add`
- Headers: VALID_HEADERS
- Body: `{ "product_id": 999999, "quantity": 1 }`
- Expected: `404 Not Found` or `400` with a clear error about invalid product id.
- Justification: Checks that the cart cannot reference non-existent products.

**BB-10 – Exceeding stock quantity**
- Method/URL: `POST /cart/add`
- Headers: VALID_HEADERS
- Body: `{ "product_id": 1, "quantity": 100000 }`
- Expected: `400 Bad Request` with message like "Insufficient stock".
- Justification: Verifies stock checks and inventory constraints are enforced.

**BB-11 – Get cart structure**
- Method/URL: `GET /cart`
- Headers: VALID_HEADERS
- Body: _none_
- Expected:
  - Status: `200 OK`.
  - JSON: object with `cart_id`, `items` (list), and `total` (number).
- Justification: Ensures the cart representation and summary total follow the contractual schema.

**BB-12 – Missing product_id field in add-to-cart**
- Method/URL: `POST /cart/add`
- Headers: VALID_HEADERS
- Body: `{ "quantity": 1 }`
- Expected: `400 Bad Request` with error about missing `product_id`.
- Justification: Validates server-side required-field checks for cart creation.

**BB-13 – Non-integer quantity type**
- Method/URL: `POST /cart/add`
- Headers: VALID_HEADERS
- Body: `{ "product_id": 1, "quantity": "two" }`
- Expected: `400 Bad Request` with a type validation error.
- Justification: Ensures input type safety and prevents invalid data from entering the system.

**BB-26 – Missing quantity field in add-to-cart**
- Method/URL: `POST /cart/add`
- Headers: VALID_HEADERS
- Body: `{ "product_id": 1 }`
- Expected: `400 Bad Request` with error about missing `quantity`.
- Justification: Validates that both `product_id` and `quantity` are required; helps detect server-side defaults that silently treat missing quantity as 0.

**BB-27 – Float quantity in add-to-cart**
- Method/URL: `POST /cart/add`
- Headers: VALID_HEADERS
- Body: `{ "product_id": 1, "quantity": 1.5 }`
- Expected: `400 Bad Request` because quantity should be an integer count.
- Justification: Ensures the API does not accept fractional item counts, which could cause rounding and stock issues.

### 3.4 Coupon API Tests

**BB-14 – Apply invalid coupon code**
- Method/URL: `POST /coupon/apply`
- Headers: VALID_HEADERS
- Body: `{ "code": "INVALID" }`
- Expected: Typically `400 Bad Request` with JSON describing that the coupon is invalid (the test also allows `200` but then expects a consistent JSON structure).
- Justification: Verifies both error handling for wrong codes and that even failure responses use proper JSON.

**BB-15 – Missing coupon code field**
- Method/URL: `POST /coupon/apply`
- Headers: VALID_HEADERS
- Body: `{}`
- Expected: `400 Bad Request` with error about missing `code`.
- Justification: Ensures the coupon endpoint validates required fields and does not crash on empty bodies.

### 3.5 Checkout API Tests

**BB-16 – Invalid payment method**
- Method/URL: `POST /checkout`
- Headers: VALID_HEADERS
- Body: `{ "payment_method": "UPI" }`
- Expected: `400 Bad Request` when the payment method is not supported.
- Justification: Confirms that only documented payment methods are accepted and errors are explicit.

**BB-17 – Checkout with empty cart**
- Method/URL: `POST /checkout`
- Headers: VALID_HEADERS
- Body: `{ "payment_method": "COD" }`
- Expected: `400 Bad Request` indicating the cart is empty / nothing to checkout.
- Justification: Prevents accidental orders with no items; enforces business rule that cart must have contents.

**BB-28 – Checkout missing payment method field**
- Method/URL: `POST /checkout`
- Headers: VALID_HEADERS
- Body: `{}`
- Expected: `400 Bad Request` indicating that `payment_method` is required.
- Justification: Ensures checkout cannot proceed without an explicit payment method and validates body-level required fields.

### 3.6 Wallet API Tests

**BB-18 – Add invalid wallet amount (zero)**
- Method/URL: `POST /wallet/add`
- Headers: VALID_HEADERS
- Body: `{ "amount": 0 }`
- Expected: `400 Bad Request` with message that amount must be positive.
- Justification: Boundary test for wallet funding; prevents no-op or ambiguous operations.

**BB-19 – Pay with insufficient wallet balance**
- Method/URL: `POST /wallet/pay`
- Headers: VALID_HEADERS
- Body: `{ "amount": 100000 }`
- Expected: `400 Bad Request` or `402 Payment Required` indicating insufficient funds.
- Justification: Critical for financial correctness – wallet must not allow overspending.

**BB-20 – Add negative wallet amount**
- Method/URL: `POST /wallet/add`
- Headers: VALID_HEADERS
- Body: `{ "amount": -50 }`
- Expected: `400 Bad Request` with appropriate error.
- Justification: Guards against negative top-ups which could be exploited.

**BB-21 – Missing amount field in wallet add**
- Method/URL: `POST /wallet/add`
- Headers: VALID_HEADERS
- Body: `{}`
- Expected: `400 Bad Request` mentioning missing `amount`.
- Justification: Ensures required-field validation for monetary operations.

### 3.7 Reviews API Tests

**BB-22 – Invalid rating value**
- Method/URL: `POST /products/1/reviews`
- Headers: VALID_HEADERS
- Body: `{ "rating": 10, "comment": "Bad" }`
- Expected: `400 Bad Request` because rating is out of allowed range (e.g., 1–5).
- Justification: Validates that review scores are constrained, which affects averages and UI displays.

**BB-23 – Missing rating field**
- Method/URL: `POST /products/1/reviews`
- Headers: VALID_HEADERS
- Body: `{ "comment": "Nice product" }`
- Expected: `400 Bad Request` with error about missing `rating`.
- Justification: Ensures a review cannot be submitted without a numeric rating.

**BB-29 – Non-integer rating type**
- Method/URL: `POST /products/1/reviews`
- Headers: VALID_HEADERS
- Body: `{ "rating": "five", "comment": "Text rating" }`
- Expected: `400 Bad Request` with a type validation error.
- Justification: Confirms that rating must be numeric and prevents string/invalid types from polluting review scores.

### 3.8 Support Ticket API Tests

**BB-24 – Invalid support subject (too short)**
- Method/URL: `POST /support/ticket`
- Headers: VALID_HEADERS
- Body: `{ "subject": "Hi", "message": "Help me" }`
- Expected: `400 Bad Request` validating subject length / format.
- Justification: Checks basic input quality rules on user-submitted tickets.

**BB-25 – Missing ticket message field**
- Method/URL: `POST /support/ticket`
- Headers: VALID_HEADERS
- Body: `{ "subject": "Order issue" }`
- Expected: `400 Bad Request` with error that `message` is required.
- Justification: Ensures tickets always contain a descriptive message so support can act.

**BB-30 – Valid support ticket creation**
- Method/URL: `POST /support/ticket`
- Headers: VALID_HEADERS
- Body: `{ "subject": "Order #12345 delayed delivery", "message": "My order is delayed by more than 3 days. Please help." }`
- Expected: `200 OK` or `201 Created` with JSON containing at least an identifier and/or the subject.
- Justification: Positive-path test that a well-formed ticket is accepted and returns a structured JSON confirmation.

---

## 4. Bug Reports from This Execution

### Environment-Level Bug B1 – API service unavailable (connection refused) – historical

In an earlier run, **all tests failed** because the QuickCart API was not accepting TCP connections on `localhost:8080`. No application-level JSON response was ever received.

- **Endpoints affected:**
  - All of the above: `/products`, `/products/{id}`, `/cart`, `/cart/add`, `/coupon/apply`, `/checkout`, `/wallet/add`, `/wallet/pay`, `/products/{id}/reviews`, `/support/ticket`.
- **Representative requests:**
  - Example 1 (BB-04: get products):
    - Method: `GET`
    - URL: `http://localhost:8080/api/v1/products`
    - Headers: `{ "X-Roll-Number": "2024101046", "X-User-ID": "1" }`
    - Body: _none_
  - Example 2 (BB-22: invalid review rating):
    - Method: `POST`
    - URL: `http://localhost:8080/api/v1/products/1/reviews`
    - Headers: VALID_HEADERS
    - Body: `{ "rating": 10, "comment": "Bad" }`
  - Example 3 (BB-25: missing ticket message):
    - Method: `POST`
    - URL: `http://localhost:8080/api/v1/support/ticket`
    - Headers: VALID_HEADERS
    - Body: `{ "subject": "Order issue" }`

- **Expected results (per API spec and tests):**
  - Requests should return appropriate HTTP status codes (`200`, `201`, `400`, `401`, or `404` depending on scenario).
  - Responses should be valid JSON objects/lists matching the structures described in Section 3.
  - For invalid input / missing fields / wrong types / boundary values, the API should return `4xx` codes with clear error messages.

- **Actual results observed:**
  - Every request raised a client-side exception in `requests`:
    - `requests.exceptions.ConnectionError`
    - Root cause: `NewConnectionError` / `WinError 10061`: _"No connection could be made because the target machine actively refused it"_.
  - No HTTP status line or body was received, so none of the assertions about status codes or JSON could be evaluated.

- **Impact:**
  - From a black-box perspective, the entire QuickCart API is **unavailable** at the configured BASE_URL.
  - All functional features (product listing, cart, checkout, wallet, reviews, support) are effectively down.

- **Suggested fix / next steps:**
  1. Start the QuickCart backend service locally on port 8080 (or adjust BASE_URL in `test_quickcart.py` to match the actual host/port where the service is running).
  2. Confirm that `/api/v1/health` or an equivalent health check returns `200 OK`.
  3. Re-run `pytest -q` from `black-box-testing` and update this report with any remaining application-level bugs (e.g., wrong status codes or JSON shapes) once connectivity is restored.

That connectivity problem has since been resolved; the following bugs (B2–B9) come from the latest successful connection run.

### Bug B2 – Cart accepts zero quantity as success

- **Endpoint tested:** `POST /cart/add`
- **Test case:** BB-07 – Quantity zero.
- **Request payload:**
  - Method: `POST`
  - URL: `http://localhost:8080/api/v1/cart/add`
  - Headers: VALID_HEADERS (`X-Roll-Number: 2024101046`, `X-User-ID: 1`)
  - Body: `{ "product_id": 1, "quantity": 0 }`
- **Expected result:** `400 Bad Request` with an error message that quantity must be at least 1.
- **Actual result:** `200 OK` indicating success.
- **Impact:** The API accepts a nonsensical cart line with zero quantity, which can hide user mistakes, complicate totals, and conflict with typical e-commerce rules.

### Bug B3 – Cart treats missing quantity as success

- **Endpoint tested:** `POST /cart/add`
- **Test case:** BB-26 – Missing quantity field in add-to-cart.
- **Request payload:**
  - Method: `POST`
  - URL: `http://localhost:8080/api/v1/cart/add`
  - Headers: VALID_HEADERS
  - Body: `{ "product_id": 1 }`
- **Expected result:** `400 Bad Request` complaining that `quantity` is required.
- **Actual result:** `200 OK`.
- **Impact:** The server appears to default a missing quantity (likely to 0 or 1) instead of rejecting the request, which can mask client bugs and lead to unintended cart contents.

### Bug B4 – Missing product_id reported as 404 instead of 400

- **Endpoint tested:** `POST /cart/add`
- **Test case:** BB-12 – Missing product_id field in add-to-cart.
- **Request payload:**
  - Method: `POST`
  - URL: `http://localhost:8080/api/v1/cart/add`
  - Headers: VALID_HEADERS
  - Body: `{ "quantity": 1 }`
- **Expected result:** `400 Bad Request` indicating a missing required body field (`product_id`).
- **Actual result:** `404 Not Found`.
- **Impact:** A request that is syntactically wrong (missing field) is surfaced as a resource-not-found error, which is misleading for clients and makes debugging harder; it also suggests the handler may be trying to look up product id `0` or `null` instead of validating input first.

### Bug B5 – Checkout succeeds with an empty cart

- **Endpoint tested:** `POST /checkout`
- **Test case:** BB-17 – Checkout with empty cart.
- **Request payload:**
  - Method: `POST`
  - URL: `http://localhost:8080/api/v1/checkout`
  - Headers: VALID_HEADERS
  - Body: `{ "payment_method": "COD" }`
- **Expected result:** `400 Bad Request` indicating that the cart is empty and checkout cannot proceed.
- **Actual result:** `200 OK`.
- **Impact:** Allows users to "checkout" with no items in the cart, which violates business rules and can result in meaningless orders or incorrect analytics.

### Bug B6 – Cart total remains zero after adding items for a fresh user

- **Endpoint tested:** `GET /cart` after `POST /cart/add`
- **Test case:** `test_cart_total_matches_product_price_for_new_user`.
- **Request sequence (fresh cart for a different user):**
  1. `GET /products` with `OTHER_USER_HEADERS` to fetch a real product and its `price`.
  2. `POST /cart/add` with body `{ "product_id": <id from step 1>, "quantity": 2 }` and the same headers.
  3. `GET /cart` with those headers to read the cart summary.
- **Expected result:**
  - After step 2, the cart should contain exactly that one line item.
  - After step 3, the `total` field in the cart JSON should equal `price * 2` for the chosen product.
- **Actual result:**
  - Step 2 returns a success status (`200`/`201`).
  - Step 3 returns `200 OK`, but the cart JSON reports `total = 0` instead of `price * 2`.
- **Impact:** The cart summary total does not reflect items that have been added, which breaks billing correctness, confuses users, and can cause undercharging at checkout.

### Bug B7 – Non-integer product ID path returns 404 instead of validation error

- **Endpoint tested:** `GET /products/abc`
- **Test case:** `test_invalid_product_id_non_integer`.
- **Request payload:**
  - Method: `GET`
  - URL: `http://localhost:8080/api/v1/products/abc`
  - Headers: VALID_HEADERS
  - Body: _none_
- **Expected result:** `400 Bad Request` (or similar 4xx) with a clear validation error that product ID must be an integer.
- **Actual result:** `404 Not Found`.
- **Impact:** A clearly malformed path parameter is reported as “not found” instead of a validation failure, which hides client-side bugs and makes error handling less precise.

### Bug B8 – Wallet allows decimal top-up amounts

- **Endpoint tested:** `POST /wallet/add`
- **Test case:** `test_wallet_add_decimal_amount`.
- **Request payload:**
  - Method: `POST`
  - URL: `http://localhost:8080/api/v1/wallet/add`
  - Headers: VALID_HEADERS
  - Body: `{ "amount": 1.5 }`
- **Expected result:** `400 Bad Request` because wallet amounts should be whole-number currency units.
- **Actual result:** `200 OK`.
- **Impact:** Accepting fractional amounts can lead to rounding inconsistencies and conflicts with integer-based balance tracking.

### Bug B9 – Review accepts blank comment consisting only of whitespace

- **Endpoint tested:** `POST /products/1/reviews`
- **Test case:** `test_review_blank_comment`.
- **Request payload:**
  - Method: `POST`
  - URL: `http://localhost:8080/api/v1/products/1/reviews`
  - Headers: VALID_HEADERS
  - Body: `{ "rating": 4, "comment": "   " }`
- **Expected result:** `400 Bad Request` because the comment text is effectively empty.
- **Actual result:** `200 OK`.
- **Impact:** Allows meaningless reviews into the system, which can degrade review quality and user experience.

---

## 5. Coverage Versus Requirements

The current automated black-box tests are designed to verify:

- **Correct HTTP status codes:**
  - Positive paths (e.g., `GET /products`, valid `POST /cart/add`).
  - Error cases for invalid inputs, missing fields, wrong types, and boundary values.
- **Proper JSON response structures:**
  - Product list structure, cart object schema, error response JSON format, and review/ticket payloads.
- **Correctness of returned data:**
  - Non-negative prices, stock constraints, wallet balance rules, rating ranges, and meaningful error messages.

Once the API service is running and reachable, these tests will detect any mismatches between implementation and specification for all the scenarios described in Section 3.
