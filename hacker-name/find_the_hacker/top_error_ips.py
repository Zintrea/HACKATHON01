from collections import Counter

errors = Counter()

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) >= 5:
            status = parts[4]

            if status in ("500", "504"):
                errors[parts[1]] += 1

for ip, count in errors.most_common(20):
    print(f"{count:>10}  {ip}")