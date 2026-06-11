# Dashboard User Flow — คนดูควรไล่ดูยังไง

## Flow ที่ดี

```text
1. ดู Overview ว่า incident ใหญ่แค่ไหน
2. ดู Timeline ว่าเกิดตอนไหน
3. ดู Top IPs ว่าใครน่าสงสัย
4. คลิก/ดู Evidence ว่าเขาทำอะไร
5. ดู Attack Pattern ว่าโจมตีแบบไหน
6. ดู Hidden Bonus ว่าพบ clue อะไร
```

## สำหรับกรรมการที่มีเวลาน้อย

ต้องตอบใน 30 วินาที:

- Top attacker คือใคร
- incident เกิดช่วงไหน
- attack pattern หลักคืออะไร
- dashboard generated from script ไม่ใช่ manual

## สำหรับคน technical

ควรมีข้อมูล drill-down:

- IP metrics
- suspicious request lines
- endpoint summary
- scoring reason

## สำหรับคน non-technical

ควรมีคำอธิบายข้างกราฟ:

```text
ช่วงที่เส้นสีแดงสูงคือ server error เพิ่มผิดปกติ สัมพันธ์กับ request spike จาก suspicious IPs
```

## Dashboard Copy ตัวอย่าง

### Overview subtitle

```text
Script-generated incident analysis from cart_web.log. No manual line-by-line inspection.
```

### Attacker table helper text

```text
IPs are ranked by combined suspicious signals: payloads, error patterns, sensitive endpoints, and request rate.
```

### Timeline helper text

```text
System state is inferred from traffic and error spikes because the log does not include response time.
```
