import re
from collections import defaultdict

letters = defaultdict(set)

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 4:
            continue

        ip = parts[1]
        url = parts[3]

        m = re.search(r'([A-Z_])(?:\.html)?$', url)

        if m:
            letters[ip].add(m.group(1))

for ip in sorted(letters):
    print(ip, "".join(sorted(letters[ip])))