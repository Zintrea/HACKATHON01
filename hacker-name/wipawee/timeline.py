first = None
last = None

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) >= 1:
            if first is None:
                first = parts[0]

            last = parts[0]

print("FIRST:", first)
print("LAST :", last)