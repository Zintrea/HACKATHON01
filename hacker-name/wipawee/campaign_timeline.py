for word in ["nexus", "cart", "NEXUS_CART"]:
    found = 0

    with open("cart_web.log", "r", encoding="utf-8") as f:
        for line in f:
            if word in line:
                found += 1

    print(word, found)