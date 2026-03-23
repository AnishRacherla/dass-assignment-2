import requests
import pytest

BASE_URL = "http://localhost:8080/api/v1"

VALID_HEADERS = {
    "X-Roll-Number": "2024101046",
    "X-User-ID": "1"
}

INVALID_ROLL_HEADERS = {
    "X-Roll-Number": "abc",
    "X-User-ID": "1"
}

NO_USER_HEADERS = {
    "X-Roll-Number": "123"
}

OTHER_USER_HEADERS = {
    "X-Roll-Number": "2024101046",
    "X-User-ID": "2",
}

THIRD_USER_HEADERS = {
    "X-Roll-Number": "2024101046",
    "X-User-ID": "3",
}


# ---------------------------
# 🔹 GLOBAL HEADER TESTS
# ---------------------------

def test_missing_roll_number():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 401


def test_invalid_roll_number():
    response = requests.get(f"{BASE_URL}/products", headers=INVALID_ROLL_HEADERS)
    assert response.status_code == 400


def test_missing_user_id():
    response = requests.get(f"{BASE_URL}/cart", headers=NO_USER_HEADERS)
    assert response.status_code == 400


def test_add_to_cart_missing_all_headers():
    payload = {"product_id": 1, "quantity": 1}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload)
    # Cart operations should also enforce auth headers like other endpoints
    assert response.status_code == 401


# ---------------------------
# 🔹 PRODUCTS
# ---------------------------

def test_get_products_structure():
    response = requests.get(f"{BASE_URL}/products", headers=VALID_HEADERS)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    product = data[0]
    assert "product_id" in product
    assert "name" in product
    assert "price" in product
    assert "stock_quantity" in product
    assert product["price"] >= 0


def test_get_products_full_schema_for_all_items():
    """Verify that every product in the list has the expected fields and types."""
    response = requests.get(f"{BASE_URL}/products", headers=VALID_HEADERS)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    for product in data:
        assert isinstance(product, dict)
        assert "product_id" in product
        assert "name" in product
        assert "price" in product
        assert "stock_quantity" in product
        assert isinstance(product["product_id"], int)
        assert isinstance(product["name"], str)
        assert isinstance(product["price"], (int, float))
        assert isinstance(product["stock_quantity"], int)
        assert product["price"] >= 0
        assert product["stock_quantity"] >= 0


def test_invalid_product_id():
    response = requests.get(f"{BASE_URL}/products/999999", headers=VALID_HEADERS)
    assert response.status_code == 404


def test_product_detail_matches_list_entry():
    """Ensure /products/{id} returns data consistent with the list entry."""
    list_resp = requests.get(f"{BASE_URL}/products", headers=VALID_HEADERS)
    assert list_resp.status_code == 200
    products = list_resp.json()
    assert isinstance(products, list)
    assert len(products) > 0

    first = products[0]
    product_id = first["product_id"]

    detail_resp = requests.get(f"{BASE_URL}/products/{product_id}", headers=VALID_HEADERS)
    assert detail_resp.status_code == 200
    detail = detail_resp.json()

    assert detail["product_id"] == first["product_id"]
    assert detail["name"] == first["name"]
    assert detail["price"] == first["price"]


def test_invalid_product_id_non_integer():
    response = requests.get(f"{BASE_URL}/products/abc", headers=VALID_HEADERS)
    # Non-integer path params should be rejected with a 4xx validation error
    assert response.status_code == 400


# ---------------------------
# 🔹 CART
# ---------------------------

def test_add_to_cart_valid():
    payload = {"product_id": 1, "quantity": 2}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)

    # Accept either success OR detect bug
    assert response.status_code in [200, 201]


def test_add_to_cart_quantity_zero():
    payload = {"product_id": 1, "quantity": 0}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_add_to_cart_negative_quantity():
    payload = {"product_id": 1, "quantity": -5}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_add_to_cart_invalid_product():
    payload = {"product_id": 999999, "quantity": 1}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 404


def test_add_to_cart_exceed_stock():
    payload = {"product_id": 1, "quantity": 100000}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_cart_structure():
    response = requests.get(f"{BASE_URL}/cart", headers=VALID_HEADERS)

    assert response.status_code == 200
    data = response.json()

    assert "cart_id" in data
    assert "items" in data
    assert "total" in data

    assert isinstance(data["items"], list)
    assert isinstance(data["total"], (int, float))


def test_cart_items_have_required_fields_after_add():
    # Add a valid item, then verify cart item structure
    add_payload = {"product_id": 1, "quantity": 1}
    add_resp = requests.post(f"{BASE_URL}/cart/add", json=add_payload, headers=VALID_HEADERS)
    assert add_resp.status_code in [200, 201]

    cart_resp = requests.get(f"{BASE_URL}/cart", headers=VALID_HEADERS)
    assert cart_resp.status_code == 200
    cart = cart_resp.json()
    assert "items" in cart
    assert isinstance(cart["items"], list)
    assert len(cart["items"]) > 0
    item = cart["items"][0]
    assert "product_id" in item
    assert "quantity" in item
    assert isinstance(item["quantity"], int)
    assert item["quantity"] >= 1


def test_cart_total_matches_product_price_for_new_user():
    """For a fresh user, cart total should equal price * quantity after a single add."""
    # Use a distinct user id so we get a clean cart state
    headers = OTHER_USER_HEADERS

    # Get a real product and its price
    prod_resp = requests.get(f"{BASE_URL}/products", headers=headers)
    assert prod_resp.status_code == 200
    products = prod_resp.json()
    assert len(products) > 0
    first = products[0]
    product_id = first["product_id"]
    price = first["price"]

    # Add two units of that product to the cart
    add_payload = {"product_id": product_id, "quantity": 2}
    add_resp = requests.post(f"{BASE_URL}/cart/add", json=add_payload, headers=headers)
    assert add_resp.status_code in [200, 201]

    # Fetch the cart and verify total matches price * quantity exactly
    cart_resp = requests.get(f"{BASE_URL}/cart", headers=headers)
    assert cart_resp.status_code == 200
    cart = cart_resp.json()
    assert "total" in cart
    assert isinstance(cart["total"], (int, float))
    expected_total = price * 2
    assert cart["total"] == expected_total


def test_cart_total_never_negative():
    """Regardless of previous operations, cart total should never be negative."""
    response = requests.get(f"{BASE_URL}/cart", headers=VALID_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert isinstance(data["total"], (int, float))
    assert data["total"] >= 0


def test_cart_isolated_between_users():
    """Items added for one user should not appear in another user's cart."""
    # Use user 1 to add a product
    prod_resp = requests.get(f"{BASE_URL}/products", headers=VALID_HEADERS)
    assert prod_resp.status_code == 200
    products = prod_resp.json()
    assert len(products) > 0
    product_id = products[0]["product_id"]

    add_payload = {"product_id": product_id, "quantity": 1}
    add_resp = requests.post(f"{BASE_URL}/cart/add", json=add_payload, headers=VALID_HEADERS)
    assert add_resp.status_code in [200, 201]

    # Now check cart for a completely different user
    other_cart_resp = requests.get(f"{BASE_URL}/cart", headers=THIRD_USER_HEADERS)
    assert other_cart_resp.status_code == 200
    other_cart = other_cart_resp.json()
    assert "items" in other_cart
    assert isinstance(other_cart["items"], list)
    # The specific product added for user 1 should not appear for user 3
    assert all(item.get("product_id") != product_id for item in other_cart["items"])


# ---------------------------
# 🔹 COUPONS
# ---------------------------

def test_apply_invalid_coupon():
    payload = {"code": "INVALID"}
    response = requests.post(f"{BASE_URL}/coupon/apply", json=payload, headers=VALID_HEADERS)

    # For an invalid coupon code, API should reject the request
    # with a 4xx error rather than accepting it as success.
    assert response.status_code == 400

    # Response for invalid coupon must still be valid JSON
    try:
        data = response.json()
    except Exception:
        pytest.fail("Coupon response is not JSON → BUG")

    # Basic structure check: should contain some error indicator
    assert isinstance(data, dict)
    assert any(key in data for key in ["error", "message", "detail"])


def test_apply_coupon_empty_body():
    response = requests.post(f"{BASE_URL}/coupon/apply", headers=VALID_HEADERS)
    # Missing JSON body should be treated as a bad request
    assert response.status_code == 400


def test_apply_coupon_empty_string_code():
    payload = {"code": ""}
    response = requests.post(f"{BASE_URL}/coupon/apply", json=payload, headers=VALID_HEADERS)
    # Empty code value should not be treated as a valid coupon
    assert response.status_code == 400


# ---------------------------
# 🔹 CHECKOUT
# ---------------------------

def test_checkout_invalid_payment():
    payload = {"payment_method": "UPI"}
    response = requests.post(f"{BASE_URL}/checkout", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_checkout_empty_cart():
    payload = {"payment_method": "COD"}
    response = requests.post(f"{BASE_URL}/checkout", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_checkout_no_body():
    response = requests.post(f"{BASE_URL}/checkout", headers=VALID_HEADERS)
    # Checkout requires a JSON body with at least payment_method
    assert response.status_code == 400


# ---------------------------
# 🔹 WALLET
# ---------------------------

def test_wallet_add_invalid_amount():
    payload = {"amount": 0}
    response = requests.post(f"{BASE_URL}/wallet/add", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_wallet_pay_insufficient_balance():
    payload = {"amount": 100000}
    response = requests.post(f"{BASE_URL}/wallet/pay", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_wallet_add_missing_roll_number():
    payload = {"amount": 100}
    # No headers at all
    response = requests.post(f"{BASE_URL}/wallet/add", json=payload)
    # Consistent with missing-roll behavior on /products: should be 401
    assert response.status_code == 401


def test_wallet_add_missing_user_id():
    payload = {"amount": 100}
    # Use NO_USER_HEADERS that omits X-User-ID
    response = requests.post(f"{BASE_URL}/wallet/add", json=payload, headers=NO_USER_HEADERS)
    # Consistent with /cart behavior: missing user id should be treated as bad request
    assert response.status_code == 400


def test_wallet_add_decimal_amount():
    payload = {"amount": 1.5}
    response = requests.post(f"{BASE_URL}/wallet/add", json=payload, headers=VALID_HEADERS)

    # Wallet amounts should be whole-number currency units
    assert response.status_code == 400


def test_wallet_add_string_amount():
    payload = {"amount": "100"}
    response = requests.post(f"{BASE_URL}/wallet/add", json=payload, headers=VALID_HEADERS)

    # Amount should be numeric, not string
    assert response.status_code == 400


# ---------------------------
# 🔹 REVIEWS
# ---------------------------

def test_review_invalid_rating():
    payload = {"rating": 10, "comment": "Bad"}
    response = requests.post(f"{BASE_URL}/products/1/reviews", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


# ---------------------------
# 🔹 SUPPORT TICKETS
# ---------------------------

def test_ticket_invalid_subject():
    payload = {"subject": "Hi", "message": "Help me"}
    response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


# ---------------------------
# 🔹 ADDITIONAL NEGATIVE CASES
# ---------------------------

def test_add_to_cart_missing_product_id():
    payload = {"quantity": 1}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_add_to_cart_non_integer_quantity():
    payload = {"product_id": 1, "quantity": "two"}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_coupon_missing_code_field():
    payload = {}
    response = requests.post(f"{BASE_URL}/coupon/apply", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_wallet_add_negative_amount():
    payload = {"amount": -50}
    response = requests.post(f"{BASE_URL}/wallet/add", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_wallet_add_missing_amount_field():
    payload = {}
    response = requests.post(f"{BASE_URL}/wallet/add", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_wallet_pay_missing_amount_field():
    payload = {}
    response = requests.post(f"{BASE_URL}/wallet/pay", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_wallet_pay_negative_amount():
    payload = {"amount": -10}
    response = requests.post(f"{BASE_URL}/wallet/pay", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_review_missing_rating():
    payload = {"comment": "Nice product"}
    response = requests.post(f"{BASE_URL}/products/1/reviews", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_review_missing_comment_field():
    payload = {"rating": 4}
    response = requests.post(f"{BASE_URL}/products/1/reviews", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


def test_ticket_missing_message_field():
    payload = {"subject": "Order issue"}
    response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=VALID_HEADERS)

    assert response.status_code == 400


# ---------------------------
# 🔹 EXTRA COVERAGE CASES
# ---------------------------


def test_add_to_cart_missing_quantity_field():
    payload = {"product_id": 1}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)

    # Missing required quantity should be treated as bad request
    assert response.status_code == 400


def test_add_to_cart_float_quantity():
    payload = {"product_id": 1, "quantity": 1.5}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)

    # Quantity should be an integer count of items
    assert response.status_code == 400


def test_checkout_missing_payment_method_field():
    payload = {}
    response = requests.post(f"{BASE_URL}/checkout", json=payload, headers=VALID_HEADERS)

    # Checkout without specifying a payment method should fail
    assert response.status_code == 400


def test_checkout_non_json_body():
    response = requests.post(f"{BASE_URL}/checkout", data="not-json", headers=VALID_HEADERS)
    # Non-JSON body should be rejected with a 4xx, not processed as valid checkout
    assert response.status_code == 400


def test_review_non_integer_rating():
    payload = {"rating": "five", "comment": "Text rating"}
    response = requests.post(f"{BASE_URL}/products/1/reviews", json=payload, headers=VALID_HEADERS)

    # Rating must be numeric; wrong type should be rejected
    assert response.status_code == 400


def test_review_blank_comment():
    payload = {"rating": 4, "comment": "   "}
    response = requests.post(f"{BASE_URL}/products/1/reviews", json=payload, headers=VALID_HEADERS)

    # Comment with only whitespace should be treated as invalid
    assert response.status_code == 400


def test_support_ticket_valid_payload_creates_ticket():
    payload = {
        "subject": "Order #12345 delayed delivery",
        "message": "My order is delayed by more than 3 days. Please help."
    }
    response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=VALID_HEADERS)

    # A well-formed ticket should succeed with a 2xx code
    assert response.status_code in [200, 201]

    # Response should be JSON with at least an ID or subject echoed back
    data = response.json()
    assert isinstance(data, dict)
    assert any(key in data for key in ["ticket_id", "id", "subject"])