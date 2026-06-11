from collections import Counter, defaultdict
import pandas as pd

# เก็บจำนวน Request ต่อ IP แยกตาม Status
ip_total = defaultdict(Counter)

# เก็บ Endpoint + Method ต่อ IP แยกตาม Status
ip_endpoint = defaultdict(lambda: defaultdict(Counter))

# หา Status Code ทั้งหมด
status_codes = set()

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

        status_codes.add(status)

        # จำนวน Request ทั้งหมดของ IP
        ip_total[status][ip] += 1

        # Endpoint + Method
        key = f"{endpoint} | {method}"
        ip_endpoint[status][ip][key] += 1

print("อ่าน log เสร็จ")
print("\nStatus Codes ที่พบ:")
print(sorted(status_codes))

# ===== Export Excel =====

output_file = "All_Status_Analysis.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    for status in sorted(status_codes):

        rows = []

        # Top 100 IP ของ Status นี้
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

        if not df.empty:
            df = df.sort_values(
                by=["Count", "Endpoint Count"],
                ascending=[False, False]
            )

        sheet_name = f"Status_{status}"

        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

        print(f"สร้าง Sheet: {sheet_name}")

print(f"\nสร้างไฟล์ {output_file} เรียบร้อย")

input("\nกด Enter เพื่อปิด...")