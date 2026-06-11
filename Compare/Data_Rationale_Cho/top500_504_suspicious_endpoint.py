from collections import Counter, defaultdict
import pandas as pd
import re

# เก็บข้อมูล
ip_total = {
    "500": Counter(),
    "504": Counter()
}

endpoint_data = {
    "500": defaultdict(dict),
    "504": defaultdict(dict)
}

print("กำลังอ่าน log...")

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:

    for line in f:

        parts = [x.strip() for x in line.split("|")]

        if len(parts) < 6:
            continue

        timestamp = parts[0]
        ip = parts[1]
        method = parts[2]
        endpoint = parts[3]
        status = parts[4]

        try:
            response_time = int(parts[5])
        except:
            response_time = 0

        # เอาเฉพาะ 500 / 504
        if status not in ("500", "504"):
            continue

        # เอาเฉพาะ endpoint ที่ลงท้าย A-Z หรือ _
        if not re.search(r'[A-Z_]+(?=(\.html)?$)', endpoint):
            continue

        ip_total[status][ip] += 1

        key = (ip, endpoint, method)

        if key not in endpoint_data[status]:
            endpoint_data[status][key] = {
                "Timestamp": timestamp,
                "Response Time": response_time,
                "Count": 0
            }

        endpoint_data[status][key]["Count"] += 1

print("อ่าน log เสร็จ")

output_file = "Suspicious_500_504.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    for status in ("500", "504"):

        rows = []

        # Top 100 IP
        top_ips = {
            ip
            for ip, count
            in ip_total[status].most_common(100)
        }

        for (ip, endpoint, method), info in endpoint_data[status].items():

            if ip not in top_ips:
                continue

            rows.append([
                info["Timestamp"],
                ip,
                method,
                endpoint,
                status,
                info["Response Time"],
                info["Count"]
            ])

        df = pd.DataFrame(
            rows,
            columns=[
                "Timestamp",
                "IP",
                "Method",
                "Endpoint",
                "Status",
                "Response Time",
                "Endpoint Count"
            ]
        )

        if not df.empty:
            df = df.sort_values(
                by=["Endpoint Count"],
                ascending=False
            )

        df.to_excel(
            writer,
            sheet_name=f"Error_{status}",
            index=False
        )

        print(f"สร้าง Sheet Error_{status}")

print(f"\nสร้างไฟล์ {output_file} เรียบร้อย")

input("\nกด Enter เพื่อปิด...")