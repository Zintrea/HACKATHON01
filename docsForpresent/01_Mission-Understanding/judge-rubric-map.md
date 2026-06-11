# Judge Rubric Map — จับโจทย์ให้ตรงกับคะแนน

## ภาพรวม

กรรมการมักให้คะแนนจากทั้ง correctness, methodology, coding, visualization, และการนำเสนอ ดังนั้นงาน H1 ควร map แบบนี้:

| Mission | สิ่งที่ส่ง/โชว์ | คะแนนที่ช่วยเพิ่ม |
|---|---|---|
| WHO ARE THEY | attacker IP table + score + evidence | analytical reasoning |
| WHEN & HOW | timeline + pattern summary | incident understanding |
| TELL PEOPLE | dashboard/web app | communication + product |
| HIDDEN BONUS | clue hunting + proof | creativity + depth |
| ห้าม manual | script + reproducible outputs | engineering quality |

## สิ่งที่กรรมการน่าจะชอบ

1. **ไม่เดาสุ่ม** — ทุก claim มี data support
2. **มี methodology ชัด** — explainable rules/scoring
3. **มี visualization** — timeline, charts, tables
4. **มี limitations** — รู้ว่า log มี/ไม่มีอะไร
5. **มี evidence** — request examples จาก log
6. **ทำซ้ำได้** — script + outputs

## สิ่งที่ทำให้เสียคะแนน

| Pitfall | ทำไมอันตราย |
|---|---|
| บอกว่า 500 ทุกอันคือ hacker | false positive สูง |
| บอกว่า request เยอะสุด = คนร้ายเสมอ | CDN/bot/user spike อาจหลอกได้ |
| ไม่มีวิธีหา IP ทั้งหมด | อาจพลาด attacker ที่ยิงน้อยแต่ payload ชัด |
| ไม่มี timeline | ตอบ WHEN ไม่ได้ |
| dashboard มีแต่ตาราง ไม่มี story | คนดูไม่เข้าใจ incident |
| hidden bonus ไม่มีหลักฐาน | เหมือนเดา |

## Rubric ส่วน coding

สคริปต์ควรมี:

- อ่านไฟล์ใหญ่แบบ streaming ไม่โหลดทั้งไฟล์เข้า memory
- parse field ได้ robust
- export CSV/JSON/Markdown
- มี config สำหรับ threshold
- มีคำอธิบายว่ากฎ scoring คืออะไร

## ประโยคใช้ตอนนำเสนอ

> Our goal was not just to find suspicious lines. We transformed a large raw log into structured evidence: IP risk scores, incident windows, attack patterns, and dashboard-ready datasets.
