import requests

BASE_URL = "http://157.85.102.236/shop/wp-json/wc/store/v1"
PRODUCT_ID = 778


# Goal: Verify an existing cart item's quantity can be updated.
def test_update_valid_quantity():
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

        # Step 2: Add the product to the cart first
        add_response = session.post(
            f"{BASE_URL}/cart/add-item",
            json={
                "id": PRODUCT_ID,
                "quantity": 1
            },
            timeout=15
        )

        assert add_response.status_code == 201, add_response.text

        add_data = add_response.json()

        item = next(
            item for item in add_data["items"]
            if int(item["id"]) == PRODUCT_ID
        )

        item_key = item["key"]

        print("Cart item key:", item_key)
        print("Original quantity:", item["quantity"])

        # Step 3: Update quantity from 1 to 3
        update_response = session.post(
            f"{BASE_URL}/cart/update-item",
            json={
                "key": item_key,
                "quantity": 3
            },
            timeout=15
        )

        print("HTTP Status:", update_response.status_code)
        print("Response:", update_response.text[:1000])

        # Step 4: Verify HTTP response
        assert update_response.status_code == 200

        data = update_response.json()

        updated_item = next(
            item for item in data["items"]
            if item["key"] == item_key
        )
        

        # Step 5: Verify important response fields
        assert int(updated_item["id"]) == PRODUCT_ID
        assert updated_item["quantity"] == 3

        print("Updated quantity:", updated_item["quantity"])

    finally:
        session.close()
        
# Goal: Verify API rejects an update request without a cart item key.
def test_update_missing_key():
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

        # Step 2: Send update request without item key
        response = session.post(
            f"{BASE_URL}/cart/update-item",
            json={
                "quantity": 3
            },
            timeout=15
        )

        print("HTTP Status:", response.status_code)
        print("Response:", response.text[:1000])

        # Step 3: Verify request is rejected
        assert 400 <= response.status_code < 500

        error = response.json()

        assert "code" in error
        assert "message" in error

        # Step 4: Verify fresh cart is still empty
        verify_response = session.get(
            f"{BASE_URL}/cart",
            timeout=15
        )

        assert verify_response.status_code == 200
        assert verify_response.json()["items_count"] == 0

    finally:
        session.close()

# Goal: Verify API rejects a cart item key that does not exist.
def test_update_invalid_key():
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

        # Step 2: Send an invalid cart item key
        response = session.post(
            f"{BASE_URL}/cart/update-item",
            json={
                "key": "invalid-cart-item-key",
                "quantity": 3
            },
            timeout=15
        )

        print("HTTP Status:", response.status_code)
        print("Response:", response.text[:1000])

        # Step 3: Verify request is rejected
        assert response.status_code == 409

        error = response.json()

        assert error["code"] == "woocommerce_rest_cart_invalid_key"
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
        
# Goal: Verify API rejects a negative quantity for an existing cart item.
def test_update_negative_quantity():
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

        # Step 2: Add a valid product first
        add_response = session.post(
            f"{BASE_URL}/cart/add-item",
            json={
                "id": PRODUCT_ID,
                "quantity": 1
            },
            timeout=15
        )

        assert add_response.status_code == 201

        add_data = add_response.json()

        item = next(
            item for item in add_data["items"]
            if int(item["id"]) == PRODUCT_ID
        )

        item_key = item["key"]

        print("Original quantity:", item["quantity"])

        # Step 3: Try to update to a negative quantity
        response = session.post(
            f"{BASE_URL}/cart/update-item",
            json={
                "key": item_key,
                "quantity": -1
            },
            timeout=15
        )

        print("HTTP Status:", response.status_code)
        print("Response:", response.text[:1000])

        # Step 4: Verify invalid quantity is rejected
        assert 400 <= response.status_code < 500

        error = response.json()

        assert "code" in error
        assert "message" in error

        # Step 5: Verify original cart item still exists
        verify_response = session.get(
            f"{BASE_URL}/cart",
            timeout=15
        )

        assert verify_response.status_code == 200

        cart = verify_response.json()

        existing_item = next(
            item for item in cart["items"]
            if item["key"] == item_key
        )

        print("Quantity after rejected update:",
              existing_item["quantity"])

        assert existing_item["quantity"] == 1

    finally:
        session.close()
        
# Goal: Verify API behavior when updating an existing cart item to zero.
def test_update_zero_quantity():
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

        # Step 2: Add one valid product
        add_response = session.post(
            f"{BASE_URL}/cart/add-item",
            json={
                "id": PRODUCT_ID,
                "quantity": 1
            },
            timeout=15
        )

        assert add_response.status_code == 201

        add_data = add_response.json()

        item = next(
            item for item in add_data["items"]
            if int(item["id"]) == PRODUCT_ID
        )

        item_key = item["key"]

        print("Original quantity:", item["quantity"])

        # Step 3: Update quantity to zero
        response = session.post(
            f"{BASE_URL}/cart/update-item",
            json={
                "key": item_key,
                "quantity": 0
            },
            timeout=15
        )

        print("HTTP Status:", response.status_code)
        print("Response:", response.text[:1000])

        # Exploratory assertion:
        # We expect either a successful cart operation
        # or a client-side validation response.
        assert response.status_code == 400

        error = response.json()

        assert error["code"] == "invalid_quantity"
        assert "message" in error

        # Step 4: Inspect final cart state
        verify_response = session.get(
            f"{BASE_URL}/cart",
            timeout=15
        )

        assert verify_response.status_code == 200

        cart = verify_response.json()

        matching_items = [
            item for item in cart["items"]
            if item["key"] == item_key
        ]

        if matching_items:
            print(
                "Item still exists. Quantity:",
                matching_items[0]["quantity"]
            )
        else:
            print("Item was removed from cart.")
        
        assert len(matching_items) == 1
        assert matching_items[0]["quantity"] == 1

    finally:
        session.close()
        
# UPDATE-06
# Goal: Verify API rejects a quantity above the allowed maximum
# and keeps the original cart quantity unchanged.
def test_update_quantity_above_maximum():
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

        # Step 2: Add one valid product to the cart
        add_response = session.post(
            f"{BASE_URL}/cart/add-item",
            json={
                "id": PRODUCT_ID,
                "quantity": 1
            },
            timeout=15
        )

        assert add_response.status_code == 201, add_response.text

        add_data = add_response.json()

        item = next(
            item for item in add_data["items"]
            if int(item["id"]) == PRODUCT_ID
        )

        item_key = item["key"]
        original_quantity = item["quantity"]
        maximum = item["quantity_limits"]["maximum"]
        requested_quantity = maximum + 1

        print("Original quantity:", original_quantity)
        print("Maximum allowed:", maximum)
        print("Quantity requested:", requested_quantity)

        # Step 3: Try to update above the maximum
        response = session.post(
            f"{BASE_URL}/cart/update-item",
            json={
                "key": item_key,
                "quantity": requested_quantity
            },
            timeout=15
        )

        print("HTTP Status:", response.status_code)
        print("Response:", response.text[:1000])

        # Step 4: Verify API rejects the request
        assert response.status_code == 400

        error = response.json()

        assert error["code"] == "invalid_quantity"
        assert "message" in error

        # Step 5: Read the same cart again
        verify_response = session.get(
            f"{BASE_URL}/cart",
            timeout=15
        )

        assert verify_response.status_code == 200

        cart = verify_response.json()

        updated_item = next(
            item for item in cart["items"]
            if item["key"] == item_key
        )

        print(
            "Quantity after rejected update:",
            updated_item["quantity"]
        )

        # Step 6: Verify original quantity did not change
        assert updated_item["quantity"] == original_quantity

    finally:
        session.close()