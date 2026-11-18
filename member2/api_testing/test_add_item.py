
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

# Goal: Verify API behavior when quantity is negative.
def test_add_negative_quantity():
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

        # Step 2: Try to add product with negative quantity
        response = session.post(
            f"{BASE_URL}/cart/add-item",
            json={
                "id": PRODUCT_ID,
                "quantity": -1
            },
            timeout=15
        )

        # Show actual server behavior
        print("HTTP Status:", response.status_code)
        print("Response:", response.text[:1000])

        # Step 3: Verify that invalid quantity is rejected
        assert response.status_code == 400

        error = response.json()

        assert "code" in error
        assert "message" in error

        # Step 4: Verify that nothing was added to the cart
        verify_response = session.get(
            f"{BASE_URL}/cart",
            timeout=15
        )

        assert verify_response.status_code == 200

        cart = verify_response.json()
        assert cart["items_count"] == 0

    finally:
        session.close()
        
# Goal: Verify API rejects quantity at the lower boundary value of zero.
def test_add_zero_quantity():
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

        # Step 2: Try to add product with quantity = 0
        response = session.post(
            f"{BASE_URL}/cart/add-item",
            json={
                "id": PRODUCT_ID,
                "quantity": 0
            },
            timeout=15
        )

        print("HTTP Status:", response.status_code)
        print("Response:", response.text[:1000])

        # Step 3: Verify zero quantity is rejected
        assert response.status_code == 400

        error = response.json()

        assert "code" in error
        assert "message" in error

        # Step 4: Verify the server reports an invalid quantity
        assert error["code"] == "woocommerce_rest_product_invalid_quantity"

        # Step 5: Verify nothing was added to the cart
        verify_response = session.get(
            f"{BASE_URL}/cart",
            timeout=15
        )

        assert verify_response.status_code == 200

        cart = verify_response.json()
        assert cart["items_count"] == 0

    finally:
        session.close()
        
# Goal: Verify API rejects a product ID that does not exist.
def test_add_nonexistent_product():
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

        # Step 2: Try to add a product that does not exist
        invalid_product_id = 99999999

        response = session.post(
            f"{BASE_URL}/cart/add-item",
            json={
                "id": invalid_product_id,
                "quantity": 1
            },
            timeout=15
        )

        print("HTTP Status:", response.status_code)
        print("Response:", response.text[:1000])

        # Step 3: Verify request is rejected
        assert response.status_code == 400

        error = response.json()

        assert "code" in error
        assert "message" in error

        # Step 4: Verify cart remains empty
        verify_response = session.get(
            f"{BASE_URL}/cart",
            timeout=15
        )

        assert verify_response.status_code == 200

        cart = verify_response.json()
        assert cart["items_count"] == 0

    finally:
        session.close()

# Goal: Verify API caps a quantity above the allowed maximum
# to the maximum allowed value.
def test_add_quantity_above_maximum():
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

        # Step 2: Get the product's current maximum quantity
        product_response = session.get(
            f"{BASE_URL}/products/{PRODUCT_ID}",
            timeout=15
        )

        assert product_response.status_code == 200

        product = product_response.json()

        maximum = product["add_to_cart"]["maximum"]
        requested_quantity = maximum + 1

        print("Maximum allowed:", maximum)
        print("Quantity requested:", requested_quantity)

        # Step 3: Request a quantity above the maximum
        response = session.post(
            f"{BASE_URL}/cart/add-item",
            json={
                "id": PRODUCT_ID,
                "quantity": requested_quantity
            },
            timeout=15
        )

        print("HTTP Status:", response.status_code)

        # Step 4: Verify the request succeeds
        assert response.status_code == 201

        data = response.json()

        item = next(
            item for item in data["items"]
            if int(item["id"]) == PRODUCT_ID
        )

        actual_quantity = item["quantity"]

        print("Quantity actually added:", actual_quantity)

        # Step 5: Verify WooCommerce caps quantity at maximum
        assert actual_quantity == maximum
        assert actual_quantity < requested_quantity

        # Verify the quantity limit reported in the cart
        assert item["quantity_limits"]["maximum"] == maximum

    finally:
        session.close()