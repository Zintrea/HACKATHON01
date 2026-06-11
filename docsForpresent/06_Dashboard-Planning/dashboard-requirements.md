# Dashboard Requirements — Dashboard ต้องตอบอะไร

## เป้าหมาย Dashboard

Dashboard ต้องทำให้คนดูตอบ 4 คำถามได้เร็ว:

1. ใครน่าสงสัยที่สุด
2. เหตุเกิดตอนไหน
3. ระบบกระทบยังไง
4. หลักฐานคืออะไร

## Minimum Sections

| Section | ตอบคำถาม | ควรแสดง |
|---|---|---|
| Overview Cards | ภาพรวม | total requests, suspicious IPs, 5xx count, incident windows |
| Attacker Ranking | WHO | IP, score, label, key metrics |
| Timeline Chart | WHEN | requests/4xx/5xx over time |
| System State | WHEN | normal/suspicious/unstable/down by minute |
| Attack Patterns | HOW | payload categories, endpoints |
| Evidence Table | HOW | suspicious request examples |
| Hidden Bonus | BONUS | candidate clue + confidence |

## Dashboard ไม่ควรเป็นแค่ตาราง

ควรมี story flow:

```text
Overview → Timeline → Attacker Ranking → Evidence → Hidden Bonus
```

## Metrics สำคัญ

### Cards

- total log lines parsed
- unique IPs
- suspicious IPs
- high-confidence attackers
- total 4xx
- total 5xx
- incident start/end
- hidden bonus candidate

### Charts

- line chart: requests per minute
- line/bar chart: 5xx per minute
- stacked bar: status code distribution
- bar chart: top suspicious IPs
- bar chart: top suspicious endpoints

### Tables

- attacker IPs
- incident windows
- suspicious requests
- hidden bonus findings

## Filters ที่ควรมีถ้าทำทัน

- time range
- IP address
- attack type
- status code
- label/confidence

## Design Principle

Dashboard ต้องตอบโจทย์นำเสนอ ไม่ใช่แค่โชว์ข้อมูลเยอะ

```text
ถ้ากรรมการมอง 10 วินาที ต้องรู้ว่าเกิด incident ช่วงไหน และ IP ไหนน่าสงสัยสุด
```
