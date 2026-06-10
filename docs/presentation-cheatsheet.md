# Presentation Cheatsheet — ชีทสั้นสำหรับพรีเซนต์ H1

> เปิดอ่านก่อนพรีเซนต์ / ใช้เป็นคำตอบเร็วเวลาถูกถาม

## Mission 4 ข้อ

| Mission | เราตอบด้วยไฟล์ไหน |
|---|---|
| WHO ARE THEY? | `attacker_ips.csv` |
| WHEN & HOW? | `incident_windows.csv`, `endpoint_summary.csv`, `suspicious_requests.csv` |
| TELL PEOPLE | `dashboard_data.json` / dashboard |
| HIDDEN BONUS | `hidden_bonus_candidates.csv` |

---

## One-minute summary

```text
เราไม่ได้อ่าน log manual แต่สร้าง Python pipeline ที่ parse log ทุกบรรทัดเป็น structured data จากนั้น detect red flags, ให้ suspicion score, aggregate ตาม IP/endpoint/time, และ export เป็น CSV/JSON/Markdown เพื่อใช้ทำ dashboard และ evidence report
```

---

## Key facts จาก output ล่าสุด

```text
parsed_lines = 21,146,397
malformed_lines = 1
suspicious_ips = 19
```

Status counts:

```text
200 = 10,608,035
304 = 2,581,383
404 = 2,584,078
500 = 2,687,007
504 = 2,685,894
```

Top attacker IPs:

```text
1. 209.103.8.44
2. 197.82.237.190
3. 162.240.218.117
4. 119.123.55.141
5. 215.143.100.205
```

Main reasons:

```text
server_error;
sensitive_endpoint;
high_500_count;
many_sensitive_hits
```

---

## Key insight ที่ควรเล่า

### `/cart` vs `/cart_`

`/cart` ปกติ:

```text
total_requests = 2,581,034
status_200 = 1,720,806
status_304 = 429,968
status_404 = 430,260
status_5xx = 0
attack_type = normal
```

`/cart_` แปลก:

```text
total_requests = 152,835
status_500 = 76,402
status_504 = 76,433
status_5xx = 152,835
attack_type = server_error
```

ประโยคพูด:

```text
Endpoint ปกติอย่าง /cart ไม่ได้ล่ม แต่ endpoint variant อย่าง /cart_ มีเฉพาะ 500/504 ทั้งหมด จึงเป็น pattern สำคัญที่ชี้ว่าการโจมตีเกี่ยวข้องกับ path variants ที่ทำให้ server error
```

---

## Code story ที่พูดบน slide

```text
1. Parser: raw log → structured request
2. Pattern Detector: request → red flags
3. Scoring: red flags → explainable score
4. Aggregator: request → IP/endpoint/time summaries
5. Timeline: minute buckets → incident windows
6. Hidden Bonus: endpoint strings → clue candidates
7. Reports: CSV/JSON/Markdown → dashboard/presentation
```

---

## คำถามกรรมการ + คำตอบเร็ว

### Q1: ทำไมบอกว่า IP นี้เป็น attacker?

```text
เพราะ IP นี้มีหลาย evidence signals พร้อมกัน: server_error จำนวนมาก, sensitive endpoint hits จำนวนมาก, และอยู่ในกลุ่ม IP ที่สร้าง 500/504 ซ้ำ ๆ บน endpoint variants ไม่ได้ตัดสินจาก request count อย่างเดียว
```

### Q2: 500 อาจเป็น bug ปกติได้ไหม?

```text
เป็นไปได้ค่ะ ดังนั้นเราไม่ใช้ 500 เดี่ยว ๆ เป็น proof แต่ดู pattern ซ้ำจาก IP กลุ่มเดิมและ endpoint variants เช่น /cart_ ที่ 5xx ทั้งหมด ซึ่งต่างจาก /cart ปกติที่ไม่มี 5xx
```

### Q3: รู้ได้ยังไงว่าระบบหน่วงหรือ down?

```text
Log ไม่มี response time field เราจึงไม่ claim latency จริง แต่ infer unstable/down windows จาก 5xx spike และ server-side error pattern
```

### Q4: ทำไมไม่อ่าน log manual?

```text
ไฟล์มีมากกว่า 21 ล้านบรรทัด การอ่าน manual ไม่ reproducible และพลาดง่าย เราจึงเขียน script เพื่อ parse, aggregate, score, และ export evidence อัตโนมัติ
```

### Q5: Dashboard ใช้อะไร?

```text
ใช้ dashboard_data.json ซึ่งรวม overview, attackers, sampled timeline, incidents, endpoints, evidence และ hidden bonus candidates ให้ browser เปิดง่าย ส่วน timeline เต็มยังอยู่ใน traffic_timeline.csv
```

### Q6: Hidden bonus เจอไหม?

```text
ด้วย rule ปัจจุบันยังไม่เจอ candidate ที่มั่นใจ จึงไม่ฟันธงเกินหลักฐาน ถ้าต่อเวลาได้จะ hunt เฉพาะ attacker IP group, endpoint variants และ response size sequences
```

---

## คำที่ควรใช้

- evidence-based
- reproducible pipeline
- explainable scoring
- inferred unstable window
- endpoint variant
- server-side error pattern
- false-positive control

## คำที่ควรเลี่ยง

- แน่นอน 100% ถ้าไม่มีหลักฐานพอ
- response time สูงจริง ทั้งที่ไม่มี field response time
- 500 ทุกอันคือ hacker
- request เยอะสุดคือ hacker เสมอ

---

## Before presentation quick command

```bash
cd /mnt/c/Users/boony/Desktop/H01/H1/Dorm/code
python3 -m unittest discover -s tests -v
python3 sanity_check.py output
```

ต้องได้:

```text
OK
status=PASS
```
