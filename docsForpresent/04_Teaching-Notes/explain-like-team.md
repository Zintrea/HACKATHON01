# Explain Like Team — อธิบายให้ทีมเข้าใจเร็ว

## ภาพเปรียบเทียบ

ให้คิดว่าเว็บคือร้านค้า และ log คือกล้องวงจรปิดหน้าร้าน

| ในร้านค้า | ใน log |
|---|---|
| ลูกค้าปกติเดินดูสินค้า | user เข้า `/products` |
| ลูกค้าจ่ายเงิน | user เข้า `/checkout` |
| คนแปลก ๆ ลองเปิดประตูหลังร้าน | attacker เข้า `/admin`, `/.env` |
| คนพยายามงัดตู้เซฟ | SQLi/path traversal |
| คนเข้ามาถี่ผิดมนุษย์ | high request rate |
| ร้านระบบรวน/แคชเชียร์ล่ม | 500 errors spike |

## อธิบายโจทย์ใน 1 นาที

```text
เรามี log เว็บ e-commerce ขนาดใหญ่มาก โจทย์ให้หาว่าใครโจมตีเว็บ เกิดตอนไหน โจมตียังไง และต้องทำ dashboard ให้คนอื่นเข้าใจ โดยห้ามอ่าน manual ทั้งไฟล์ ดังนั้นเราต้องเขียน script เพื่อ parse log ทุกบรรทัด แล้วสรุปเป็น IP risk score, incident timeline, attack pattern และ hidden clue
```

## สิ่งที่ทีมต้องเข้าใจ

1. log หนึ่งบรรทัด = request หนึ่งครั้ง
2. IP หนึ่งตัว = ผู้ต้องสงสัยหนึ่งราย/กลุ่ม
3. endpoint = สิ่งที่เขาพยายามเข้าถึง
4. status = server ตอบว่าเกิดอะไร
5. pattern สำคัญกว่าบรรทัดเดี่ยว
6. evidence สำคัญกว่า guess

## Example แบบง่าย

### User ปกติ

```text
GET /products 200
GET /cart 200
POST /checkout 200
```

เล่าได้ว่า: เดินดูสินค้า → ใส่ตะกร้า → จ่ายเงิน

### Attacker

```text
GET /.env 404
GET /config.php 404
GET /../../etc/passwd 404
GET /search?q=' OR 1=1-- 500
```

เล่าได้ว่า: หาไฟล์ลับ → ลอง path traversal → ลอง SQL injection → ทำ server error

## ประโยคจำง่าย

```text
เราไม่ได้ถามว่า request ไหนแปลก แต่ถามว่า IP ไหนมีพฤติกรรมเหมือนโจมตีซ้ำ ๆ และเกิดผลกับระบบตอนไหน
```
