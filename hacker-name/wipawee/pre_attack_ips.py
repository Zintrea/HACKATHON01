from collections import Counter

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

counts = Counter()

start = "2024-06-16 10:15"
end = "2024-06-16 10:25"

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 2:
            continue

        timestamp = parts[0]
        ip = parts[1]

        # เอาเฉพาะช่วง 10:15 ถึง 10:25 ก่อนเริ่ม N
        if timestamp.startswith(start) or timestamp.startswith(end):

            if ip in suspects:
                counts[ip] += 1

print("\nPre-Attack Activity\n")

for ip, count in counts.most_common():
    print(ip, count)