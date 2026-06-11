import re

seen = set()
msg = []

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 4:
            continue

        m = re.search(r'([A-Z_])(?:\.html)?$', parts[3])

        if m:
            ch = m.group(1)

            if ch not in seen:
                seen.add(ch)
                msg.append(ch)

print("".join(msg))