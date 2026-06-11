from collections import Counter

suffix = Counter()

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) >= 4:
            path = parts[3]

            base_paths = [
                "/search",
                "/checkout",
                "/products",
                "/cart",
                "/api/v1/user",
                "/index.html"
            ]

            for base in base_paths:
                if path.startswith(base) and path != base:
                    extra = path[len(base):]

                    if extra:
                        suffix[extra] += 1

print("\nSuffix ranking:")
for k, v in suffix.most_common():
    print(k, v)