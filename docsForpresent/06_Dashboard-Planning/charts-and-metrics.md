# Charts and Metrics — กราฟและตัวชี้วัดที่ควรมี

## 1. Traffic Timeline

ตอบ: ระบบเริ่มผิดปกติตอนไหน

Data:

```text
minute,total_requests
```

Interpretation:

- spike สูงกว่าปกติ = suspicious/unstable
- spike ยาว = sustained attack

## 2. Error Timeline

ตอบ: ระบบล่ม/ไม่เสถียรตอนไหน

Data:

```text
minute,status_4xx,status_5xx
```

Interpretation:

- 4xx spike = scanning/probing
- 5xx spike = server instability/crash

## 3. Top Suspicious IPs

ตอบ: ใครคือคนร้าย

Data:

```text
ip,score,total_requests,payload_hits,status_500,peak_rpm
```

Chart:

- horizontal bar by score

## 4. Attack Type Distribution

ตอบ: โจมตียังไง

Data:

```text
attack_type,count
```

Types:

- path traversal
- SQL injection
- XSS
- sensitive scan
- high-rate flood
- crash probing

## 5. Endpoint Summary

ตอบ: จุดไหนถูกโจมตี

Data:

```text
endpoint,total_requests,unique_ips,status_500,payload_hits
```

## 6. System State Timeline

ตอบ: สถานะระบบแต่ละช่วงเวลา

Data:

```text
minute,state,reason
```

States:

- normal
- suspicious
- unstable
- down_or_crashing

## Metric Definitions

| Metric | นิยาม |
|---|---|
| `peak_rpm` | requests สูงสุดของ IP ใน 1 นาที |
| `payload_hits` | จำนวน request ที่มี exploit pattern |
| `sensitive_hits` | จำนวน request ไป endpoint เสี่ยง |
| `incident_overlap` | IP active ใน incident window |
| `error_rate` | errors / total requests |

## Presentation Tip

ก่อนโชว์กราฟ ให้บอกว่ากราฟตอบอะไร:

```text
กราฟนี้ตอบ WHEN โดยแสดงว่าช่วง 05:12 requests และ 5xx spike พร้อมกัน
```
