# Attacker IP Table Template

## Purpose

ใช้สรุป WHO ARE THEY

## Table Template

| Rank | IP | Label | Score | Total Req | Peak RPM | 404 | 403 | 500 | Payload Hits | Sensitive Hits | Key Reasons |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `x.x.x.x` | high_confidence_attacker | 18 | 2500 | 900 | 1200 | 20 | 80 | 15 | 300 | path traversal, high 404, incident overlap |

## Explanation Template

```text
IP ______ ถูกจัดเป็น ______ เพราะมี score ______ จาก evidence หลักคือ ______, ______, และ ______ โดย active ในช่วง ______ ซึ่งตรงกับ incident window
```

## Evidence Snippet Template

```text
timestamp | ip | method | endpoint | status | reason
```
