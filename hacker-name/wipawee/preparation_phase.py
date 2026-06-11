suspects = {
    "209.103.8.44",
    "162.240.218.117",
    "197.82.237.190",
    "215.143.100.205",
    "199.242.130.73",
    "119.123.55.141",
    "148.9.19.27",
    "187.91.79.110",
    "196.45.2.86",
    "199.71.56.65",
    "14.121.165.122",
    "202.129.225.117",
    "211.92.75.1",
    "95.125.101.128",
    "14.252.124.193",
    "80.130.43.26",
    "139.94.203.41",
    "12.104.185.44",
    "131.33.12.73"
}

count = 0

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:

        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 4:
            continue

        timestamp = parts[0]
        ip = parts[1]

        if not timestamp.startswith("2024-06-13 10:"):
            continue

        if ip not in suspects:
            continue

        print(line.strip())

        count += 1

        if count >= 100:
            break