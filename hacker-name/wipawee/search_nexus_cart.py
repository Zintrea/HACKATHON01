from collections import Counter

weird = Counter()

bases = [
    "/search",
    "/checkout",
    "/products",
    "/cart",
    "/api/v1/user",
    "/index.html"
]

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 4:
            continue

        path = parts[3]

        normal = False
        for b in bases:
            if path == b:
                normal = True
                break

        if not normal:
            weird[path] += 1

print("Top 50 weird paths")
for path, count in weird.most_common(50):
    print(path, count)