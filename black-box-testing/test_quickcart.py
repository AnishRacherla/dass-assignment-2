import requests
import pytest

BASE_URL = "http://localhost:8080/api/v1"

VALID_HEADERS = {
    "X-Roll-Number": "123",
    "X-User-ID": "1"
}

INVALID_ROLL_HEADERS = {
    "X-Roll-Number": "abc",
    "X-User-ID": "1"
}

NO_USER_HEADERS = {
    "X-Roll-Number": "123"
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


def test_invalid_product_id():
    response = requests.get(f"{BASE_URL}/products/999999", headers=VALID_HEADERS)
    assert response.status_code == 404


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


# ---------------------------
# 🔹 COUPONS
# ---------------------------

def test_apply_invalid_coupon():
    payload = {"code": "INVALID"}
    response = requests.post(f"{BASE_URL}/coupon/apply", json=payload, headers=VALID_HEADERS)

    # Could be 400 or inconsistent response
    assert response.status_code in [200, 400]

    # Try checking response format
    try:
        response.json()
    except:
        pytest.fail("Coupon response is not JSON → BUG")


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