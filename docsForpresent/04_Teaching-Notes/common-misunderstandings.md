# Common Misunderstandings — ความเข้าใจผิดที่ต้องกันไว้

## 1. “500 คือ hacker แน่นอน”

ผิดบางส่วนค่ะ 500 คือ server error อาจเกิดจาก:

- bug ปกติ
- input แปลกจาก user
- attack payload
- resource exhaustion

วิธีคิดที่ถูก:

```text
500 เป็น signal ต้องดู payload, IP behavior, endpoint และ incident timeline ประกอบ
```

## 2. “IP ที่ request เยอะสุดคือคนร้าย”

ไม่เสมอไป อาจเป็น:

- proxy/NAT
- crawler
- load test
- traffic ปกติของระบบ

วิธีคิดที่ถูก:

```text
request เยอะ + red flags + incident overlap = น่าสงสัยกว่า request เยอะอย่างเดียว
```

## 3. “404 เยอะคือแฮกแน่นอน”

404 เยอะอาจเป็น broken asset ได้ เช่น frontend เรียกไฟล์ผิด

ต้องดูว่า path เป็นอะไร:

- `/assets/logo.png` 404 ซ้ำ อาจเป็น bug
- `/.env`, `/admin`, `/backup.zip`, `/config.php` หลาย path = scan

## 4. “ถ้า status 200 แปลว่าปลอดภัย”

ผิดค่ะ attacker อาจได้ 200 จาก endpoint ที่ probe สำเร็จ

ตัวอย่าง:

```text
/search?q=<script>alert(1)</script> | 200
```

200 แต่ยังน่าสงสัย เพราะ payload เป็น XSS

## 5. “ไม่มี User-Agent แปลว่าวิเคราะห์ไม่ได้”

ยังวิเคราะห์ได้จาก:

- endpoint
- status
- rate
- IP pattern
- timeline
- payload ใน URL

แต่ต้องบอก limitation ว่าไม่มี UA

## 6. “Hidden bonus ต้องมีคำว่า name”

ไม่เสมอไป อาจซ่อนเป็น:

- base64
- hex
- path initials
- username ใน payload
- signature path
- response size sequence

## ประโยคจำง่าย

> log analysis ที่ดีคือการลดการเดา เพิ่ม evidence และพูดข้อจำกัดอย่างซื่อสัตย์
