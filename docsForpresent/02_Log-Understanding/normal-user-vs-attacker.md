# Normal User vs Attacker — แยกยังไงให้ไม่มั่ว

## หลักการใหญ่

อย่าตัดสินจากบรรทัดเดียว ให้ดู **พฤติกรรมซ้ำ + context + ช่วงเวลา**

```text
single weird request = clue
repeated suspicious behavior = evidence
suspicious behavior during incident window = strong evidence
```

## ผู้ใช้งานทั่วไปมักมี pattern แบบไหน

| Pattern | ตัวอย่าง |
|---|---|
| เข้า endpoint ปกติ | `/`, `/products`, `/cart`, `/checkout`, `/login` |
| request rate สมเหตุสมผล | หลาย request ภายในหลายนาที ไม่ใช่พันครั้งในนาทีเดียว |
| status ส่วนใหญ่ 200/302 | สำเร็จหรือ redirect |
| path มีลำดับ user journey | products → cart → checkout |
| error ไม่ซ้ำจำนวนมาก | อาจมี 404 บ้างแต่ไม่ใช่รัว ๆ หลายสิบ path |

ตัวอย่าง:

```text
09:00:01 | 1.1.1.1 | GET  | /products | 200
09:00:15 | 1.1.1.1 | GET  | /cart     | 200
09:00:40 | 1.1.1.1 | POST | /checkout | 200
```

นี่เหมือน user journey ธรรมดา

## Attacker มักมี pattern แบบไหน

| Pattern | ตัวอย่าง |
|---|---|
| ยิง endpoint จำนวนมาก | `/admin`, `/.env`, `/backup.zip`, `/config.php` |
| 404 เยอะ | directory brute force |
| 401/403 เยอะ | probing protected endpoint |
| 500 เยอะ | อาจ trigger bug/crash |
| payload แปลก | `../`, `UNION SELECT`, `<script>` |
| rate สูง | requests per minute สูงผิดปกติ |
| path ไม่เป็น user journey | กระโดดไปเรื่อย ๆ แบบ wordlist |

ตัวอย่าง:

```text
09:01:00 | 9.9.9.9 | GET | /.env        | 404
09:01:01 | 9.9.9.9 | GET | /admin       | 403
09:01:01 | 9.9.9.9 | GET | /config.php  | 404
09:01:02 | 9.9.9.9 | GET | /../../etc/passwd | 404
```

นี่เหมือน scanner/attacker มากกว่า user ปกติ

## กรณีที่ต้องระวัง False Positive

| สถานการณ์ | ทำไมหลอกได้ | วิธีลดความเสี่ยง |
|---|---|---|
| user เข้า `/admin` ครั้งเดียว | อาจพิมพ์เล่น | ต้องดูซ้ำไหมและมี path อื่นไหม |
| 500 จาก endpoint ปกติ | เว็บอาจ bug เอง | ดูว่ามี payload หรือ spike ไหม |
| request เยอะจาก IP เดียว | อาจเป็น NAT/proxy | ดู payload + status pattern ประกอบ |
| 404 หลายครั้ง | broken frontend asset | ดูว่า path เป็น asset จริงหรือ wordlist |

## Example: ตัดสินแบบ scoring

ถ้า IP A มี:

- 404 = 300 ครั้ง
- path มี `/.env`, `/config`, `/admin`
- peak 500 requests/minute
- ไม่มี payload แปลก

ผล: suspicious/likely scanner

ถ้า IP B มี:

- 20 requests
- มี `UNION SELECT` 3 ครั้ง
- มี 500 จาก endpoint เดิม 2 ครั้ง

ผล: likely attacker แม้ request ไม่เยอะ เพราะ payload ชัด

## ประโยคสอนทีม

> Hacker ไม่จำเป็นต้องยิงเยอะที่สุดเสมอ บางคนยิงน้อยแต่ payload ชัด ส่วนบางคนยิงเยอะมากแต่ต้องดูว่าเขายิงอะไรและเกิดผลอะไรกับระบบ
