# Risk Checklist — ความเสี่ยงของงาน H1

## Technical Risks

| Risk | วิธีลดความเสี่ยง |
|---|---|
| ไฟล์ใหญ่มาก script ช้า | streaming + aggregate dict |
| memory เต็ม | ไม่เก็บ raw rows ทั้งหมด |
| parse error | log malformed lines แยก |
| output ใหญ่เกิน | จำกัด evidence samples/top N |
| dashboard ช้า | ใช้ aggregated JSON/CSV ไม่อ่าน raw log ใน browser |

## Analysis Risks

| Risk | วิธีลดความเสี่ยง |
|---|---|
| false positive | scoring + evidence + labels หลายระดับ |
| false negative | payload score สูงแม้ request น้อย |
| overclaim response time | ใช้คำว่า inferred unstable |
| hidden bonus เดาผิด | confidence + source evidence |

## Presentation Risks

| Risk | วิธีลดความเสี่ยง |
|---|---|
| อธิบาย technical เกิน | เริ่มจาก story WHO/WHEN/HOW |
| กรรมการถาม threshold | เตรียม scoring rationale |
| dashboard ไม่ตอบโจทย์ | label sections ตาม mission |
| ไม่มี evidence | เตรียม request snippets |

## Red Team Question ที่ควรซ้อม

```text
ถ้า attacker ใช้ IP น้อยและยิง payload แค่ไม่กี่ครั้ง คุณจะเจอไหม?
```

คำตอบ:

```text
เจอค่ะ เพราะ scoring ให้ payload ที่ชัด เช่น SQLi/path traversal คะแนนสูง ไม่ได้พึ่ง request volume อย่างเดียว
```
