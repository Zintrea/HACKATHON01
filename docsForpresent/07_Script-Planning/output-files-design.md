# Output Files Design — ออกแบบไฟล์ผลลัพธ์

## 1. `attacker_ips.csv`

ใช้ตอบ WHO

Columns:

```text
ip,label,score,total_requests,peak_rpm,status_404,status_403,status_500,payload_hits,sensitive_hits,first_seen,last_seen,evidence_count,reasons
```

Example:

```text
6.6.6.6,high_confidence_attacker,18,2500,900,1200,20,80,15,300,2024-06-10 05:10:00,2024-06-10 05:18:00,5,"path_traversal;high_404;incident_overlap"
```

## 2. `traffic_timeline.csv`

ใช้ตอบ WHEN

Columns:

```text
minute,total_requests,status_2xx,status_3xx,status_4xx,status_5xx,unique_ips,suspicious_requests,system_state
```

## 3. `incident_windows.csv`

สรุปช่วงผิดปกติ

Columns:

```text
start_time,end_time,state,peak_requests,peak_5xx,top_ips,top_endpoints,reason
```

## 4. `endpoint_summary.csv`

ใช้ตอบ HOW

Columns:

```text
endpoint,total_requests,unique_ips,status_404,status_500,payload_hits,attack_type
```

## 5. `suspicious_requests.csv`

ใช้เป็น evidence

Columns:

```text
timestamp,ip,method,endpoint,status,size,score,reasons
```

## 6. `hidden_bonus_candidates.csv`

ใช้ตอบ HIDDEN BONUS

Columns:

```text
candidate,confidence,clue_type,decode_method,timestamp,ip,endpoint,reason
```

## 7. `h1_summary.md`

ควรเป็น report อ่านเร็ว:

```text
# H1 Incident Summary
- Source log
- Methodology
- Key findings
- Attacker IPs
- Incident timeline
- Attack patterns
- Hidden bonus
- Limitations
```

## 8. `dashboard_data.json`

รวมข้อมูลให้ web app ใช้ง่าย เช่น:

```json
{
  "overview": {},
  "attackers": [],
  "timeline": [],
  "incidents": [],
  "evidence": [],
  "hidden_bonus": []
}
```
