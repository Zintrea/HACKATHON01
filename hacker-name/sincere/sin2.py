from collections import Counter

target_ip = "209.103.8.44"

endpoints = Counter()

with open("cart_web.log", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) != 6:
            continue

        ip = parts[1]
        endpoint = parts[3]

        if ip == target_ip:
            endpoints[endpoint] += 1

print("Top endpoints for", target_ip)
for ep, count in endpoints.most_common(20):
    print(count, ep)