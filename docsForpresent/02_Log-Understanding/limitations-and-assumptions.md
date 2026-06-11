# Limitations and Assumptions — ข้อจำกัดที่ต้องพูดให้เป็น

## ทำไมต้องมีไฟล์นี้

เวลานำเสนอ กรรมการอาจถามว่า “รู้ได้ยังไง” หรือ “มั่นใจแค่ไหน” การบอก limitations ทำให้เราดูน่าเชื่อถือ ไม่ใช่เดาเกินข้อมูล

## Limitations ของ `cart_web.log`

| ข้อจำกัด | ผลกระทบ | วิธีพูด |
|---|---|---|
| ไม่มี response time | ระบุ latency จริงไม่ได้ | ใช้ traffic/error spike เป็น proxy |
| ไม่มี user-agent | แยก tool เช่น sqlmap/curl จาก UA ไม่ได้ | ใช้ endpoint/payload/rate แทน |
| ไม่มี request body | payload ใน POST body อาจมองไม่เห็น | วิเคราะห์เฉพาะ URL/path/status |
| ไม่มี session/user id | ผูก IP กับ user จริงไม่ได้ | วิเคราะห์ระดับ IP เท่านั้น |
| IP อาจเป็น NAT/proxy | หลายคนอาจแชร์ IP | ใช้ behavior pattern ไม่ใช่ IP อย่างเดียว |

## Assumptions ที่ใช้ได้

1. แต่ละบรรทัดคือหนึ่ง HTTP request
2. field ถูกคั่นด้วย ` | `
3. timestamp ใน log เรียงตามเวลาหรืออย่างน้อย parse ได้
4. status code สะท้อนผลตอบกลับจาก server
5. path/query ที่ปรากฏใน endpoint ใช้เป็น evidence ของ payload ได้

## ตัวอย่างประโยคตอบกรรมการ

### ถาม: “คุณรู้ได้ยังไงว่าระบบหน่วง?”

ตอบ:

```text
Log ชุดนี้ไม่มี response time field เราจึงไม่ claim latency โดยตรง แต่ระบุเป็น inferred unstable window จาก traffic spike, error spike, และ server-side 500 ที่เพิ่มขึ้นผิดปกติ
```

### ถาม: “IP เดียวอาจเป็น NAT ได้ไหม?”

ตอบ:

```text
เป็นไปได้ค่ะ ดังนั้นเราไม่ได้ตัดสินจาก IP request count อย่างเดียว แต่ดู payload, sensitive endpoint probing, status distribution และช่วงเวลาที่สัมพันธ์กับ incident ด้วย
```

### ถาม: “ถ้า 500 เกิดจาก bug ปกติล่ะ?”

ตอบ:

```text
เรา treat 500 as a signal, not direct proof. ถ้า 500 เกิดร่วมกับ malicious payload หรือ request burst จาก IP เดิมในช่วง incident ความน่าเชื่อถือจึงสูงขึ้น
```
