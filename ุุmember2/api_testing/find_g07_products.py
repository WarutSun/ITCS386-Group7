
import requests

BASE_URL = "http://157.85.102.236/shop/wp-json/wc/store/v1"

print("Searching for Group 07 products...")

try:
    response = requests.get(
        f"{BASE_URL}/products",
        params={
            "search": "G07",
            "per_page": 100
        },
        timeout=15
    )

    print("HTTP Status:", response.status_code)

    response.raise_for_status()
    products = response.json()

    print("Products found:", len(products))

    for product in products:
        print("---------------------------")
        print("ID:", product.get("id"))
        print("Name:", product.get("name"))
        print("Price:", product.get("prices", {}).get("price"))
        print("Purchasable:", product.get("is_purchasable"))
        print("In Stock:", product.get("is_in_stock"))

except requests.exceptions.RequestException as error:
    print("Request failed:", error)
