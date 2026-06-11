# Dashboard Layout — โครงหน้าจอ Web App

## Layout ที่แนะนำ

```text
┌────────────────────────────────────────────┐
│ H1 Incident Dashboard                       │
│ Mission summary + last generated time       │
├──────────┬──────────┬──────────┬───────────┤
│ Requests │ 5xx Errs │ Attackers│ Incident  │
├────────────────────────────────────────────┤
│ Traffic + Error Timeline                    │
├──────────────────────┬─────────────────────┤
│ Top Suspicious IPs   │ System State Timeline│
├──────────────────────┴─────────────────────┤
│ Attack Pattern Summary                      │
├────────────────────────────────────────────┤
│ Evidence Requests Table                     │
├────────────────────────────────────────────┤
│ Hidden Bonus Candidate                      │
└────────────────────────────────────────────┘
```

## Section Details

### 1. Header

ควรมี:

- ชื่อ dashboard
- source log: `cart_web.log`
- generated timestamp
- note: no manual log reading, script-generated analysis

### 2. Overview Cards

ตัวอย่าง:

| Card | ตัวอย่างข้อความ |
|---|---|
| Total Requests | 21,146,398 |
| Suspicious IPs | 12 |
| 5xx Errors | 3,420 |
| Main Incident Window | 05:12-05:18 |

### 3. Timeline

แกน X = เวลา

เส้น/แท่ง:

- total requests
- 4xx
- 5xx
- suspicious requests

### 4. Attacker Ranking

Columns:

```text
rank, ip, score, label, total_requests, peak_rpm, 404, 500, payload_hits, evidence_link
```

### 5. Attack Pattern Summary

แสดงหมวด:

- brute force / directory scan
- SQLi
- XSS
- path traversal
- crash probing

### 6. Evidence Table

Columns:

```text
timestamp, ip, method, endpoint, status, reason, score
```

ควร truncate endpoint แต่ click expand ได้ถ้าทำ web app

### 7. Hidden Bonus

แสดง:

```text
candidate, confidence, clue_type, decode_method, evidence_line
```

## UX Trick สำหรับนำเสนอ

ทำให้ dashboard มี “answer labels” เช่น:

- WHO: Top attacker IPs
- WHEN: Incident timeline
- HOW: Attack pattern
- BONUS: Hidden clue

กรรมการจะเห็นว่าตอบโจทย์ครบค่ะ
