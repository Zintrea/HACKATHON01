# Output Data Dictionary — ความหมายของไฟล์และตัวแปรใน `output/`

> ใช้ไฟล์นี้เวลาต้องอธิบายว่า “ค่าต่าง ๆ มาจากไหน” และ “แต่ละ column แปลว่าอะไร”

Source log:

```text
../../cart_web.log
```

Log format ที่ analyzer ใช้:

```text
timestamp | ip | method | endpoint | status | size
```

Pipeline ที่สร้าง output:

```text
parser.py → patterns.py → scoring.py → aggregators.py → timeline.py → hidden_bonus.py → reports.py
```

---

## 1. `attacker_ips.csv`

ใช้ตอบโจทย์:

```text
WHO ARE THEY?
```

ไฟล์นี้มีเฉพาะ IP ที่ถูกจัดว่าน่าสงสัย ไม่ใช่ทุก IP ใน log

| Column | ความหมาย | มาจากไหน / คำนวณยังไง | วิธีตีความ |
|---|---|---|---|
| `ip` | IP address | field ที่ 2 ของ log | ผู้ต้องสงสัยระดับ IP |
| `label` | ระดับความน่าสงสัย | `classify_ip_score(score)` ใน `scoring.py` | เช่น `suspicious`, `likely_attacker`, `high_confidence_attacker` |
| `score` | คะแนนรวมของ IP | request score รวม + behavior bonus | ใช้จัดอันดับ ไม่ใช่ความจริง 100% |
| `total_requests` | จำนวน request ของ IP นี้ | นับทุก request ที่ IP นี้มี red flag อย่างน้อยบางระดับ | ยิ่งเยอะยิ่งมี behavior pattern |
| `peak_rpm` | request สูงสุดต่อนาทีของ IP | max requests/minute จาก `minute_counts` | ใช้ดู burst/flood; ใน H1 attacker กระจายยาว ไม่ได้ peak สูงมาก |
| `status_404` | จำนวน 404 ของ IP | นับ status = 404 | ถ้าเยอะมากอาจเป็น directory scan |
| `status_403` | จำนวน 403 ของ IP | นับ status = 403 | probing resource ต้องห้าม |
| `status_401` | จำนวน 401 ของ IP | นับ status = 401 | probing resource ที่ต้อง auth |
| `status_500` | จำนวน 500 ของ IP | นับ status 500 | server error ที่สัมพันธ์กับ IP |
| `payload_hits` | จำนวน request ที่มี exploit payload ชัด | flags: `path_traversal`, `sqli`, `xss` | payload ชัด = evidence แข็ง |
| `sensitive_hits` | จำนวน request ไป endpoint เสี่ยง | flag `sensitive_endpoint` | เช่น `/login`, `/admin`, `/api/v1/user` |
| `first_seen` | เวลาแรกที่ IP นี้ปรากฏใน tracked suspicious stats | min timestamp | ใช้ดูเริ่ม active เมื่อไหร่ |
| `last_seen` | เวลาสุดท้ายที่ IP นี้ปรากฏ | max timestamp | ใช้ดู active ยาวแค่ไหน |
| `evidence_count` | จำนวนตัวอย่าง evidence ที่เก็บให้ IP นี้ | จำกัดต่อ IP เพื่อ report อ่านง่าย | ใช้อ้างอิงใน `suspicious_requests.csv` |
| `reasons` | เหตุผลที่ score เพิ่ม | red flags + behavior bonus | ใช้ตอบกรรมการว่า “ทำไม IP นี้น่าสงสัย” |

### ตัวอย่างจาก output จริง

```text
209.103.8.44
label = high_confidence_attacker
status_500 = 283699
reasons = server_error;sensitive_endpoint;high_500_count;many_sensitive_hits
```

คำอธิบาย:

> IP นี้มี server error จำนวนมากและมี sensitive endpoint hits จำนวนมาก จึงถูกจัดเป็น high-confidence attacker

---

## 2. `endpoint_summary.csv`

ใช้ตอบโจทย์:

```text
HOW?
```

ไฟล์นี้คือภาพรวมต่อ endpoint/path แยก status ให้ชัดเจน เพื่อกันสับสนระหว่าง endpoint ปกติและ endpoint variant เช่น `/cart` vs `/cart_`

| Column | ความหมาย | มาจากไหน / คำนวณยังไง | วิธีตีความ |
|---|---|---|---|
| `endpoint` | path ที่ถูกเรียก | field ที่ 4 ของ log | เช่น `/cart`, `/cart_`, `/searchE` |
| `total_requests` | จำนวน request ทั้งหมดของ endpoint | count ต่อ endpoint | ใช้ดู endpoint ไหนโดนเรียกเยอะ |
| `unique_ips` | จำนวน IP ที่เรียก endpoint นี้ | unique IP set ต่อ endpoint | ถ้า unique ต่ำแต่ error สูง อาจเป็นกลุ่มโจมตีจำกัด |
| `status_200` | จำนวน success | status = 200 | endpoint ใช้งานสำเร็จ |
| `status_302` | จำนวน redirect | status = 302 | redirect ถ้ามี |
| `status_304` | จำนวน not modified/cache | status = 304 | มักเจอใน traffic ปกติ |
| `status_401` | unauthorized | status = 401 | probing auth resource |
| `status_403` | forbidden | status = 403 | probing forbidden resource |
| `status_404` | not found | status = 404 | อาจเป็น broken link หรือ scanning |
| `status_500` | internal server error | status = 500 | server crash/error |
| `status_504` | gateway timeout | status = 504 | timeout/service unavailable pattern |
| `status_5xx` | server-side errors รวม | status 500-599 | ใช้ดูผลกระทบฝั่ง server |
| `payload_hits` | exploit payload hits | pattern detector | ถ้ามีคือ HOW แบบ payload |
| `attack_type` | ประเภทสัญญาณหลักของ endpoint | `attack_type_from_flags()` | เช่น `server_error`, `sqli`, `path_traversal`, `normal` |

### Example สำคัญ: `/cart` vs `/cart_`

`/cart`:

```text
total_requests = 2581034
status_200 = 1720806
status_304 = 429968
status_404 = 430260
status_5xx = 0
attack_type = normal
```

`/cart_`:

```text
total_requests = 152835
status_500 = 76402
status_504 = 76433
status_5xx = 152835
attack_type = server_error
```

คำอธิบายสำหรับนำเสนอ:

> `/cart` เป็น endpoint ปกติ มี 200/304/404 และไม่มี 5xx แต่ `/cart_` เป็น endpoint variant ที่มีเฉพาะ 500/504 จึงเป็น suspicious pattern

---

## 3. `incident_windows.csv`

ใช้ตอบโจทย์:

```text
WHEN?
```

ไฟล์นี้ merge ช่วงเวลาที่ timeline มีสถานะไม่ปกติให้เป็น window อ่านง่าย

| Column | ความหมาย | มาจากไหน / คำนวณยังไง | วิธีตีความ |
|---|---|---|---|
| `start_time` | เวลาเริ่ม window | minute แรกที่ไม่ normal | จุดเริ่มผิดปกติ |
| `end_time` | เวลาจบ window | minute สุดท้ายก่อนกลับ normal | จุดจบช่วงผิดปกติ |
| `states_seen` | สถานะที่พบใน window | จาก `system_state` ใน timeline | เช่น `suspicious`, `down_or_crashing` |
| `peak_requests` | request/minute สูงสุดใน window | max `total_requests` | ดู traffic peak |
| `peak_5xx` | 5xx/minute สูงสุดใน window | max `status_5xx` | ดู server-side impact |
| `total_suspicious_requests` | request น่าสงสัยรวมใน window | sum suspicious_requests | ดูความหนาแน่นของ red flags |
| `reason` | เหตุผลที่จัดเป็น incident | hardcoded summary จาก timeline logic | ใช้อธิบายบน slide |

### ข้อควรพูด

เพราะ log ไม่มี response time:

> slow/unstable window เป็นการ infer จาก traffic/error spike ไม่ใช่ response time ที่วัดจริง

---

## 4. `traffic_timeline.csv`

ใช้ตอบโจทย์:

```text
WHEN แบบละเอียดรายนาที
```

ไฟล์นี้ใหญ่เพราะเก็บทุก minute bucket ใช้ทำกราฟ/ตรวจย้อนหลัง ไม่จำเป็นต้องเปิด manual ทั้งไฟล์

| Column | ความหมาย | มาจากไหน / คำนวณยังไง |
|---|---|---|
| `minute` | timestamp ปัดเป็นระดับนาที | `YYYY-MM-DD HH:MM` |
| `total_requests` | request ทั้งหมดในนาทีนั้น | count |
| `status_2xx` | success responses | 200-299 |
| `status_3xx` | redirects/cache responses | 300-399 |
| `status_4xx` | client-side errors | 400-499 |
| `status_5xx` | server-side errors | 500-599 |
| `unique_ips` | unique IPs ใน minute | set ต่อ minute |
| `suspicious_requests` | request ที่ score >= 3 | strong enough red flag |
| `system_state` | state ของ minute | `normal`, `suspicious`, `unstable`, `down_or_crashing` |

---

## 5. `suspicious_requests.csv`

ใช้ตอบโจทย์:

```text
HOW evidence
```

ไฟล์นี้เก็บตัวอย่าง request ที่มี red flags เพื่อใช้เป็นหลักฐาน ไม่ใช่ทุก request ใน log

| Column | ความหมาย | มาจากไหน / คำนวณยังไง |
|---|---|---|
| `line_number` | เลขบรรทัดใน raw log | enumerate ตอนอ่านไฟล์ |
| `timestamp` | เวลา request | field 1 |
| `ip` | IP | field 2 |
| `method` | HTTP method | field 3 |
| `endpoint` | path | field 4 |
| `status` | HTTP status | field 5 |
| `size` | response size | field 6 |
| `score` | request-level score | `score_request()` |
| `reasons` | flags ที่ทำให้ request น่าสงสัย | เช่น `server_error`, `sqli`, `xss` |

ใช้พูดว่า:

> นี่คือตัวอย่าง request จริงจาก log ที่รองรับ conclusion ของเรา

---

## 6. `hidden_bonus_candidates.csv`

ใช้ตอบโจทย์:

```text
HIDDEN BONUS
```

ตอนนี้ไฟล์อาจว่าง แปลว่า rule ปัจจุบันยังไม่เจอ clue ที่มั่นใจ

| Column | ความหมาย |
|---|---|
| `candidate` | ชื่อ/clue candidate |
| `confidence` | low/medium/high |
| `clue_type` | keyword, encoded, prompt_injection_like |
| `decode_method` | none/url/base64/hex |
| `timestamp` | เวลา ถ้าผูกกับ request ได้ |
| `ip` | IP ถ้าผูกกับ request ได้ |
| `endpoint` | endpoint ที่เจอ clue |
| `reason` | ทำไมถือเป็น clue |

---

## 7. `dashboard_data.json`

ใช้ตอบโจทย์:

```text
TELL PEOPLE
```

เป็น JSON รวมข้อมูลสำหรับ web app/dashboard แบบ compact

Top-level keys:

| Key | ความหมาย |
|---|---|
| `overview` | ภาพรวม เช่น parsed lines, suspicious IPs |
| `attackers` | top suspicious IPs จาก `attacker_ips.csv` |
| `timeline` | timeline sample สำหรับ dashboard |
| `incidents` | incident windows |
| `endpoints` | top endpoints |
| `evidence` | suspicious request examples |
| `hidden_bonus` | hidden clue candidates |

หมายเหตุ:

- `traffic_timeline.csv` เก็บ timeline เต็ม
- `dashboard_data.json` ใช้ sampled/compact timeline เพื่อให้ browser เปิดง่าย

---

## 8. `h1_summary.md`

ใช้สำหรับ:

```text
อ่านเร็ว / ทำ slide / presentation
```

ประกอบด้วย:

- overview
- top suspicious IPs
- incident windows
- hidden bonus section
- limitations

ไม่ใช่ไฟล์ data raw แต่เป็น report ที่ generate จาก output หลัก

---

## วิธีอธิบายสั้น ๆ เวลาโดนถามว่า “ค่ามาจากไหน”

```text
ค่าทุกอย่างมาจาก raw log 6 fields คือ timestamp, IP, method, endpoint, status, size
เรา parse เป็น structured request จากนั้น detect red flags ต่อ request, ให้ score, aggregate ตาม IP/endpoint/time, แล้ว export เป็น CSV/JSON/Markdown
```

## ข้อจำกัดสำคัญ

- ไม่มี response time จริง → ห้าม claim latency ตรง ๆ
- ไม่มี User-Agent → บอก tool เช่น sqlmap/curl จาก UA ไม่ได้
- ไม่มี request body → เห็น payload เฉพาะที่อยู่ใน endpoint/path/query
- score เป็น heuristic เพื่อจัดอันดับ evidence ไม่ใช่คำตัดสิน 100%
