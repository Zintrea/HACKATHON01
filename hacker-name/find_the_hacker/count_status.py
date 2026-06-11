from collections import Counter

c = Counter()

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]
        if len(parts) >= 5:
            c[parts[4]] += 1

for status, count in sorted(c.items()):
    print(status, count)