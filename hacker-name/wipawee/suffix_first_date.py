bases = [
    "/search",
    "/checkout",
    "/products",
    "/cart",
    "/api/v1/user",
    "/index.html"
]

first_seen = {}

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 4:
            continue

        timestamp = parts[0]
        path = parts[3]

        for base in bases:
            if path.startswith(base) and path != base:

                extra = path[len(base):]

                if len(extra) == 1:
                    if extra not in first_seen:
                        first_seen[extra] = timestamp

for suffix, date in sorted(first_seen.items(), key=lambda x: x[1]):
    print(date, suffix)