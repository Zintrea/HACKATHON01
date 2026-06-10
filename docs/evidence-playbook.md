# Evidence Playbook — วิธีไล่หลักฐานจาก output

> ใช้ไฟล์นี้เป็นขั้นตอนตอบคำถาม “พิสูจน์ยังไงว่า IP นี้เป็นคนร้าย?”

## หลักคิด

อย่าดูไฟล์เดียวแล้วฟันธง ให้ไล่หลักฐานแบบนี้:

```text
attacker_ips.csv
→ endpoint_summary.csv
→ suspicious_requests.csv
→ incident_windows.csv / traffic_timeline.csv
→ raw log sample ถ้าต้องการยืนยัน
```

---

## Playbook A: พิสูจน์ WHO ARE THEY

### Step 1 — เปิด `attacker_ips.csv`

ดู columns:

```text
ip, label, score, total_requests, status_500, sensitive_hits, reasons
```

เลือก IP ที่ label เป็น:

```text
high_confidence_attacker
```

### Step 2 — อ่าน reasons

ตัวอย่าง:

```text
server_error;sensitive_endpoint;high_500_count;many_sensitive_hits
```

แปลว่า:

- มี server error จำนวนมาก
- มีการยิง endpoint เสี่ยง/variant
- มี 500 จำนวนมากในระดับ IP

### Step 3 — เชื่อมกับ evidence

ไปที่:

```text
suspicious_requests.csv
```

หา IP เดียวกัน แล้วดูตัวอย่าง request:

```text
timestamp, ip, method, endpoint, status, score, reasons
```

คำพูดนำเสนอ:

> IP นี้ไม่ใช่แค่ request เยอะ แต่มี request ที่เกิด server_error ซ้ำ ๆ บน endpoint pattern เดิม จึงมี evidence เป็นบรรทัดจริงจาก log

---

## Playbook B: พิสูจน์ HOW — โจมตียังไง

### Step 1 — เปิด `endpoint_summary.csv`

ดู endpoint ที่มี:

```text
status_5xx สูง
attack_type = server_error
unique_ips ต่ำ/จำกัด
```

ใน H1 มี pattern สำคัญ:

```text
/cart_     → 500/504 ทั้งหมด
/search_   → 500/504 ทั้งหมด
/products_ → 500/504 ทั้งหมด
```

### Step 2 — เปรียบเทียบ endpoint ปกติกับ variant

ตัวอย่าง:

| endpoint | 200 | 304 | 404 | 5xx | interpretation |
|---|---:|---:|---:|---:|---|
| `/cart` | มีเยอะ | มี | มี | 0 | normal endpoint |
| `/cart_` | 0 | 0 | 0 | 152835 | suspicious variant / server error trigger |

คำพูดนำเสนอ:

> จุดสำคัญคือ endpoint ปกติไม่ได้พัง แต่ endpoint variant ที่เติม suffix เช่น `_` ทำให้เกิด 500/504 ทั้งหมด จึงเป็น attack pattern ที่ชัดกว่าแค่ดู `/cart` เฉย ๆ

---

## Playbook C: พิสูจน์ WHEN — เกิดตอนไหน

### Step 1 — เปิด `incident_windows.csv`

ดู:

```text
start_time, end_time, states_seen, peak_5xx
```

ถ้า `states_seen` มี:

```text
down_or_crashing
```

แปลว่า window นั้นมี 5xx spike / server-side error pattern

### Step 2 — ถ้าต้องการละเอียด เปิด `traffic_timeline.csv`

ดูรายนาที:

```text
minute,total_requests,status_5xx,suspicious_requests,system_state
```

คำพูดนำเสนอ:

> เราไม่ได้เดาเวลา incident แต่ bucket log เป็นรายนาที แล้ว merge นาทีที่ไม่ normal เป็น incident window

---

## Playbook D: ตรวจว่าข้อมูลไม่หลอกเรา

ก่อนเชื่อ output ให้รัน:

```bash
cd /mnt/c/Users/boony/Desktop/H01/H1/Dorm/code
python3 sanity_check.py output
```

ผลควรเป็น:

```text
status=PASS
```

สิ่งที่ sanity check ดูให้:

- output files ครบ
- CSV columns ครบ
- dashboard JSON อ่านได้
- `/cart` กับ `/cart_` แยกกันจริง
- `attacker_ips.csv` มี suspicious rows

---

## Playbook E: ถ้ากรรมการถามว่า “ทำไมไม่ใช่ user ปกติ?”

ตอบด้วย 3 ชั้น:

1. **Pattern** — ไม่ใช่ request เดี่ยว แต่เป็นพฤติกรรมซ้ำ
2. **Impact** — request เหล่านี้สัมพันธ์กับ 500/504
3. **Separation** — endpoint ปกติ (`/cart`) ไม่พัง แต่ variant (`/cart_`) พังทั้งหมด

คำตอบตัวอย่าง:

```text
ถ้าเป็น user ปกติ เราคาดว่าจะเห็น traffic บน /cart ที่มี 200/304/404 ปะปน แต่สิ่งที่น่าสงสัยคือ /cart_ ซึ่งเป็น variant path มีเฉพาะ 500/504 และมาจาก IP กลุ่มเดียวกัน 19 ตัว จึงไม่ใช่ normal user journey
```

---

## Playbook F: Hidden Bonus

เปิด:

```text
hidden_bonus_candidates.csv
```

ถ้าว่าง ให้พูดว่า:

```text
เรา search ด้วย keyword/encoding heuristic แล้ว แต่ยังไม่พบ clue ที่มั่นใจ จึงไม่ฟันธง hidden bonus เกินหลักฐาน
```

ถ้าจะ hunt ต่อ ให้โฟกัส:

- endpoint variants: `_`, `E`, `A`, `S`, `N`
- response latency sequence (`latency_ms`)
- IP attacker group 19 ตัว
- lines รอบ marker `hackathon#1`

---

## Checklist ก่อนนำหลักฐานไปใส่ slide

- [ ] มี IP จาก `attacker_ips.csv`
- [ ] มี endpoint pattern จาก `endpoint_summary.csv`
- [ ] มีเวลา incident จาก `incident_windows.csv`
- [ ] มี request example จาก `suspicious_requests.csv`
- [ ] sanity check ผ่าน
- [ ] ไม่ claim response time จริง เพราะ log ไม่มี field นั้น
