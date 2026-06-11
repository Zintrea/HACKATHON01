with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if "| 500 |" in line:
            print(line.strip())
            break