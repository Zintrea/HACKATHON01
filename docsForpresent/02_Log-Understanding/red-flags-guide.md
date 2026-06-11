# Red Flags Guide — จุดสังเกตการโจมตี

## Red Flag ไม่ใช่ Proof เดี่ยว ๆ

Red flag คือสัญญาณเตือน ต้องรวมหลายสัญญาณเพื่อสร้าง confidence

## 1. Malicious Payloads

### Path Traversal

พยายามอ่านไฟล์นอก web root:

```text
../
..%2f
%2e%2e
/etc/passwd
/proc/self/environ
C:\Windows\win.ini
```

ตัวอย่าง:

```text
GET | /download?file=../../../../etc/passwd | 404
```

ความหมาย: คนร้ายลองดูว่า endpoint download อ่านไฟล์ระบบได้ไหม

### SQL Injection

keyword/pattern ที่ควรหา:

```text
'
%27
UNION
SELECT
OR 1=1
--
/*
SLEEP(
```

ตัวอย่าง:

```text
GET | /search?q=' OR 1=1-- | 500
```

ความหมาย: พยายามทำให้ SQL query หลุด logic หรือ crash

### XSS

keyword/pattern:

```text
<script>
%3Cscript
javascript:
onerror=
onload=
```

ตัวอย่าง:

```text
GET | /search?q=<script>alert(1)</script> | 200
```

ความหมาย: ลองฝัง JavaScript ในหน้าเว็บ

## 2. Status Code Anomalies

| Status | ถ้าเจอแบบไหนน่าสงสัย |
|---|---|
| 404 | IP เดียวลองหลาย path ที่ไม่มีจริง |
| 401/403 | IP เดียว probe protected/admin paths |
| 500 | เกิดซ้ำหลัง payload แปลก หรือ spike ในช่วง attack |

## 3. High Request Rate

มนุษย์กดเว็บไม่ได้ถี่ระดับหลายร้อย/พัน request ต่อนาที

ตัวอย่าง evidence:

```text
IP 7.7.7.7 peak_rpm = 950 requests/minute
normal median IP peak_rpm = 8 requests/minute
```

แปลว่า IP นี้เป็น outlier ชัด

## 4. Sensitive Endpoints

กลุ่ม path ที่น่าสงสัย:

```text
/admin
/admin_dashboard
/login
/api/v1/users
/.env
/config
/config.php
/backup
/backup.zip
/db.sql
/phpmyadmin
/wp-admin
```

แต่ต้องระวัง: `/login` เป็น endpoint ปกติได้ ถ้า POST เยอะผิดปกติหรือ fail เยอะ จึงน่าสงสัย

## 5. Hidden/Signature Clues

คำที่ควร search:

```text
hackathon
flag
secret
signature
name
realname
admin
root
owned
pwned
by
007
```

และอย่าลืม encoded clues:

- base64-like string
- hex string
- path initials
- response size sequence
- endpoint suffix ที่สะกดเป็นคำ

## ตัวอย่างการรวม Red Flags

```text
IP 5.5.5.5
- 404 = 1,430 ครั้ง
- 500 = 55 ครั้ง
- malicious payload = 21 ครั้ง
- sensitive endpoints = 300 ครั้ง
- peak_rpm = 800
```

สรุปได้ว่า high-confidence attacker เพราะมีหลาย red flags พร้อมกัน
