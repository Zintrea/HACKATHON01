# What We Need To Prove — เราต้องพิสูจน์อะไรบ้าง

## 1. พิสูจน์ว่า “ใครคือคนร้าย”

ต้องตอบเป็น IP หลายตัวได้ ไม่ใช่ IP เดียว ถ้ามีหลายกลุ่มหรือหลายเครื่องร่วมโจมตี

หลักฐานที่ควรใช้:

- จำนวน request รวม
- จำนวน 404/401/403/500
- malicious payload เช่น `../`, `UNION SELECT`, `<script>`
- sensitive endpoint เช่น `/admin`, `/.env`, `/config.php`
- peak requests per minute
- active time อยู่ตรงกับ incident window หรือไม่

ตัวอย่างการอธิบาย:

```text
IP 10.1.2.3 ถูกจัดเป็น attacker เพราะภายใน 3 นาทีมี 1,200 requests, 900 ครั้งเป็น 404, path กระจายไปยัง admin/config/backup และมี request ไปยัง /etc/passwd
```

## 2. พิสูจน์ว่า “เกิดตอนไหน”

ต้องแบ่งเวลาเป็น bucket เช่น ราย 1 นาที หรือ 5 นาที แล้วดู pattern:

- total requests ต่อช่วงเวลา
- 4xx ต่อช่วงเวลา
- 5xx ต่อช่วงเวลา
- จำนวน IP ที่ active
- endpoint ที่ถูกยิงมากที่สุด

คำสำคัญ:

| คำ | ความหมายที่ควรใช้ |
|---|---|
| เริ่มผิดปกติ | เริ่มมี traffic/error เบี่ยงจาก baseline |
| ระบบหน่วง | traffic spike หรือ error เพิ่ม แต่ยังไม่ใช่ล่มชัดเจน |
| ระบบล่ม | 500/503 spike หรือ endpoint หลักล้มเหลวเยอะผิดปกติ |

## 3. พิสูจน์ว่า “โจมตียังไง”

ต้องบอกลักษณะการโจมตี ไม่ใช่แค่บอก IP:

| Attack Type | Evidence ที่ควรเห็น |
|---|---|
| Directory brute force | 404 จำนวนมาก หลาย path จาก IP เดียว |
| Path traversal | `../`, `%2e%2e`, `/etc/passwd` |
| SQL injection | `'`, `%27`, `UNION`, `SELECT`, `OR 1=1` |
| XSS | `<script>`, `%3Cscript`, `javascript:` |
| DoS / flood | request rate สูงมากในเวลาสั้น |
| Crash probing | request ที่สัมพันธ์กับ 500 errors |

## 4. พิสูจน์ว่า Dashboard ช่วยเล่าเรื่องได้

Dashboard ควรตอบได้ทันที:

- IP ไหนเสี่ยงสุด
- เหตุเกิดช่วงเวลาไหน
- ระบบกระทบยังไง
- evidence request คืออะไร
- attack pattern หลักคืออะไร

## 5. พิสูจน์ Hidden Bonus

ถ้าพบชื่อ/ลายเซ็นคนร้าย ต้องตอบได้ว่า:

- clue เจอที่ไหนใน log
- ทำไมคิดว่าเป็นชื่อจริง/signature
- ถ้าเป็น encoded text decode ด้วยวิธีอะไร
- มี request lines รองรับหรือไม่

## หลักฐานต้องไม่เกินจริง

ถ้า log ไม่มี response time อย่าพูดว่า “response time สูง” แบบฟันธง ให้พูดว่า:

> The log does not include actual response time. We infer unstable or slow periods from abnormal traffic spikes and increased server-side errors.
