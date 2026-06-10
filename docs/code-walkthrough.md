# Code Walkthrough — อธิบาย code เป็น story

## 1. `parser.py`

เปลี่ยน raw log line เป็น `LogRequest` ที่มี field ชัดเจน เช่น timestamp, ip, endpoint, status

## 2. `patterns.py`

ตรวจ red flags ต่อ request เช่น SQLi, XSS, path traversal, sensitive endpoint, 404, 500

## 3. `scoring.py`

แปลง red flags เป็นคะแนน พร้อม reasons เพื่อให้ explainable

## 4. `aggregators.py`

รวม request หลายล้านบรรทัดเป็นพฤติกรรมต่อ IP, timeline ราย minute, endpoint summary, และ evidence samples

## 5. `timeline.py`

รวม minute ที่ผิดปกติเป็น incident windows สำหรับตอบ WHEN

## 6. `hidden_bonus.py`

ค้นหา clue เช่น keyword, URL/base64/hex encoded strings, signature-like paths

## 7. `reports.py`

เขียน CSV/JSON/Markdown output แบบ format คงที่ เพื่อใช้กับ dashboard และ presentation

## 8. `runner.py`

ต่อทุก module เข้าด้วยกันเป็น pipeline เดียว
