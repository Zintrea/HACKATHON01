# Scoring Rules — คะแนนความน่าสงสัยคิดยังไง

> ใช้ไฟล์นี้ตอบคำถามกรรมการว่า “ทำไม IP นี้ถูกจัดเป็น attacker?” และ “score มาจากไหน?”

## แนวคิดหลัก

เราไม่ฟันธงจาก signal เดียว เช่น:

- 404 ครั้งเดียว ≠ hacker
- 500 ครั้งเดียว ≠ hacker
- request เยอะอย่างเดียว ≠ hacker

เราใช้แนวคิด:

```text
request red flags → request score → aggregate by IP → behavior bonus → final IP score → label
```

---

## 1. Request-level score

อยู่ใน:

```text
h1_analyzer/scoring.py
```

| Red Flag | คะแนน | เหตุผล |
|---|---:|---|
| `path_traversal` | +5 | พยายามอ่านไฟล์นอก web root เช่น `../`, `/etc/passwd` |
| `sqli` | +5 | SQL injection เช่น `UNION`, `SELECT`, `OR 1=1` |
| `xss` | +5 | XSS เช่น `<script>`, `javascript:` |
| `sensitive_endpoint` | +3 | ยิง endpoint เสี่ยง เช่น `/admin`, `/login`, `/api/v1/user` |
| `server_error` | +4 | status 500-599 แปลว่า server-side error |
| `forbidden_or_unauthorized` | +2 | status 401/403 แปลว่าเข้าของต้องห้าม/ต้อง auth |
| `not_found` | +1 | status 404 เป็น weak clue อาจ scan หรือ broken link |

### ทำไม 404 ได้แค่ +1

เพราะ 404 อาจเกิดจาก:

- user พิมพ์ URL ผิด
- broken link
- frontend asset หาย
- bot scan

ดังนั้น 404 เดี่ยว ๆ เป็น clue อ่อน ต้องดูจำนวน/endpoint/rate ประกอบ

### ทำไม 500/504 สำคัญ

500/504 เป็น server-side error ถ้าเกิดซ้ำจาก IP กลุ่มเดิมหรือ endpoint variant แปลก ๆ เช่น `/cart_`, `/searchE` จะชี้ว่า request pattern นั้นสัมพันธ์กับระบบล้ม/ไม่เสถียร

---

## 2. IP-level behavior bonus

อยู่ใน:

```text
h1_analyzer/aggregators.py
```

หลังจากรวม request ต่อ IP แล้ว analyzer เพิ่ม bonus จากพฤติกรรมรวม:

| Behavior | คะแนน | ความหมาย |
|---|---:|---|
| `high_404_count` | +5 | IP มี 404 จำนวนมาก อาจ scan |
| `moderate_404_count` | +3 | IP มี 404 ระดับกลาง |
| `high_500_count` | +4 | IP ทำให้เกิด 500 จำนวนมาก |
| `has_500_error` | +2 | IP มี 500 อย่างน้อยบางส่วน |
| `high_peak_rpm` | +4 | request/minute สูงมาก |
| `moderate_peak_rpm` | +2 | request/minute สูงกว่าปกติ |
| `many_sensitive_hits` | +3 | ยิง endpoint เสี่ยงหลายครั้ง |

## 3. Final label

อยู่ใน:

```text
h1_analyzer/scoring.py
```

| Score | Label | ความหมาย |
|---:|---|---|
| 0-2 | `normal` | ไม่มี evidence พอ |
| 3-6 | `suspicious` | มี red flag บ้าง |
| 7-12 | `likely_attacker` | หลาย red flags หรือ behavior น่าสงสัย |
| 13+ | `high_confidence_attacker` | evidence แข็ง / pattern ชัด |

## 4. ตัวอย่างจาก H1 จริง

Top attacker เช่น:

```text
IP: 209.103.8.44
label: high_confidence_attacker
status_500: 283699
reasons: server_error;sensitive_endpoint;high_500_count;many_sensitive_hits
```

อธิบายว่า:

> IP นี้ถูกจัดเป็น high-confidence เพราะมี server error จำนวนมาก และสัมพันธ์กับ sensitive/variant endpoints จำนวนมาก ไม่ใช่เพราะ request count อย่างเดียว

## 5. จุดที่ต้องพูดอย่างระวัง

### Score ไม่ใช่ truth 100%

ควรพูดว่า:

```text
score เป็น explainable heuristic เพื่อจัดอันดับความน่าสงสัย และทุก conclusion ต้องอ้าง evidence rows ประกอบ
```

### 500 ไม่ได้แปลว่า attacker เสมอ

ควรพูดว่า:

```text
500 เป็น server-side impact signal ถ้าเกิดซ้ำจำนวนมากจาก IP/endpoint pattern เดิม จะเพิ่ม confidence ว่าเกี่ยวข้องกับ incident
```

### Response time ไม่มี

ควรพูดว่า:

```text
เรา infer unstable/down windows จาก 5xx และ traffic pattern ไม่ได้วัด response time จริง เพราะ log ไม่มี field response time
```

## 6. วิธี defend scoring ต่อกรรมการ

ถ้าถามว่า “ทำไม threshold เป็นแบบนี้?”

ตอบ:

```text
เราให้ exploit payload ที่ชัด เช่น SQLi/path traversal/XSS คะแนนสูง เพราะมี intention ชัด ส่วน signal ที่ false positive ได้ เช่น 404 ให้คะแนนต่ำ แล้วค่อยรวมกับ behavior-level evidence เช่น high 500 count, many sensitive hits และ incident overlap
```

ถ้าถามว่า “ทำไม IP ที่ยิงไม่เร็วมากก็เป็น attacker?”

ตอบ:

```text
เพราะ attack pattern ของ H1 ดูเหมือน distributed long-running error trigger มากกว่า high-RPM flood ค่า peak_rpm จึงไม่สูงมาก แต่ 500/504 จำนวนมากและ endpoint variants ชัดเจนกว่า
```
