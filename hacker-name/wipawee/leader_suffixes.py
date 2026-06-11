from collections import defaultdict

leaders = defaultdict(set)

with open("cart_web.log","r",encoding="utf-8") as f:
    for line in f:

        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 4:
            continue

        ip = parts[1]
        path = parts[3]

        bases = [
            "/search",
            "/cart",
            "/products",
            "/checkout",
            "/api/v1/user",
            "/index.html"
        ]

        for base in bases:

            if path.startswith(base) and path != base:

                suffix = path[len(base):]

                if len(suffix) == 1:
                    leaders[ip].add(suffix)

for ip, suffixes in sorted(
        leaders.items(),
        key=lambda x: len(x[1]),
        reverse=True)[:20]:

    print(ip, len(suffixes), "".join(sorted(suffixes)))