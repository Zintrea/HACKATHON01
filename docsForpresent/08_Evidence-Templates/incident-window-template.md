# Incident Window Template

## Purpose

ใช้สรุป WHEN & system state

## Table Template

| Window | State | Start | End | Peak Requests/min | Peak 5xx/min | Top IPs | Main Evidence |
|---:|---|---|---|---:|---:|---|---|
| 1 | unstable | 05:10 | 05:15 | 4500 | 300 | x.x.x.x | traffic spike + 5xx increase |

## Explanation Template

```text
ช่วง ______ ถึง ______ ถูกจัดเป็น ______ เพราะ requests เพิ่มจาก baseline ______ เป็น ______ และ 5xx เพิ่มจาก ______ เป็น ______ โดย top IP ในช่วงนี้คือ ______
```

## Safe Wording

ถ้าไม่มี response time:

```text
เรา infer ว่าเป็นช่วง unstable จาก traffic/error spike ไม่ได้วัด response time โดยตรง
```
