# Likely Judge Questions — คำถามกรรมการที่น่าจะเจอ

## 1. ทำไมถึงบอกว่า IP นี้เป็น attacker?

คำตอบ:

```text
เราไม่ได้ดูจาก request count อย่างเดียวค่ะ IP นี้มีหลาย red flags พร้อมกัน เช่น malicious payload, sensitive endpoint probing, 404/500 จำนวนมาก, peak request rate สูง และ activity เกิดตรงกับ incident window จึงจัดเป็น high-confidence attacker
```

## 2. ถ้า user ปกติเข้า `/admin` ครั้งเดียวล่ะ?

คำตอบ:

```text
request เดียวเราไม่ฟันธงค่ะ เราใช้ repeated behavior และหลาย signals ประกอบกัน เช่น จำนวน endpoint ที่ลอง ความถี่ status pattern และ payload
```

## 3. Log ไม่มี response time แล้วรู้ได้ไงว่าระบบหน่วง?

คำตอบ:

```text
เราไม่ claim response time จริงค่ะ เพราะ field นั้นไม่มีใน log เราใช้คำว่า inferred unstable period จาก traffic spike และ server error spike แทน
```

## 4. ทำไมไม่อ่าน log manual?

คำตอบ:

```text
ไฟล์มีจำนวนบรรทัดมหาศาล การอ่าน manual ไม่ reproducible และพลาดง่าย เราจึงเขียน script เพื่อ parse, aggregate, score และ generate evidence อัตโนมัติ
```

## 5. Scoring threshold ตั้งมายังไง?

คำตอบ:

```text
เราเริ่มจาก conservative scoring โดยให้ payload ที่เป็น exploit ชัดได้คะแนนสูง ส่วน signal ที่อาจ false positive เช่น 404 เดี่ยว ๆ ได้คะแนนต่ำ จากนั้นใช้ threshold แบ่ง suspicious/likely/high-confidence และตรวจ evidence lines ประกอบ
```

## 6. ถ้า IP เป็น NAT/proxy จะทำยังไง?

คำตอบ:

```text
เป็น limitation ที่เราระบุไว้ค่ะ เราจึงไม่ใช้ IP count อย่างเดียว แต่ดู behavior pattern, payload, endpoint, rate และ incident correlation เพื่อเพิ่ม confidence
```

## 7. Dashboard มีประโยชน์อะไร?

คำตอบ:

```text
Dashboard ทำให้ non-technical stakeholders เห็น incident ได้ทันที เช่น top suspicious IPs, traffic/error timeline, affected endpoints และ evidence requests โดยไม่ต้องเปิด raw log
```

## 8. Hidden bonus มั่นใจได้ยังไงว่าเป็นชื่อจริง?

คำตอบถ้าเจอ:

```text
เราเจอ clue นี้ใน suspicious request จาก attacker IP ช่วง incident และข้อความไม่ใช่ endpoint ปกติ หลัง decode/normalize ได้ candidate name พร้อม evidence line จึงจัดเป็น hidden bonus candidate
```

คำตอบถ้ายังไม่มั่นใจ:

```text
เราแยก confidence level ไว้ค่ะ ถ้า clue ยังมีหลักฐานไม่พอ จะรายงานเป็น candidate พร้อมเหตุผล ไม่ฟันธงเกินข้อมูล
```

## 9. ถ้า attacker ยิงน้อยแต่ payload ชัด จะเจอไหม?

คำตอบ:

```text
เจอค่ะ เพราะ scoring ไม่ได้พึ่ง request volume อย่างเดียว payload เช่น SQLi/path traversal ได้คะแนนสูง แม้จำนวน request ไม่มากก็ถูกจัดอันดับขึ้นมาได้
```

## 10. คุณ validate ผลยังไง?

คำตอบ:

```text
เรา validate โดยเก็บ evidence lines ต่อ IP, ตรวจ top incident windows กับ raw log snippets, และแยก limitations/false positive cases ชัดเจน
```
