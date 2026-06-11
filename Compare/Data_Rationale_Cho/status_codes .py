status_codes = set()

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = line.split("|")

        if len(parts) >= 6:
            status_codes.add(parts[4].strip())

print(sorted(status_codes))