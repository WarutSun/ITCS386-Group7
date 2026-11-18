import { shopperFlow } from './workload.js';

export const options = {
  stages: [
    { duration: '30s', target: 5 },   // ช่วงปกติ (baseline)
    { duration: '5s',  target: 20 },  // พุ่งขึ้นเร็ว
    { duration: '30s', target: 20 },  // ค้างที่ยอดพุ่ง
    { duration: '5s',  target: 5 },   // ลดลง
    { duration: '60s', target: 5 },   // ดู recovery
  ],
  thresholds: {
    http_req_failed:   ['rate<0.01'],
    http_req_duration: ['p(95)<1000'],
  },
};

export default function () { shopperFlow(); }