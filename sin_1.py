from collections import defaultdict, Counter
import csv

# -------------------------
# สรุปสถิติราย IP
# -------------------------

ip_stats = defaultdict(lambda: {
    "requests": 0,
    "404": 0,
    "500": 0,
    "504": 0
})

paths = Counter()
error_paths = Counter()
methods = Counter()

print("Reading log file...")

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 5:
            continue

        ip = parts[1]
        method = parts[2]
        path = parts[3]
        status = parts[4]

        # สถิติราย IP
        ip_stats[ip]["requests"] += 1

        if status == "404":
            ip_stats[ip]["404"] += 1

        elif status == "500":
            ip_stats[ip]["500"] += 1

        elif status == "504":
            ip_stats[ip]["504"] += 1

        # สถิติรวม
        methods[method] += 1
        paths[path] += 1

        if status in ["404", "500", "504"]:
            error_paths[path] += 1

print("Finished reading log.")

# -------------------------
# Ranking IP
# -------------------------

ranking = sorted(
    ip_stats.items(),
    key=lambda x:
        x[1]["404"] +
        x[1]["500"] +
        x[1]["504"],
    reverse=True
)

# -------------------------
# Export IP Summary
# -------------------------

with open("ip_summary.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "ip",
        "requests",
        "404",
        "500",
        "504",
        "score"
    ])

    for ip, stats in ranking:

        score = (
            stats["404"]
            + stats["500"]
            + stats["504"]
        )

        writer.writerow([
            ip,
            stats["requests"],
            stats["404"],
            stats["500"],
            stats["504"],
            score
        ])

# -------------------------
# Export Top Paths
# -------------------------

with open("path_summary.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "path",
        "requests"
    ])

    for path, count in paths.most_common():
        writer.writerow([path, count])

# -------------------------
# Export Error Paths
# -------------------------

with open("error_path_summary.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "path",
        "errors"
    ])

    for path, count in error_paths.most_common():
        writer.writerow([path, count])

# -------------------------
# Export Methods
# -------------------------

with open("method_summary.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "method",
        "count"
    ])

    for method, count in methods.most_common():
        writer.writerow([method, count])

# -------------------------
# Show Top 10
# -------------------------

print("\n=== TOP 10 SUSPICIOUS IP ===")

for ip, stats in ranking[:10]:
    score = (
        stats["404"]
        + stats["500"]
        + stats["504"]
    )

    print(
        ip,
        "Requests:", stats["requests"],
        "404:", stats["404"],
        "500:", stats["500"],
        "504:", stats["504"],
        "Score:", score
    )

print("\nFiles created:")
print("- ip_summary.csv")
print("- path_summary.csv")
print("- error_path_summary.csv")
print("- method_summary.csv")

from datetime import datetime

target_ip = "209.103.8.44"
errors = {"404", "500", "504"}

logs = []

with open("cart_web.log", "r", encoding="utf-8") as f:
    for line in f:
        parts = [x.strip() for x in line.split("|")]

        if len(parts) != 6:
            continue

        dt, ip, method, endpoint, status, response_time = parts

        if ip == target_ip and status in errors:
            logs.append(
                (
                    datetime.strptime(dt, "%Y-%m-%d %H:%M:%S"),
                    ip,
                    method,
                    endpoint,
                    status,
                    response_time
                )
            )

logs.sort(key=lambda x: x[0])

for log in logs:
    print(
        f"{log[0]} | {log[1]} | {log[2]} | "
        f"{log[3]} | {log[4]} | {log[5]}"
    )