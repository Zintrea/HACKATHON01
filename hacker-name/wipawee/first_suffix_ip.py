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

        if len(parts) < 6:
            continue

        timestamp = parts[0]
        ip = parts[1]
        method = parts[2]
        path = parts[3]

        for base in bases:
            if path.startswith(base) and path != base:

                suffix = path[len(base):]

                if len(suffix) == 1:

                    if suffix not in first_seen:
                        first_seen[suffix] = (
                            timestamp,
                            ip,
                            method,
                            path
                        )

print("\n=== FIRST APPEARANCE OF EACH SUFFIX ===\n")

for suffix, data in sorted(
        first_seen.items(),
        key=lambda x: x[1][0]):

    timestamp, ip, method, path = data

    print(
        f"{suffix} | "
        f"{timestamp} | "
        f"{ip} | "
        f"{method} | "
        f"{path}"
    )