from collections import Counter

urls = Counter()

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]
        if len(parts) >= 4:
            url = parts[3]

            if url not in [
                "/search",
                "/checkout",
                "/products",
                "/index.html",
                "/cart",
                "/api/v1/user"
            ]:
                urls[url] += 1

for url, count in urls.most_common(100):
    print(count, url)