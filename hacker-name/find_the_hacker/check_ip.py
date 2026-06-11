from collections import Counter

target_ip = "209.103.8.44"

urls = Counter()

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) >= 4 and parts[1] == target_ip:
            urls[parts[3]] += 1

for url, count in urls.most_common(20):
    print(count, url)