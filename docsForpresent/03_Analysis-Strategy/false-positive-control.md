# False Positive Control — กันการกล่าวหาผิด

## ทำไมสำคัญ

ใน security analysis การกล่าวหาผิดทำให้ผลวิเคราะห์ไม่น่าเชื่อถือ กรรมการอาจถามทันทีว่า “คุณมั่นใจได้ยังไง”

## สาเหตุ False Positive ที่พบบ่อย

| Signal | อาจไม่ใช่ attacker เพราะ |
|---|---|
| 404 | broken link / user พิมพ์ผิด |
| 500 | server bug ปกติ |
| request เยอะ | NAT, proxy, crawler |
| เข้า `/admin` | user เดา URL เล่น |
| POST `/login` | user login ปกติ |

## วิธีลด False Positive

### 1. ใช้หลาย signal ประกอบกัน

ไม่ใช้ signal เดียวตัดสิน

```text
404 เยอะ + many endpoints + high rate + sensitive paths = stronger evidence
```

### 2. ดูช่วงเวลา incident

IP ที่ active ตรงช่วงระบบ error spike น่าสงสัยกว่า IP ที่แปลกแต่เกิดนอกช่วง incident

### 3. เก็บ evidence examples

ทุก attacker IP ควรมีตัวอย่าง request 3-5 บรรทัด

### 4. ใช้ label แบบมีระดับ

อย่าใช้แค่ hacker/non-hacker

```text
normal / suspicious / likely_attacker / high_confidence_attacker
```

### 5. ระบุ limitations

เช่น ไม่มี user-agent, ไม่มี response time, ไม่มี request body

## ตัวอย่างคำตอบกรรมการ

ถาม:

```text
ทำไมไม่ถือว่า IP นี้เป็น user ปกติที่พิมพ์ URL ผิด?
```

ตอบ:

```text
ถ้าเป็น request เดียวเราไม่ฟันธงค่ะ แต่ IP นี้ลอง endpoint หลายร้อย path ภายในเวลาสั้น ๆ เช่น /.env, /config.php, /backup.zip และมี 404 จำนวนมาก จึงมี pattern แบบ directory brute-force ไม่ใช่ user journey ปกติ
```

## Conservative Claiming

คำที่ควรใช้:

- likely
- suspected
- high-confidence
- inferred
- correlated with

คำที่ควรเลี่ยงถ้ายังไม่มีหลักฐาน:

- แน่นอน 100%
- เป็นคนร้ายแน่ ๆ เพราะ request เยอะ
- response time สูงแน่นอน ทั้งที่ไม่มี response time

## ประโยคสอนทีม

> เราไม่ได้พยายามหาคำตอบที่ดูแรงที่สุด แต่หาคำตอบที่ defend ได้ดีที่สุดต่อหน้ากรรมการ
