# 🔍 Nexus Cart Investigation Write-up

## 📌 Objective

วิเคราะห์ไฟล์ `cart_web.log` เพื่อค้นหาข้อความหรือข้อมูลที่ถูกซ่อนอยู่ภายใน Log ของระบบ Nexus Cart

---

## 🕵️ Step 1 — ค้นหารูปแบบที่ผิดปกติใน URL

จากการตรวจสอบ Log พบว่า URL หลายรายการมี **ตัวอักษรพิมพ์ใหญ่ (A–Z)** ปรากฏอยู่ท้าย Path เช่น

```text
/productsG
/indexG.html
/cartM
/searchM
```

จึงตั้งสมมติฐานว่าตัวอักษรเหล่านี้อาจถูกใช้เป็นช่องทางซ่อนข้อความ (Hidden Message)

---

## ⚙️ Step 2 — ดึงตัวอักษรพิมพ์ใหญ่จาก URL

ใช้ `awk` เพื่อดึงตัวอักษรพิมพ์ใหญ่ที่อยู่ท้าย URL และบันทึกเฉพาะจุดที่มีการเปลี่ยนตัวอักษร (Transition)

```bash
awk -F' \| ' '
{
    if (match($4,/([A-Z])([.]html)?$/)) {
        c = substr($4,RSTART,1)

        if (c != prev) {
            print $1 " -> " c
            prev = c
        }
    }
}' cart_web.log > transitions.txt
```

ผลลัพธ์ตัวอย่าง

```text
2024-06-16 10:25:29 -> N
2024-06-17 00:00:03 -> E
2024-06-18 00:00:00 -> X
2024-06-19 00:00:05 -> U
2024-06-20 00:00:03 -> S
```

---

## 📊 Step 3 — ตรวจสอบจำนวน Transition

นับจำนวนรายการที่ถูกดึงออกมา

```bash
wc -l transitions.txt
```

ผลลัพธ์

```text
238 transitions.txt
```

พบว่ามีทั้งหมด **238 Transition**

---

## 🔡 Step 4 — รวมตัวอักษรเป็นข้อความ

ดึงเฉพาะตัวอักษรและต่อกันเป็น String เดียว

```bash
awk '{print $NF}' transitions.txt | tr -d '\n'
```

ผลลัพธ์

```text
NEXUSCARTWASTOEASYOURSYSTEMWASALREADYFALINGAPARTBEFOREYOUEVENREALIZEDITWASMEGOEMON...
```

---

## 📈 Step 5 — วิเคราะห์ความถี่ของตัวอักษร

ตรวจสอบความถี่เพื่อยืนยันว่าเป็นข้อความภาษาอังกฤษ

```bash
awk '{print $NF}' transitions.txt \
| sort \
| uniq -c \
| sort -nr
```

ผลลัพธ์บางส่วน

```text
35 E
33 A
21 S
18 R
16 O
15 T
```

รูปแบบความถี่สอดคล้องกับข้อความภาษาอังกฤษทั่วไป

---

## 📍 Step 6 — บันทึกเลขบรรทัดจริงใน Log

เพื่อใช้อ้างอิงตำแหน่งของแต่ละ Transition ในไฟล์ต้นฉบับ

```bash
awk -F' \| ' '
{
    if (match($4,/([A-Z])([.]html)?$/)) {
        c = substr($4,RSTART,1)

        if (c != prev) {
            print NR, $1, c
            prev = c
        }
    }
}' cart_web.log > transitions_nr.txt
```

ตัวอย่างผลลัพธ์

```text
20663681 2026-05-23 21:13:28 D
20690022 2026-05-25 00:00:04 I
20713587 2026-05-26 00:00:01 T
20842948 2026-05-30 14:33:48 W
20852282 2026-05-31 00:00:02 A
20875688 2026-06-01 00:00:01 S
21118791 2026-06-09 00:00:00 M
21142208 2026-06-10 00:00:03 E
```

---

## 🧩 Decoded Message

เมื่อนำตัวอักษรทั้งหมดมาเรียงตามลำดับเวลา จะได้ข้อความ

```text
NEXUSCARTWASTOEASYOURSYSTEMWASALREADYFALINGAPARTBEFOREYOUEVENREALIZEDITWASMEGOEMON
```

จัดรูปแบบให้อ่านง่าย

```text
NEXUS CART WAS TO EASY
YOUR SYSTEM WAS ALREADY FALING APART
BEFORE YOU EVEN REALIZED IT WAS ME
GOEMON
```

และเมื่อแก้คำสะกดผิดที่น่าจะเป็นความตั้งใจของผู้ทิ้งข้อความ

```text
NEXUS CART WAS TOO EASY.
YOUR SYSTEM WAS ALREADY FALLING APART
BEFORE YOU EVEN REALIZED IT WAS ME.

— GOEMON
```

---

## ✅ Conclusion

พบการซ่อนข้อความลับไว้ใน URL ของระบบ โดยใช้ตัวอักษรพิมพ์ใหญ่ที่ปรากฏท้าย Path ของ Request

การวิเคราะห์อาศัย

* Pattern Analysis
* Log Parsing ด้วย AWK
* Transition Tracking
* Timeline Reconstruction

ข้อความที่ถูกซ่อนไว้คือ

> **NEXUS CART WAS TOO EASY.**
>
> **YOUR SYSTEM WAS ALREADY FALLING APART**
>
> **BEFORE YOU EVEN REALIZED IT WAS ME.**
>
> **— GOEMON**
