from collections import defaultdict
import csv

stats = defaultdict(lambda: {
    "requests": 0,
    "GET": 0,
    "POST": 0,
    "200": 0,
    "404": 0,
    "500": 0,
    "504": 0
})

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 6:
            continue

        ip = parts[1]
        method = parts[2]
        status = parts[4]

        stats[ip]["requests"] += 1

        if method in ["GET", "POST"]:
            stats[ip][method] += 1

        if status in ["200", "404", "500", "504"]:
            stats[ip][status] += 1

with open("ip_behavior.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "ip",
        "requests",
        "GET",
        "POST",
        "200",
        "404",
        "500",
        "504"
    ])

    for ip, s in stats.items():
        writer.writerow([
            ip,
            s["requests"],
            s["GET"],
            s["POST"],
            s["200"],
            s["404"],
            s["500"],
            s["504"]
        ])

print("ip_behavior.csv created")