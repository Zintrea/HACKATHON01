from collections import Counter

sus_ips = Counter()

base_paths = {
    "/search",
    "/checkout",
    "/products",
    "/cart",
    "/api/v1/user",
    "/index.html"
}

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) >= 4:
            ip = parts[1]
            path = parts[3]

            if path not in base_paths:
                sus_ips[ip] += 1

print("\nTop suspicious IPs:")
for ip, count in sus_ips.most_common(20):
    print(ip, count)