from collections import defaultdict
import re

data = defaultdict(set)

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) >= 4:
            ip = parts[1]
            url = parts[3]

            m = re.search(r'([A-Z_])(?:\.html)?$', url)

            if m:
                data[ip].add(m.group(1))

for ip, chars in data.items():
    if chars:
        print(ip, "".join(sorted(chars)))