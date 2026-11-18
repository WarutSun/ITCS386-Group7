import { shopperFlow } from './workload.js';

export const options = {
  stages: [
    { duration: '5s', target: 5 },
    { duration: '5s', target: 10 },
    { duration: '5s', target: 20 },
    { duration: '5s', target: 30 },
    { duration: '3s', target: 0 },
  ],
  thresholds: {
    http_req_failed:   ['rate<0.01'],
    http_req_duration: ['p(95)<1000'],
  },
};

export default function () { shopperFlow(); }