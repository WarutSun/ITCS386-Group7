import { shopperFlow } from '../../member5/performance_testing/workload.js';

// Average-load profile for Group 7.
//
// This file defines only the load profile.
// The user behavior itself is shared with Member 5 through workload.js.

export const options = {
  scenarios: {
    average_load: {
      executor: 'ramping-vus',

      stages: [
        // Warm up
        { duration: '30s', target: 5 },

        // Normal average load
        { duration: '2m', target: 10 },

        // Ramp down
        { duration: '30s', target: 0 },
      ],

      gracefulRampDown: '10s',
    },
  },

  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1000'],
  },
};

export default function () {
  shopperFlow();
}