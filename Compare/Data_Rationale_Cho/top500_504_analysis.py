from collections import Counter, defaultdict
import pandas as pd

# เก็บจำนวน Error ต่อ IP
ip_total = {
    "500": Counter(),
    "504": Counter()
}

# เก็บ Endpoint + Method ต่อ IP
ip_endpoint = {
    "500": defaultdict(Counter),
    "504": defaultdict(Counter)
}

print("กำลังอ่าน log...")

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:

    for line in f:

        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 6:
            continue

        ip = parts[1]
        method = parts[2]
        endpoint = parts[3]
        status = parts[4]

        if status not in ("500", "504"):
            continue

        ip_total[status][ip] += 1

        key = f"{endpoint} | {method}"
        ip_endpoint[status][ip][key] += 1

print("อ่าน log เสร็จ")

# ===== Export Excel =====

with pd.ExcelWriter("Error_IP_Analysis.xlsx", engine="openpyxl") as writer:

    for status in ("500", "504"):

        rows = []

        for ip, total_count in ip_total[status].most_common(100):

            for endpoint_method, endpoint_count in ip_endpoint[status][ip].most_common():

                endpoint, method = endpoint_method.split(" | ")

                rows.append([
                    status,
                    ip,
                    total_count,
                    endpoint,
                    method,
                    endpoint_count
                ])

        df = pd.DataFrame(
            rows,
            columns=[
                "Status",
                "IP",
                "Count",
                "Endpoint",
                "Method",
                "Endpoint Count"
            ]
        )

        df = df.sort_values(
            by=["Count", "Endpoint Count"],
            ascending=[False, False]
        )

        df.to_excel(
            writer,
            sheet_name=f"Error_{status}",
            index=False
        )

print("สร้างไฟล์ Error_IP_Analysis.xlsx เรียบร้อย")

input("\nกด Enter เพื่อปิด...")