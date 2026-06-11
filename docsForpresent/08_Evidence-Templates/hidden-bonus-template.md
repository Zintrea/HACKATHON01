# Hidden Bonus Template

## Purpose

ใช้บันทึก clue สำหรับชื่อจริง/ลายเซ็นคนร้าย

## Candidate Template

| Field | Value |
|---|---|
| Candidate |  |
| Confidence | low/medium/high |
| Clue Type | path/query/base64/hex/size-sequence/signature |
| Decode Method | none/url/base64/hex/ascii |
| Timestamp |  |
| IP |  |
| Endpoint |  |
| Reason |  |

## Explanation Template

```text
เราเจอ clue แบบ ______ จาก IP ______ ช่วง ______ ใน endpoint ______ หลังใช้วิธี ______ ได้ candidate ว่า ______ โดย confidence ระดับ ______ เพราะ ______
```

## Confidence Guide

| Confidence | เงื่อนไข |
|---|---|
| low | string แปลก แต่ยังไม่สัมพันธ์กับ attacker |
| medium | clue มาจาก suspicious IP หรือช่วง incident |
| high | clue มาจาก high-confidence attacker + decode/meaning ชัด + มีซ้ำ/context รองรับ |
