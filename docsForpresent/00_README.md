# H1 Dorm — ฐานความเข้าใจสำหรับภารกิจวิเคราะห์ Log

> เป้าหมายของโฟลเดอร์นี้: ทำให้ใบเข้าใจโจทย์ H1 แบบลึกพอที่จะ **สอนทีม**, **อธิบายกรรมการ**, และ **ต่อยอดเป็นสคริปต์ + Dashboard** ได้ โดยไม่ต้องไล่อ่าน log ทั้งไฟล์แบบ manual

## ใช้โฟลเดอร์นี้ยังไง

อ่านตามลำดับนี้:

1. `01_Mission-Understanding/mission-summary.md` — เข้าใจโจทย์จริง ๆ ว่าเขาถามอะไร
2. `02_Log-Understanding/log-format-explained.md` — เข้าใจข้อมูลใน `cart_web.log`
3. `02_Log-Understanding/normal-user-vs-attacker.md` — แยก user ปกติ vs attacker แบบมีเหตุผล
4. `03_Analysis-Strategy/investigation-framework.md` — วิธีคิดแบบนักสืบ log
5. `03_Analysis-Strategy/suspicion-scoring-model.md` — เปลี่ยน red flags เป็นคะแนน
6. `03_Analysis-Strategy/incident-timeline-method.md` — หา WHEN & HOW
7. `03_Analysis-Strategy/hidden-bonus-hunting.md` — หา hidden bonus / ชื่อจริงคนร้าย
8. `06_Dashboard-Planning/dashboard-layout.md` — ออกแบบ Dashboard
9. `05_Presentation-Prep/likely-judge-questions.md` — เตรียมตอบกรรมการ
10. `99_Final-Checklist/before-presentation-checklist.md` — เช็กก่อนนำเสนอ

## กติกาสำคัญของงานนี้

โจทย์บอกชัดว่า:

> ห้ามใช้วิธี Manual ไล่อ่าน Log ทั้งไฟล์ เพราะอาจใช้เวลานานมาก จงเขียนสคริปต์เพื่อช่วยวิเคราะห์ข้อมูล และตามหาตัวคนร้ายให้ได้

ดังนั้นคำตอบที่ดีต้องมี 3 ชั้น:

| ชั้น | สิ่งที่ต้องมี | ตัวอย่าง |
|---|---|---|
| Analysis Logic | วิธีคิด/กฎที่ใช้ตัดสิน | red flags, scoring, timeline |
| Script / Reproducible Output | รันซ้ำได้ ไม่ใช่อ่านมั่ว | CSV, summary, dashboard data |
| Evidence | หลักฐานจาก log จริง | request examples, IP stats, incident window |

## หลักคิดสั้นที่สุด

เราไม่ได้ถามว่า “บรรทัดไหนดูแปลก” อย่างเดียว แต่ถามว่า:

1. **ใคร** มีพฤติกรรมโจมตีหลายอย่างพร้อมกัน
2. **เมื่อไหร่** ระบบเริ่มผิดปกติ / หน่วง / ล่ม
3. **โจมตียังไง** ผ่าน path, payload, status, rate pattern
4. **สื่อสารยังไง** ให้คนอื่นเห็นภาพผ่าน Dashboard
5. **มี clue ลับไหม** ที่คนร้ายทิ้งไว้ เช่น signature, username, path แปลก, encoded message

## สิ่งที่ไม่ทำใน Dorm

- ไม่ทำเป็น lab แบบแบบฝึกหัด เพราะ H1 เองคือ lab/โจทย์แข่งขัน
- ไม่แตะหรือแก้ `cart_web.log`
- ไม่ claim สิ่งที่ log ไม่มี เช่น response time จริง ถ้าไม่มี field response time

## สิ่งที่ Dorm ให้แทน

- concept ลึก
- example ให้เห็นภาพ
- framework สำหรับคิดต่อ
- template สำหรับทำ script/dashboard/report
- คำถามกรรมการที่ควรเตรียมตอบ
