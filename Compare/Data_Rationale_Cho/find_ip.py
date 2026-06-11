import re
from collections import defaultdict

# เก็บ endpoint ไม่ซ้ำ
endpoints = set()

# อ่านไฟล์ log
with open("cart_web.log", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = line.split("|")

        if len(parts) >= 6:
            endpoint = parts[3].strip()
            endpoints.add(endpoint)

# จัดกลุ่ม endpoint
groups = defaultdict(list)

for endpoint in sorted(endpoints):

    # เช่น /cartA -> /cart
    #      /searchB -> /search
    #      /indexA.html -> /index.html
    base = re.sub(r'[A-Z_]+(?=(\.html)?$)', '', endpoint)

    groups[base].append(endpoint)

# แสดงผล
for group in groups.values():
    print(group)

input("\nกด Enter เพื่อปิด...")