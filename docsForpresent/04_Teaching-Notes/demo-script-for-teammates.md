# Demo Script For Teammates — สคริปต์พูดอธิบายให้ทีมฟัง

> ใช้เป็นบทพูด ไม่ใช่ lab

## Opening

```text
โจทย์นี้ให้เราหาคนร้ายจาก access log ขนาดใหญ่มาก ห้ามอ่าน manual ทั้งไฟล์ เพราะช้าและพลาดง่าย เราเลยต้องทำ script ที่อ่านทุกบรรทัด สรุปพฤติกรรม แล้วบอกว่า IP ไหนน่าสงสัย เกิดช่วงเวลาไหน และโจมตียังไง
```

## Explain Log Line

```text
หนึ่งบรรทัดของ log คือหนึ่ง request มีเวลา, IP, method, path, status และ size เช่น user เข้า /products แล้ว server ตอบ 200
```

## Explain Normal vs Attacker

```text
user ปกติมักเดินตาม flow เช่น products → cart → checkout แต่ attacker จะลอง path แปลก ๆ เช่น /.env, /admin, /../../etc/passwd หรือส่ง payload SQLi/XSS
```

## Explain Why Script

```text
ถ้า log มี 21 ล้านบรรทัด เราอ่านเองไม่ได้ เราต้องให้ script aggregate เช่น IP ไหนยิงกี่ครั้ง, status 404/500 เท่าไหร่, peak request/minute เท่าไหร่, และมี payload แปลกกี่ครั้ง
```

## Explain Scoring

```text
เราให้คะแนนความน่าสงสัยจากหลาย red flags ไม่ใช่จากกฎเดียว เช่น payload ชัดได้คะแนนสูง, 500 ได้คะแนน, sensitive endpoint ได้คะแนน, request rate สูงได้คะแนน แล้วรวมเป็น risk score ต่อ IP
```

## Explain Timeline

```text
เพื่อหาว่าเกิดตอนไหน เราแบ่ง log เป็นรายนาที แล้วดูว่า traffic กับ error เริ่ม spike ตอนไหน ช่วงนั้นคือ incident window
```

## Explain Hidden Bonus

```text
ส่วน hidden bonus คือการหา clue ที่คนร้ายทิ้งไว้ เช่น signature, username, path แปลก หรือ encoded text เราต้องเก็บ evidence ว่าเจอที่บรรทัดไหนและ decode ยังไง
```

## Closing

```text
สุดท้าย dashboard จะทำให้คนดูเห็นภาพว่าใครโจมตี เมื่อไหร่ ระบบกระทบยังไง และหลักฐานคืออะไร โดยไม่ต้องเปิด raw log เอง
```
