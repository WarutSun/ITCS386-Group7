import requests

BASE = "http://157.85.102.236/shop/wp-json/wc/store/v1"

# Goal: per_page=5 returns 200 and at most 5 products with required fields
def test_per_page_5():
    r = requests.get(f"{BASE}/products", params={"per_page": 5}, timeout=15)
    assert r.status_code == 200
    items = r.json()
    assert 1 <= len(items) <= 5
    for p in items:
        assert {"id", "name", "prices", "is_in_stock", "categories"} <= p.keys()