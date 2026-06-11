from collections import defaultdict
import re

first_seen = {}
count = defaultdict(int)

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]
        if len(parts) < 4:
            continue

        t = parts[0]
        url = parts[3]

        m = re.search(r'([A-Z_])(?:\.html)?$', url)
        if not m:
            continue

        c = m.group(1)

        count[c] += 1
        if c not in first_seen:
            first_seen[c] = t

# combine score = first_seen order + frequency
sorted_chars = sorted(first_seen.keys(), key=lambda c: (first_seen[c], -count[c]))

print("".join(sorted_chars))