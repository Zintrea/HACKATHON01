# Strong Answers — คำตอบแบบแข็งแรงสำหรับนำเสนอ

## Answer Pattern: Claim → Evidence → Limitation

เวลาตอบกรรมการ ใช้สูตรนี้:

```text
เราสรุปว่า ... เพราะ evidence คือ ... อย่างไรก็ตาม limitation คือ ... ดังนั้นเราใช้วิธี ... เพื่อควบคุมความเสี่ยง
```

## ตัวอย่าง 1: Attacker IP

```text
เราจัด IP นี้เป็น high-confidence attacker เพราะมีทั้ง SQL injection payload, path traversal, 500 errors และ peak request rate สูงในช่วง incident window โดยเราไม่ได้ใช้ request count อย่างเดียว แต่ใช้หลาย red flags ร่วมกัน
```

## ตัวอย่าง 2: Slow/Down Window

```text
เราแบ่ง log เป็นรายนาที แล้วพบว่า requests และ 5xx errors เพิ่มขึ้นผิดปกติในช่วงนี้ จึงระบุเป็น unstable/down window อย่างไรก็ตาม log ไม่มี response time field เราจึงไม่ claim latency จริง แต่ infer จาก error/traffic spike
```

## ตัวอย่าง 3: False Positive

```text
404 หนึ่งครั้งไม่เพียงพอในการตัดสิน attacker ค่ะ แต่ IP นี้มี 404 หลายร้อยครั้งต่อหลายร้อย unique endpoints เช่น /.env, /config.php และ /backup.zip ซึ่งเป็น pattern ของ directory brute-force
```

## ตัวอย่าง 4: Hidden Bonus

```text
Hidden clue นี้เจอใน endpoint ที่มาจาก suspicious IP ช่วง incident และมีรูปแบบคล้าย encoded/signature text หลัง decode ได้คำว่า ... เราจึงรายงานเป็น candidate พร้อม confidence และ evidence line
```

## ตัวอย่าง 5: Why Dashboard

```text
Dashboard ไม่ใช่แค่ตกแต่ง แต่เป็นการเปลี่ยน raw forensic data ให้คนตัดสินใจเห็นภาพ เช่น attacker ranking, incident timeline, error spike และ evidence requests
```

## คำที่ควรใช้

- evidence-based
- reproducible
- correlated with
- inferred
- high-confidence
- conservative threshold
- false-positive control
- dashboard-ready output

## คำที่ควรเลี่ยง

- เดา
- แน่นอน 100% ถ้ายังไม่พิสูจน์
- response time สูง ถ้าไม่มี response time
- IP นี้ hacker เพราะยิงเยอะอย่างเดียว
