
import requests

# WooCommerce Store API ของกลุ่ม 7
BASE_URL = "http://157.85.102.236/shop/wp-json/wc/store/v1"

print("Connecting to WooCommerce API...")

try:
    response = requests.get(
        f"{BASE_URL}/products",
        params={"per_page": 5},
        timeout=15
    )

    print("HTTP Status:", response.status_code)

    if response.status_code == 200:
        products = response.json()

        print("Connection successful!")
        print("Products returned:", len(products))

        for product in products:
            print(
                "ID:", product.get("id"),
                "| Name:", product.get("name")
            )
    else:
        print("API returned an error.")
        print(response.text[:500])

except requests.exceptions.RequestException as error:
    print("Connection failed!")
    print(error)
