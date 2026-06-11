target_ip = "201.5.9.64"

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if target_ip in line:
            print(line.strip())