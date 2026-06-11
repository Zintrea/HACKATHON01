import re
from collections import Counter

c = Counter()

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 4:
            continue

        m = re.search(r'([A-Z_])(?:\.html)?$', parts[3])

        if m:
            c[m.group(1)] += 1

for ch, count in c.most_common():
    print(f"{count:>10} {ch}")