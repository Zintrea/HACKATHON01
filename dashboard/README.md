# H1 Static Dashboard

## เปิดแบบง่ายที่สุด

ดับเบิลคลิกไฟล์นี้บน Windows:

```text
C:\Users\boony\Desktop\H01\H1\Dorm\code\dashboard\index.html
```

Dashboard นี้ใช้ `data.js` ที่ embed ข้อมูลไว้แล้ว จึงไม่ต้องเปิด server และไม่ต้อง fetch file ผ่าน browser.

## ถ้าต้องการเปิดผ่าน local server

```bash
cd /mnt/c/Users/boony/Desktop/H01/H1/Dorm/code
python3 -m http.server 8000
```

แล้วเปิด:

```text
http://localhost:8000/dashboard/
```

## Regenerate data

ถ้ารัน analyzer ใหม่ ให้ regenerate dashboard data:

```bash
python3 dashboard/build_dashboard_data.py
```

## Sections

- Overview cards
- Top suspicious IPs
- Normal vs variant endpoints
- Suffix clue sequence
- Incident windows
- Evidence examples
- Limitations
