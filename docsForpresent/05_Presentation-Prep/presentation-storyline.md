# Presentation Storyline — โครงเรื่องนำเสนอ

## Story ที่ควรเล่า

อย่านำเสนอแบบ “เราทำ command นี้ แล้วได้ตารางนี้” ให้เล่าเป็น incident story:

```text
เว็บมี log ขนาดใหญ่ → เราสร้าง pipeline → พบ traffic/error anomaly → identify attacker IPs → explain attack pattern → visualize dashboard → found hidden clue
```

## โครง Slide 15 นาที

| Slide | หัวข้อ | เวลา |
|---:|---|---:|
| 1 | Title + Mission | 1 นาที |
| 2 | Log Dataset & Constraints | 1 นาที |
| 3 | Analysis Pipeline | 2 นาที |
| 4 | Red Flags & Scoring Model | 2 นาที |
| 5 | WHO: Attacker IPs | 2 นาที |
| 6 | WHEN: Incident Timeline | 2 นาที |
| 7 | HOW: Attack Patterns | 2 นาที |
| 8 | Dashboard Demo | 2 นาที |
| 9 | Hidden Bonus + Conclusion | 1 นาที |

## Narrative ตัวอย่าง

### Problem

```text
เราได้รับ access log ขนาดใหญ่มาก และต้องหากลุ่มแฮกเกอร์โดยห้ามอ่าน log manual
```

### Method

```text
เรา parse log ทุกบรรทัดแบบ streaming แล้ว extract red flags เช่น payload, status anomalies, sensitive endpoints และ request rate
```

### Evidence

```text
จากนั้น aggregate ต่อ IP และต่อ minute เพื่อหาทั้ง attacker และ incident window
```

### Result

```text
เราได้รายชื่อ suspicious IPs พร้อม score, ช่วงเวลาที่ระบบผิดปกติ, attack pattern และ evidence lines
```

### Communication

```text
เราแสดงผลผ่าน dashboard เพื่อให้คนทั่วไปเห็น incident timeline และ attacker evidence โดยไม่ต้องอ่าน raw log
```

## Slide ที่ควรมีภาพ/กราฟ

- traffic over time
- 5xx over time
- top attacker IPs by score
- status distribution by attacker group
- suspicious endpoint categories

## ประโยคจบที่ดี

```text
Our main contribution is a reproducible investigation pipeline: it transforms millions of raw log lines into explainable evidence that identifies attackers, incident windows, attack methods, and hidden clues.
```
