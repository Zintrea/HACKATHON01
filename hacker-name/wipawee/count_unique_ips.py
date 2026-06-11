# count_unique_ips.py

ips = set()

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) >= 6:
            ips.add(parts[1])

print("Unique IPs:", len(ips))