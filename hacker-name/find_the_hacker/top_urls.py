from collections import Counter

urls = Counter()

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]
        if len(parts) >= 4:
            urls[parts[3]] += 1

for url, count in urls.most_common(50):
    print(count, url)