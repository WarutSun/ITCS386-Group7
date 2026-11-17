
import requests

BASE_URL = "http://157.85.102.236/shop/wp-json/wc/store/v1"
PRODUCT_ID = 778


# Goal: Verify that a valid product can be added to cart.
def test_add_valid_product():
    session = requests.Session()

    try:
        # Step 1: Create a fresh cart session
        cart_response = session.get(
            f"{BASE_URL}/cart",
            timeout=15
        )

        assert cart_response.status_code == 200

        # Step 2: Get Cart-Token
        token = cart_response.headers.get("Cart-Token")

        assert token is not None, "Cart-Token missing"

        session.headers.update({
            "Cart-Token": token
        })

        # Step 3: Add product to cart
        response = session.post(
            f"{BASE_URL}/cart/add-item",
            json={
                "id": PRODUCT_ID,
                "quantity": 2
            },
            timeout=15
        )

        # Step 4: Verify HTTP status
        assert response.status_code == 201, response.text

        # Step 5: Verify response data
        data = response.json()

        items = [
            item for item in data["items"]
            if int(item["id"]) == PRODUCT_ID
        ]

        assert len(items) == 1
        assert items[0]["quantity"] == 2
        
        # Verify cart total: 2 items x 100 THB
        assert data["totals"]["total_items"] == "20000"
        assert data["items_count"] == 2

        print("Product added successfully!")
        print("Product ID:", PRODUCT_ID)
        print("Quantity:", items[0]["quantity"])

    finally:
        session.close()
        
# Goal: Verify API rejects a missing product ID.
def test_add_missing_product_id():
    session = requests.Session()

    try:
        # Step 1: Create a fresh cart
        cart_response = session.get(
            f"{BASE_URL}/cart",
            timeout=15
        )

        assert cart_response.status_code == 200

        token = cart_response.headers.get("Cart-Token")
        assert token, "Cart-Token missing"

        session.headers.update({
            "Cart-Token": token
        })

        # Step 2: Send request without product ID
        response = session.post(
            f"{BASE_URL}/cart/add-item",
            json={
                "quantity": 1
            },
            timeout=15
        )

        print("HTTP Status:", response.status_code)
        print("Response:", response.text[:500])

        # Step 3: Verify API rejects invalid input
        assert 400 <= response.status_code < 500

        error = response.json()
        assert "code" in error
        assert "message" in error

        # Step 4: Verify cart remains empty
        verify_response = session.get(
            f"{BASE_URL}/cart",
            timeout=15
        )

        assert verify_response.status_code == 200
        assert verify_response.json()["items_count"] == 0

    finally:
        session.close()

