# 15-Minute Talk Track — บทพูดนำเสนอ 15 นาที

## 0:00-1:00 — Mission

```text
งานนี้คือการวิเคราะห์ access log ขนาดใหญ่เพื่อหากลุ่มแฮกเกอร์ ระบุช่วงเวลาที่ระบบผิดปกติ อธิบายรูปแบบการโจมตี และนำเสนอผ่าน dashboard โดยห้ามอ่าน log manual ทั้งไฟล์
```

## 1:00-2:00 — Dataset

```text
log แต่ละบรรทัดมี timestamp, IP, method, endpoint, status และ size ข้อจำกัดคือไม่มี response time และ user-agent ดังนั้นเราจะ infer system instability จาก traffic/error patterns ไม่ claim latency โดยตรง
```

## 2:00-4:00 — Pipeline

```text
เราสร้าง pipeline ที่ parse log แบบ streaming, extract red flags, aggregate by IP และ by minute, calculate suspicion score, แล้ว export dashboard-ready files
```

## 4:00-6:00 — Scoring

```text
เราให้คะแนนจากหลายสัญญาณ เช่น malicious payload, sensitive endpoints, 404/500 anomalies และ request rate เพราะเราไม่ต้องการฟันธงจาก signal เดียว
```

## 6:00-8:00 — WHO

```text
ตารางนี้คือ suspicious IP ranking แต่ละ IP มี score, metrics และ evidence lines รองรับ
```

## 8:00-10:00 — WHEN

```text
timeline นี้แสดงช่วงที่ traffic/error เริ่มเบี่ยงจาก baseline จนถึงช่วง unstable/down window
```

## 10:00-12:00 — HOW

```text
attack pattern หลักที่พบคือ ... โดยมี evidence จาก endpoint/payload/status pattern เช่น ...
```

## 12:00-14:00 — Dashboard

```text
Dashboard แบ่งเป็น overview, attacker table, incident timeline, attack pattern และ evidence panel เพื่อให้คนทั่วไปเข้าใจ incident โดยไม่ต้องอ่าน raw log
```

## 14:00-15:00 — Hidden Bonus + Close

```text
สำหรับ hidden bonus เราค้นหา clue จาก suspicious endpoints, encoded strings และ marker-adjacent lines ผลที่พบคือ ... พร้อม evidence/confidence
```

## Closing Sentence

```text
สรุปคือเราเปลี่ยน raw log หลายล้านบรรทัดให้เป็น evidence-based incident report ที่ตอบได้ว่าใครโจมตี เมื่อไหร่ โจมตียังไง และแสดงผลให้คนอื่นเข้าใจผ่าน dashboard
```
