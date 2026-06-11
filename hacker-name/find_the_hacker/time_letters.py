import re

first_seen = {}

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]
        if len(parts) < 4:
            continue

        timestamp = parts[0]
        url = parts[3]

        m = re.search(r'([A-Z_])(?:\.html)?$', url)
        if not m:
            continue

        ch = m.group(1)

        # เก็บเฉพาะครั้งแรก
        if ch not in first_seen:
            first_seen[ch] = timestamp

# เรียงตามเวลา
for ch, t in sorted(first_seen.items(), key=lambda x: x[1]):
    print(ch, t)