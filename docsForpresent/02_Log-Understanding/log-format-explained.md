# Log Format Explained — เข้าใจ `cart_web.log`

## รูปแบบข้อมูลที่พบ

ตัวอย่าง format:

```text
2024-06-10 04:17:43 | 39.3.141.152 | POST | /checkout | 200 | 122
```

แยกได้เป็น 6 fields:

| ลำดับ | Field | ตัวอย่าง | ความหมาย |
|---:|---|---|---|
| 1 | timestamp | `2024-06-10 04:17:43` | เวลาที่ request เข้ามา |
| 2 | ip | `39.3.141.152` | IP ผู้เรียกเว็บ |
| 3 | method | `POST` | HTTP method |
| 4 | endpoint/path | `/checkout` | path ที่ถูกเรียก |
| 5 | status | `200` | HTTP response status |
| 6 | size | `122` | response size หรือขนาด response โดยประมาณ |

## สิ่งที่ log นี้ไม่มี

สำคัญมากสำหรับการนำเสนอ:

| Field ที่ไม่มี | ผลกระทบ |
|---|---|
| response time จริง | ห้าม claim ว่า response time สูงโดยตรง |
| user-agent | ใช้แยก `curl/sqlmap/Nmap` ไม่ได้ |
| request body | เห็น payload เฉพาะที่อยู่ใน URL/path/query เท่านั้น |
| header | หา clue ใน header ไม่ได้ เว้นแต่ถูก encode ลง path |

## แล้วจะวิเคราะห์ “ระบบหน่วง” ได้ยังไง

ถ้าไม่มี response time เราใช้ proxy signals:

- request volume spike
- 500 errors เพิ่มขึ้น
- 404/403 เพิ่มขึ้นจาก scanning
- endpoint หลักเริ่ม fail
- มี burst จาก IP เดิมในช่วงสั้น ๆ

คำพูดที่ปลอดภัย:

```text
เรา infer ช่วงระบบหน่วง/ไม่เสถียรจาก traffic spike และ server error spike ไม่ได้อ้าง response time จริง เพราะ log ไม่มี field response time
```

## Status code ที่ต้องเข้าใจ

| Status | ความหมายทั่วไป | ใช้เป็น signal ยังไง |
|---|---|---|
| 200 | สำเร็จ | อาจเป็น user ปกติ หรือ attacker ที่ probe สำเร็จ |
| 301/302 | redirect | ปกติได้ในบาง path |
| 400 | bad request | payload แปลกอาจทำให้เกิด |
| 401 | unauthorized | probing protected resource |
| 403 | forbidden | พยายามเข้า resource ต้องห้าม |
| 404 | not found | ถ้าเยอะจาก IP เดียว = directory brute-force |
| 500 | server error | อาจเป็น crash probing หรือ bug ถูก trigger |
| 503 | unavailable | ถ้ามี อาจสัมพันธ์กับ downtime |

## ตัวอย่างการตีความ 1 บรรทัด

```text
2024-06-10 05:01:12 | 8.8.8.8 | GET | /products | 200 | 143
```

น่าจะเป็น user ปกติ เพราะ:

- path ธรรมดา
- status 200
- ไม่มี payload แปลก

แต่:

```text
2024-06-10 05:01:13 | 6.6.6.6 | GET | /../../etc/passwd | 404 | 20
```

มี red flags:

- path traversal
- sensitive file `/etc/passwd`
- 404 อาจแปลว่ากำลัง probe

## หลักคิดสำคัญ

หนึ่งบรรทัดเป็นแค่ clue แต่การตัดสิน attacker ต้องดู pattern รวมของ IP และเวลาค่ะ
