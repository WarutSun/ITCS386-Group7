import csv, sys
from collections import defaultdict

rows = []
with open(sys.argv[1], newline='') as f:
    for r in csv.DictReader(f):
        if r['metric_name'] == 'http_req_duration':
            rows.append((float(r['timestamp']), float(r['metric_value'])))

t0 = min(t for t, _ in rows)
buckets = defaultdict(list)
for t, v in rows:
    buckets[int((t - t0) // 30)].append(v)

def p95(xs):
    xs = sorted(xs)
    return xs[int(0.95 * (len(xs) - 1))]

for b in sorted(buckets):
    xs = buckets[b]
    print(f"{b*30:>4}-{b*30+30:<4}s  n={len(xs):<4} p95={p95(xs):7.0f} ms  max={max(xs):7.0f} ms")