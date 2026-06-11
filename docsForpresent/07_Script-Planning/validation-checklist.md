# Validation Checklist — เช็กวิเคราะห์ให้ไม่พัง

## ก่อนรัน

- [ ] ยืนยันว่า source log คือ `H1/cart_web.log`
- [ ] ไม่แก้ไข raw log
- [ ] script อ่านแบบ streaming
- [ ] output path แยกจาก raw log

## หลัง parse

- [ ] parsed line count สมเหตุสมผล
- [ ] malformed line count ถูก report
- [ ] status counts รวมเท่ากับ parsed lines
- [ ] timestamp parse ได้
- [ ] IP format ส่วนใหญ่ถูกต้อง

## หลัง scoring

- [ ] top attacker IP มี evidence lines
- [ ] score reasons อ่านเข้าใจ
- [ ] ไม่มีการใช้ signal เดียวฟันธง
- [ ] threshold อธิบายได้

## หลัง timeline

- [ ] incident windows มี start/end
- [ ] state แต่ละ window มี reason
- [ ] ถ้าพูดเรื่องหน่วง ใช้คำว่า inferred ถ้าไม่มี response time

## หลัง hidden bonus

- [ ] candidate มี source line/context
- [ ] decode method ระบุชัด
- [ ] confidence ไม่เกินหลักฐาน

## ก่อนนำเสนอ

- [ ] dashboard ตอบ WHO/WHEN/HOW/BONUS ครบ
- [ ] report มี limitations
- [ ] slides มี evidence ไม่ใช่แค่ conclusion
- [ ] เตรียมตอบ false positive questions
