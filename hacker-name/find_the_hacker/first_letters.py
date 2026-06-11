import re

count = 0

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 4:
            continue

        url = parts[3]

        m = re.search(r'([A-Z_])(?:\.html)?$', url)

        if m:
            print(parts[0], m.group(1))
            count += 1

            if count >= 200:
                break