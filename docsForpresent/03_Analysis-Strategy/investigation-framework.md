# Investigation Framework — วิธีคิดแบบนักสืบ Log

## Pipeline หลัก

```text
1. Parse raw log
2. Validate fields
3. Extract features per request
4. Aggregate by IP
5. Aggregate by time window
6. Detect red flags
7. Score IPs
8. Identify incident windows
9. Find hidden bonus clues
10. Export data for dashboard/report
```

## Step 1: Parse raw log

ต้องแยก field ให้ถูก:

```text
timestamp | ip | method | endpoint | status | size
```

ถ้าบรรทัด parse ไม่ได้ ให้เก็บไว้ใน `parse_errors.csv` ไม่ควรทิ้งเงียบ ๆ

## Step 2: Feature per request

แต่ละ request ควรมี flags เช่น:

| Feature | ตัวอย่าง |
|---|---|
| `is_path_traversal` | endpoint มี `../` |
| `is_sqli` | endpoint มี `UNION SELECT` |
| `is_xss` | endpoint มี `<script>` |
| `is_sensitive_endpoint` | endpoint มี `/admin`, `/.env` |
| `is_error_4xx` | status 400-499 |
| `is_error_5xx` | status 500-599 |
| `minute_bucket` | timestamp ปัดลงเป็นนาที |

## Step 3: Aggregate by IP

ตาราง IP ควรมี:

```text
ip,total_requests,status_404,status_403,status_500,malicious_payloads,sensitive_hits,peak_rpm,first_seen,last_seen,score,label
```

## Step 4: Aggregate by time

ตาราง timeline ควรมี:

```text
minute,total_requests,status_4xx,status_5xx,unique_ips,top_ip,top_endpoint,system_state
```

## Step 5: Evidence examples

อย่ามีแค่ score ต้องเก็บตัวอย่าง request เช่น top 5 suspicious lines ต่อ IP

ตัวอย่าง:

```text
2024-06-10 05:13:00 | 6.6.6.6 | GET | /../../etc/passwd | 404 | 20
```

## Step 6: Classification

แนะนำ label:

| Label | ความหมาย |
|---|---|
| `normal` | ไม่มี red flag สำคัญ |
| `suspicious` | มีบาง red flags แต่ยังไม่พอ |
| `likely_attacker` | มีหลาย red flags หรือ rate สูง |
| `high_confidence_attacker` | payload ชัด + incident correlation |

## Mental Model สำหรับใบ

ให้นึกว่า log analysis คือการทำคดี:

| งานนักสืบ | งาน log analysis |
|---|---|
| คนต้องสงสัย | IP address |
| พฤติกรรม | request pattern |
| เวลาเกิดเหตุ | incident window |
| อาวุธ | payload / endpoint |
| หลักฐาน | request lines / stats |
| motive/signature | hidden bonus clue |

## ประโยคสอนทีม

> เราไม่ได้อ่าน log เพื่อหาบรรทัดแปลก แต่สร้างระบบที่สรุปพฤติกรรมทั้งหมด แล้วค่อยใช้ evidence ตัดสินว่าใครคือ attacker
