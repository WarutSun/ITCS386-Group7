import { shopperFlow } from './workload.js';

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '3m',  target: 10 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_failed:   ['rate<0.01'],
    http_req_duration: ['p(95)<1000'],
  },
};

export default function () { shopperFlow(); }