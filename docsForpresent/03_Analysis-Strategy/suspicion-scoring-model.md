# Suspicion Scoring Model — เปลี่ยน Red Flags เป็นคะแนน

## ทำไมต้อง scoring

ถ้าใช้กฎเดียว เช่น “มี 500 = hacker” จะ false positive ง่าย

Scoring ทำให้เรา:

- รวมหลายสัญญาณเข้าด้วยกัน
- อธิบายกรรมการได้เป็นระบบ
- ปรับ threshold ได้
- rank IP ได้
- เห็น high-confidence attacker ชัด

## Scoring ระดับ Request

ตัวอย่าง rule:

| Condition | Score | เหตุผล |
|---|---:|---|
| Path traversal | +5 | exploit ชัด |
| SQL injection | +5 | exploit ชัด |
| XSS | +5 | exploit ชัด |
| Sensitive endpoint | +3 | probe จุดเสี่ยง |
| Status 500 | +4 | อาจ trigger server error |
| Status 401/403 | +2 | probe protected resource |
| Status 404 | +1 | อาจเป็น scan แต่เดี่ยว ๆ ยังไม่แรง |
| POST to login/admin repeated | +3 | brute force / abuse |

## Scoring ระดับ IP

เพิ่มคะแนนจาก behavior รวม:

| Metric | Condition | Score |
|---|---|---:|
| high_404_count | 404 มากกว่า threshold | +3 ถึง +5 |
| high_500_count | 500 มากกว่า threshold | +4 |
| high_peak_rpm | peak request/minute สูงผิดปกติ | +4 |
| many_unique_endpoints | ยิงหลาย path มาก | +3 |
| incident_overlap | active ใน incident window | +3 |
| hidden_signature_hit | มี clue/signature | +5 |

## Label ที่แนะนำ

| Score | Label | คำอธิบาย |
|---:|---|---|
| 0-2 | `normal` | ไม่มี signal สำคัญ |
| 3-6 | `suspicious` | มีบางพฤติกรรมผิดปกติ |
| 7-12 | `likely_attacker` | red flags หลายข้อ |
| 13+ | `high_confidence_attacker` | evidence ชัดมาก |

## ตัวอย่างการคิดคะแนน

### IP A

```text
404 count สูงมาก: +5
sensitive endpoints: +3
peak rpm สูง: +4
ไม่มี payload ชัด: +0
รวม = 12 → likely_attacker
```

### IP B

```text
SQL injection payload: +5
500 errors หลัง payload: +4
incident overlap: +3
sensitive endpoint: +3
รวม = 15 → high_confidence_attacker
```

### IP C

```text
เข้า /admin ครั้งเดียว: +3
ไม่มีอย่างอื่น: +0
รวม = 3 → suspicious แต่ยังไม่ฟันธง
```

## Threshold ต้องอธิบายได้

Threshold ไม่ควรเป็น magic number เฉย ๆ ควรพูดว่า:

```text
เราเริ่มจาก conservative threshold เพื่อหลีกเลี่ยง false positives แล้วใช้ evidence lines ตรวจ manual เฉพาะ top suspicious IPs แทนการอ่านทั้งไฟล์
```

## ข้อควรระวัง

- score ไม่ใช่ความจริงสุดท้าย เป็น prioritization tool
- ต้องมี evidence request lines รองรับ
- top score อาจเป็น bot/proxy ต้องดู pattern ประกอบ
- hidden bonus อาจอยู่กับ IP ที่ไม่ได้ score สูงสุด
