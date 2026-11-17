
import requests

BASE_URL = "http://157.85.102.236/shop/wp-json/wc/store/v1"

print("Connecting to WooCommerce Cart API...")

try:
    response = requests.get(
        f"{BASE_URL}/cart",
        timeout=15
    )

    print("HTTP Status:", response.status_code)

    token = response.headers.get("Cart-Token")

    if response.status_code == 200:
        print("Cart API connection successful!")

        if token:
            print("Cart Token received: YES")
            print("Token length:", len(token))
        else:
            print("Cart Token received: NO")

        data = response.json()

        print("Items in cart:", len(data.get("items", [])))
        print("Cart response keys:", list(data.keys()))

    else:
        print("Cart API returned an error.")
        print(response.text[:500])

except requests.exceptions.RequestException as error:
    print("Connection failed:", error)
