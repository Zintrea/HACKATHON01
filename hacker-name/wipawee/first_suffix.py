bases = [
    "/search",
    "/checkout",
    "/products",
    "/cart",
    "/api/v1/user",
    "/index.html"
]

seen = []

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 4:
            continue

        path = parts[3]

        for base in bases:
            if path.startswith(base) and path != base:

                extra = path[len(base):]

                if len(extra) == 1 and extra not in seen:
                    seen.append(extra)

for s in seen:
    print(s)