# Tricks To Explain Well — เทคนิคสอนและนำเสนอให้เข้าใจ

## 1. ใช้ภาพเปรียบเทียบก่อนเทคนิค

เริ่มจาก:

```text
Log เหมือนกล้องวงจรปิดของเว็บ แต่มีหลายสิบล้านเฟรม เราเลยต้องใช้ script ช่วยหา pattern
```

คนฟังจะเข้าใจทันทีว่าทำไม manual ไม่ได้

## 2. แยกคำว่า Clue / Signal / Evidence

| คำ | ความหมาย |
|---|---|
| Clue | บรรทัดแปลกหนึ่งบรรทัด |
| Signal | metric ที่บอกความผิดปกติ |
| Evidence | หลาย signals รวมกันพร้อมตัวอย่าง log |

## 3. พูดว่า “เราไม่ฟันธงจากสิ่งเดียว”

ประโยคนี้ช่วยกันคำถาม false positive:

```text
เราไม่ classify จาก single request แต่ใช้ repeated behavior และหลาย red flags ประกอบกัน
```

## 4. อธิบาย Dashboard เป็น Story

ไม่ใช่บอกว่า “นี่กราฟ” แต่บอกว่า:

```text
กราฟนี้ตอบ WHEN, ตารางนี้ตอบ WHO, ส่วน evidence panel ตอบ HOW
```

## 5. ถ้าโดนถามแล้วไม่แน่ใจ

ตอบแบบมืออาชีพ:

```text
จาก log field ที่มี เรายืนยันได้ระดับนี้ ส่วนข้อมูลนี้ต้องใช้ field เพิ่ม เช่น user-agent/response time/request body เพื่อยืนยันต่อ
```

## 6. ใช้คำว่า “confidence”

แทนที่จะบอกว่า “ใช่/ไม่ใช่” อย่างเดียว ให้บอกระดับ:

```text
low / medium / high-confidence attacker
```

## 7. แสดงตัวอย่างน้อยแต่คม

อย่าโชว์ log 100 บรรทัด ให้โชว์ 3 บรรทัดที่แทน pattern:

- path traversal
- SQLi/XSS
- 500 trigger

## 8. เทคนิคตอบ Hidden Bonus

ถ้า clue เป็น encoded ให้เล่าว่า:

```text
เจอ string แปลก → ตรวจว่าเป็น encoding → decode → เทียบกับ suspicious IP/time → สรุป candidate
```
