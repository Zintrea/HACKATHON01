from collections import Counter

urls = Counter()

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) >= 5 and parts[4] in ("500", "504"):
            urls[parts[3]] += 1

for url, count in urls.most_common(50):
    print(f"{count:>10}  {url}")