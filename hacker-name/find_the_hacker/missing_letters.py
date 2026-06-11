import re

wanted = {"H","J","K","Q"}

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]
        if len(parts) < 4:
            continue

        url = parts[3]

        for ch in wanted:
            if ch in url:
                print(line.strip())
                break