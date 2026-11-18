import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE = 'http://157.85.102.236/shop/wp-json/wc/store/v1';

// ตัวแปรนอกฟังก์ชัน: แต่ละ VU มีสำเนาของตัวเอง = ตั๋วตะกร้าของ VU คนนั้น
let token = null;

export function shopperFlow() {
  // 0. ขอตั๋วตะกร้าครั้งเดียวต่อ VU
  if (!token) {
    token = http.get(`${BASE}/cart`).headers['Cart-Token'];
  }
  const headers = { 'Content-Type': 'application/json', 'Cart-Token': token };

  // 1. เปิดรายการสินค้า
  const list = http.get(`${BASE}/products?per_page=20&type=simple`);
  check(list, { 'list: 200': (r) => r.status === 200 });
  sleep(1);

  // 2. ค้นหา
  const search = http.get(`${BASE}/products?search=beanie`);
  check(search, { 'search: 200': (r) => r.status === 200 });
  sleep(1);

  // 3. เลือกสินค้าที่ซื้อได้และมีของ
  const items = list.json().filter((p) => p.is_purchasable && p.is_in_stock);
  if (items.length === 0) return;
  const p = items[Math.floor(Math.random() * items.length)];

  // 4. ใส่ตะกร้า
  const add = http.post(`${BASE}/cart/add-item`,
    JSON.stringify({ id: p.id, quantity: 1 }), { headers });
  check(add, { 'add-item: 200/201': (r) => r.status === 200 || r.status === 201 });
  sleep(1);

  // 5. เอาออกจากตะกร้า (ไม่ให้ตะกร้าสะสมจนเกิน stock)
  if (add.status === 200 || add.status === 201) {
    const key = add.json().items.find((i) => i.id === p.id).key;
    http.post(`${BASE}/cart/remove-item`, JSON.stringify({ key }), { headers });
  }
}