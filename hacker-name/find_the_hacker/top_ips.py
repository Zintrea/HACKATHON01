from collections import Counter

ip_counts = Counter()

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]
        if len(parts) >= 2:
            ip_counts[parts[1]] += 1

print("Top 20 IPs")
print("-" * 40)

for ip, count in ip_counts.most_common(20):
    print(f"{count:>10}  {ip}")