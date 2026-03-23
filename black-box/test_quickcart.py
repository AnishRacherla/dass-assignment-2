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
# ---------------------------
# 🔹 PROFILE
# ---------------------------

def test_profile_update_short_name():
    payload = {"name": "A", "phone": "1234567890"}
    response = requests.put(f"{BASE_URL}/profile", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_profile_update_invalid_phone():
    payload = {"name": "Valid Name", "phone": "123456789"} # 9 digits
    response = requests.put(f"{BASE_URL}/profile", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_profile_update_valid():
    payload = {"name": "John Doe", "phone": "1234567890"}
    response = requests.put(f"{BASE_URL}/profile", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 200

# ---------------------------
# 🔹 ADDRESSES
# ---------------------------

def test_address_add_invalid_label():
    payload = {
        "label": "INVALID_LABEL",
        "street": "123 Main St",
        "city": "Metropolis",
        "pincode": "123456"
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_address_add_short_street():
    payload = {
        "label": "HOME",
        "street": "123", # < 5
        "city": "Metropolis",
        "pincode": "123456"
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_address_add_invalid_pincode():
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "city": "Metropole",
        "pincode": "12345" # < 6 digits
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_address_update_illegal_field_city():
    # Fetch an ID first (assuming user 1 has at least 1 address)
    resp = requests.get(f"{BASE_URL}/addresses", headers=VALID_HEADERS)
    if resp.status_code == 200 and len(resp.json()) > 0:
        addr_id = resp.json()[0]["address_id"]
        # Try to modify city which is forbidden
        payload = {"city": "New City", "street": "Brand New Street"}
        put_resp = requests.put(f"{BASE_URL}/addresses/{addr_id}", json=payload, headers=VALID_HEADERS)
        # Should not update the city or should throw 400
        assert put_resp.status_code in [400, 200]
        if put_resp.status_code == 200:
            assert put_resp.json()["address"]["city"] != "New City"

# ---------------------------
# 🔹 LOYALTY POINTS
# ---------------------------

def test_loyalty_redeem_zero_points():
    payload = {"points": 0}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_loyalty_redeem_negative_points():
    payload = {"points": -5}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

# ---------------------------
# 🔹 ORDERS 
# ---------------------------

def test_order_cancel_non_existent():
    response = requests.post(f"{BASE_URL}/orders/99999/cancel", headers=VALID_HEADERS)
    assert response.status_code == 404

# ---------------------------
# 🔹 TICKETS
# ---------------------------

def test_ticket_create_short_subject():
    payload = {"subject": "abc", "message": "Valid long message."}
    response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_ticket_update_status_backward():
    # Try updating a non-existent ticket to CLOSED (expecting 404, not internal error)
    payload = {"status": "CLOSED"}
    response = requests.put(f"{BASE_URL}/support/tickets/99999", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 404


def test_loyalty_negative_balance():
    # Trying to redeem more points than what user has
    # User likely has 0 points
    payload = {"points": 99999}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_ticket_injection():
    # Potential SQL injection in message or subject
    payload = {"subject": "Test Ticket", "message": "' OR 1=1; DROP TABLE tickets; --"}
    response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=VALID_HEADERS)
    assert response.status_code in [200, 201]
    
def test_address_negative_pincode():
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "city": "Metropolis",
        "pincode": "-12345"
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_profile_empty_payload():
    response = requests.put(f"{BASE_URL}/profile", json={}, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_loyalty_float_points():
    payload = {"points": 10.5}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400


def test_loyalty_redeem_no_points_field():
    payload = {}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_address_missing_label():
    payload = {
        "street": "123 Main St",
        "city": "Metropolis",
        "pincode": "123456"
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_address_missing_street():
    payload = {
        "label": "HOME",
        "city": "Metropolis",
        "pincode": "123456"
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_address_missing_city():
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "pincode": "123456"
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_address_missing_pincode():
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "city": "Metropolis"
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_profile_update_missing_name():
    payload = {"phone": "1234567890"}
    response = requests.put(f"{BASE_URL}/profile", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_profile_update_missing_phone():
    payload = {"name": "John Doe"}
    response = requests.put(f"{BASE_URL}/profile", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_loyalty_point_redemption_exceeds_available():
    # User tries to redeem 1 point but doesn't have enough. (They might have 0)
    payload = {"points": 1}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    # The server might allow this or maybe it's returning a 400.
    assert response.status_code == 400
    
def test_ticket_update_status_invalid():
    payload = {"status": "INVALID_STATUS"}
    # Using 1 as we know there is a chance it exists. If not, it will be 404. Let's create one.
    ticket_payload = {"subject": "Need help", "message": "Can't find my order."}
    ticket_res = requests.post(f"{BASE_URL}/support/ticket", json=ticket_payload, headers=VALID_HEADERS)
    
    if ticket_res.status_code in [200, 201]:
        ticket_id = ticket_res.json().get("ticket_id")
        response = requests.put(f"{BASE_URL}/support/tickets/{ticket_id}", json=payload, headers=VALID_HEADERS)
        assert response.status_code == 400

def test_support_ticket_subject_too_long():
    long_subject = "A" * 105
    payload = {"subject": long_subject, "message": "My issue is detailed"}
    response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400
    
def test_checkout_invalid_payment_method():
    # We should have something in the cart
    requests.post(f"{BASE_URL}/cart/add", json={"product_id": 1, "quantity": 1}, headers=VALID_HEADERS)
    payload = {"payment_method": "INVALID"}
    response = requests.post(f"{BASE_URL}/checkout", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400
    
def test_order_history_empty_pagination():
    response = requests.get(f"{BASE_URL}/orders?page=-1", headers=VALID_HEADERS)
    assert response.status_code == 400
    
def test_loyalty_redeem_non_integer_points():
    payload = {"points": "two"}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_loyalty_redeem_boolean_points():
    payload = {"points": True}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_loyalty_redeem_empty_points():
    payload = {"points": ""}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_profile_update_long_name():
    # > 50 characters
    payload = {"name": "A" * 55, "phone": "1234567890"}
    response = requests.put(f"{BASE_URL}/profile", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_profile_update_non_string_name():
    payload = {"name": 123456, "phone": "1234567890"}
    response = requests.put(f"{BASE_URL}/profile", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_address_add_long_street():
    payload = {
        "label": "HOME",
        "street": "A" * 105, # > 100 characters
        "city": "Metropolis",
        "pincode": "123456"
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_ticket_add_long_message():
    # > 1000 characters
    payload = {"subject": "Need help", "message": "A" * 1050}
    response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_loyalty_redeem_very_large_points():
    payload = {"points": 99999999999999999999999}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_checkout_missing_payment_method():
    payload = {}
    response = requests.post(f"{BASE_URL}/checkout", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_wallet_balance_after_successful_checkout_cod():
    # Adding items + Checking out shouldn't deduct wallet money for COD
    # Get initial
    wallet_resp1 = requests.get(f"{BASE_URL}/wallet", headers=VALID_HEADERS)
    assert wallet_resp1.status_code == 200
    initial_bal = wallet_resp1.json()["balance"]

    # add to cart
    requests.post(f"{BASE_URL}/cart/add", json={"product_id": 1, "quantity": 1}, headers=VALID_HEADERS)
    # checkout COD
    response = requests.post(f"{BASE_URL}/checkout", json={"payment_method": "COD"}, headers=VALID_HEADERS)
    assert response.status_code in [200, 201]

    wallet_resp2 = requests.get(f"{BASE_URL}/wallet", headers=VALID_HEADERS)
    assert wallet_resp2.json()["balance"] == initial_bal

def test_order_history_invalid_page_type():
    response = requests.get(f"{BASE_URL}/orders?page=abc", headers=VALID_HEADERS)
    assert response.status_code == 400

def test_put_profile_without_name():
    payload = {"phone": "1314151617"}
    response = requests.put(f"{BASE_URL}/profile", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_delete_non_existent_address():
    response = requests.delete(f"{BASE_URL}/addresses/9999", headers=VALID_HEADERS)
    assert response.status_code == 404

def test_apply_coupon_empty_discount():
    payload = {"code": "NEW50", "discount_value": ""}
    response = requests.post(f"{BASE_URL}/coupons/apply", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_order_cancel_invalid_id_type():
    response = requests.post(f"{BASE_URL}/orders/abc/cancel", headers=VALID_HEADERS)
    assert response.status_code == 400

def test_apply_coupon_negative_discount():
    payload = {"code": "MYCOUPON", "discount_value": -10}
    response = requests.post(f"{BASE_URL}/coupons/apply", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_profile_update_phone_with_letters():
    payload = {"name": "Valid Name", "phone": "12345abcde"}
    response = requests.put(f"{BASE_URL}/profile", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_address_add_non_numeric_pincode():
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "city": "Metropolis",
        "pincode": "abcdef"
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_review_non_existent_product():
    payload = {"rating": 5, "comment": "Great!"}
    response = requests.post(f"{BASE_URL}/products/9999999/reviews", json=payload, headers=VALID_HEADERS)
    # The spec typically says 404 for related non-existent entities, or 400.
    assert response.status_code in [400, 404]

def test_review_integer_comment():
    payload = {"rating": 5, "comment": 12345}
    response = requests.post(f"{BASE_URL}/products/1/reviews", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_cart_add_boolean_quantity():
    payload = {"product_id": 1, "quantity": True}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_support_ticket_invalid_id_type():
    payload = {"status": "CLOSED"}
    response = requests.put(f"{BASE_URL}/support/tickets/abc", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400
def test_delete_cart_item_missing_auth():
    response = requests.delete(f"{BASE_URL}/cart/remove/1")
    assert response.status_code == 401

def test_delete_cart_item_invalid_product():
    response = requests.delete(f"{BASE_URL}/cart/remove/abc", headers=VALID_HEADERS)
    assert response.status_code == 400
def test_address_add_boolean_city():
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "city": True,
        "pincode": "123456"
    }
    response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_loyalty_redeem_boolean_points():
    payload = {"points": True}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_cart_add_negative_product_id():
    payload = {"product_id": -1, "quantity": 1}
    response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=VALID_HEADERS)
    assert response.status_code in [400, 404]

def test_review_negative_rating():
    payload = {"rating": -5, "comment": "Good"}
    response = requests.post(f"{BASE_URL}/products/1/reviews", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400
def test_products_invalid_page():
    response = requests.get(f"{BASE_URL}/products?page=abc", headers=VALID_HEADERS)
    assert response.status_code == 400

def test_loyalty_point_redemption_string():
    payload = {"points": "10"}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=VALID_HEADERS)
    assert response.status_code in [400, 200]

def test_delete_cart_item_missing_auth_header():
    response = requests.delete(f"{BASE_URL}/cart/remove/1")
    assert response.status_code == 401

def test_get_ticket_non_existent():
    response = requests.get(f"{BASE_URL}/support/tickets/999999", headers=VALID_HEADERS)
    assert response.status_code == 404

def test_update_ticket_non_existent():
    payload = {"status": "CLOSED"}
    response = requests.put(f"{BASE_URL}/support/tickets/999999", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 404

def test_reviews_empty_payload():
    response = requests.post(f"{BASE_URL}/products/1/reviews", json={}, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_checkout_invalid_type_payment():
    payload = {"payment_method": 1234}
    response = requests.post(f"{BASE_URL}/checkout", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400

def test_checkout_long_payment_method():
    payload = {"payment_method": "A" * 100}
    response = requests.post(f"{BASE_URL}/checkout", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400
