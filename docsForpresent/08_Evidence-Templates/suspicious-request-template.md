# Suspicious Request Template

## Purpose

ใช้เป็นหลักฐาน HOW

## Table Template

| Timestamp | IP | Method | Endpoint | Status | Red Flags | Score |
|---|---|---|---|---:|---|---:|
| 2024-... | x.x.x.x | GET | `/../../etc/passwd` | 404 | path traversal | 5 |

## Red Flag Reason Examples

| Reason | ความหมาย |
|---|---|
| `path_traversal` | พยายามอ่านไฟล์นอก web root |
| `sqli` | SQL injection probing |
| `xss` | XSS probing |
| `sensitive_endpoint` | เข้าจุดเสี่ยง เช่น admin/config |
| `server_error` | ทำให้เกิด 500 |
| `directory_scan` | 404 หลาย endpoint |

## Explanation Template

```text
Request นี้น่าสงสัยเพราะ endpoint มี ______ ซึ่งเป็น pattern ของ ______ และ status ______ แสดงว่า server ตอบกลับแบบ ______
```
