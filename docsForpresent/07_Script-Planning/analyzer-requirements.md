# Analyzer Requirements — สคริปต์วิเคราะห์ควรทำอะไร

## เป้าหมาย

สร้าง analyzer ที่อ่าน `cart_web.log` แล้ว output ไฟล์พร้อมใช้สำหรับ report/dashboard

## Requirement หลัก

1. อ่านไฟล์ใหญ่แบบ streaming
2. parse fields 6 ช่อง
3. handle malformed lines
4. detect red flags
5. aggregate by IP
6. aggregate by minute
7. calculate suspicion score
8. export CSV/Markdown/JSON
9. เก็บ evidence examples
10. หา hidden bonus candidates

## Input

```text
H1/cart_web.log
```

## Output ที่แนะนำ

```text
output/
├── attacker_ips.csv
├── incident_windows.csv
├── traffic_timeline.csv
├── endpoint_summary.csv
├── suspicious_requests.csv
├── hidden_bonus_candidates.csv
├── h1_summary.md
└── dashboard_data.json
```

## Parser Rules

แต่ละบรรทัด split ด้วย:

```text
 | 
```

ต้องได้ 6 fields:

```text
timestamp, ip, method, endpoint, status, size
```

ถ้าไม่ได้ 6 fields:

- count เป็น malformed
- เก็บตัวอย่างไว้ ไม่ crash ทั้งโปรแกรม

## Performance Notes

เพราะ log ใหญ่มาก:

- ห้าม `read()` ทั้งไฟล์เข้า memory
- ใช้ loop ทีละ line
- เก็บ aggregate dict แทน raw rows ทั้งหมด
- suspicious_requests เก็บเฉพาะ top/sample ไม่ใช่ทุกบรรทัดถ้าเยอะมาก

## Config ที่ควรแยกได้

- high rate threshold
- score thresholds
- suspicious keywords
- sensitive endpoints
- max evidence lines per IP
- time bucket size

## Validation

หลังรันควรตอบได้:

- parsed lines = expected line count หรือใกล้เคียง
- malformed lines เท่าไหร่
- unique IPs เท่าไหร่
- status count รวมเท่ากับ parsed lines
- output files ถูกสร้างครบ
