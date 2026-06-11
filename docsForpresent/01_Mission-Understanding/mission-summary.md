# Mission Summary — ภารกิจ H1 ถามอะไรจริง ๆ

## โจทย์หลัก

เรามี log ขนาดใหญ่มากชื่อ `cart_web.log` และต้องใช้สคริปต์ช่วยวิเคราะห์เพื่อหาคำตอบ 4 ส่วน:

1. **WHO ARE THEY?** — IP Address ทั้งหมดของกลุ่มแฮกเกอร์
2. **WHEN & HOW?** — ระบบผิดปกติตอนไหน หน่วงตอนไหน ล่มตอนไหน และโดนโจมตียังไง
3. **TELL PEOPLE** — ทำ Web Application หรือ Dashboard ให้คนอื่นเข้าใจผลวิเคราะห์
4. **HIDDEN BONUS** — หา “ชื่อที่แท้จริงของคนร้าย” จาก clue ที่ซ่อนใน log

## ทำไมโจทย์ถึงห้ามอ่าน manual

เพราะ log มีจำนวนบรรทัดระดับหลายล้าน/หลายสิบล้าน การอ่านเองจะมีปัญหา:

| ปัญหา | ผลเสีย |
|---|---|
| ใช้เวลานาน | แข่งไม่ทัน |
| พลาดง่าย | มองไม่เห็น pattern ใหญ่ |
| ไม่ reproducible | กรรมการถามว่าทำซ้ำได้ไหมจะตอบยาก |
| ไม่มี evidence aggregation | บอกได้แค่ “เห็นแปลก ๆ” แต่พิสูจน์ไม่ได้ |

ดังนั้นวิธีที่ถูกคือ:

```text
เขียนสคริปต์ parse log
→ สร้าง metrics
→ ตรวจ red flags
→ รวมคะแนนต่อ IP
→ หา timeline
→ export CSV/JSON
→ แสดงบน Dashboard
```

## คำตอบที่กรรมการต้องการเห็น

ไม่ใช่แค่:

> IP นี้น่าสงสัย เพราะยิงเยอะ

แต่ต้องเป็น:

> IP นี้ถูกจัดเป็น high-confidence attacker เพราะมี request rate สูงผิดปกติ, มี 404 scanning หลาย endpoint, มี payload แบบ path traversal/SQL injection, และ activity อยู่ในช่วงเดียวกับ server error spike

## Output ที่ควรมีในท้ายงาน

| Output | ใช้ตอบภารกิจ |
|---|---|
| `attacker_ips.csv` | WHO ARE THEY |
| `incident_windows.csv` | WHEN |
| `suspicious_requests.csv` | HOW / Evidence |
| `endpoint_summary.csv` | HOW / Pattern |
| `hidden_bonus_findings.md` | HIDDEN BONUS |
| Dashboard | TELL PEOPLE |
| Final report/slides | นำเสนอกรรมการ |

## ประโยคแกนสำหรับนำเสนอ

> We did not manually inspect the log. We built a reproducible analysis pipeline that parses every request, extracts suspicious features, scores IP addresses, detects abnormal time windows, and visualizes the incident for non-technical users.
