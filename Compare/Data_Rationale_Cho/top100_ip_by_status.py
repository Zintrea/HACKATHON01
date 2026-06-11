from collections import defaultdict, Counter
import pandas as pd

# เก็บจำนวน IP แยกตาม Status Code
status_ip = defaultdict(Counter)

print("กำลังอ่านไฟล์ log...")

with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = line.split("|")

        if len(parts) >= 6:
            ip = parts[1].strip()
            status = parts[4].strip()

            status_ip[status][ip] += 1

print("อ่านไฟล์เสร็จ")

# สร้างไฟล์ Excel
excel_file = "Top100_IP_By_Status.xlsx"

with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:

    for status in sorted(status_ip.keys()):

        df = pd.DataFrame(
            status_ip[status].most_common(100),  # Top 100
            columns=["IP Address", "Count"]
        )

        # บันทึกลง Sheet
        df.to_excel(
            writer,
            sheet_name=f"Status_{status}",
            index=False
        )

        print(f"Status {status}: {len(df)} rows")

print(f"\nสร้างไฟล์ {excel_file} เรียบร้อย")
input("\nกด Enter เพื่อปิด...")