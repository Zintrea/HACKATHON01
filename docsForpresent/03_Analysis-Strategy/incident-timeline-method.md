# Incident Timeline Method — หา WHEN & HOW

## เป้าหมาย

ตอบโจทย์:

- ระบบเริ่มผิดปกติตอนไหน
- ช่วงไหนระบบหน่วงหรือไม่เสถียร
- ช่วงไหนระบบล่มหรือให้บริการไม่ได้
- pattern การโจมตีเป็นยังไง

## วิธีทำ Timeline

แบ่ง log เป็น time bucket เช่น 1 นาที:

```text
minute,total_requests,status_2xx,status_3xx,status_4xx,status_5xx,unique_ips,top_ip,top_endpoint
```

## Baseline คืออะไร

Baseline = พฤติกรรมปกติก่อน incident เช่น median requests/minute และ median errors/minute

ตัวอย่าง:

```text
normal median requests/minute = 300
normal median 5xx/minute = 2
incident minute requests = 4,800
incident minute 5xx = 900
```

แปลว่า incident spike ชัด

## นิยามสถานะระบบ

| State | เงื่อนไขตัวอย่าง | ความหมาย |
|---|---|---|
| `normal` | request/error ใกล้ baseline | ระบบปกติ |
| `suspicious` | 4xx หรือ suspicious request เริ่มเพิ่ม | เริ่มมี probe/scan |
| `unstable` | traffic spike หรือ 5xx เพิ่ม | ระบบเริ่มหน่วง/ไม่เสถียร |
| `down_or_crashing` | 5xx spike สูงมาก หรือ endpoint หลัก fail เยอะ | ระบบล่ม/พังบางส่วน |

## ถ้าไม่มี response time ให้พูดแบบไหน

ห้ามพูดว่า:

```text
response time สูงแน่นอน
```

ให้พูดว่า:

```text
เรา infer unstable period จาก traffic spike และ server error spike เพราะ log ไม่มี response time field
```

## Example Timeline Interpretation

```text
09:00-09:05 normal traffic
09:06 suspicious 404 scanning starts from IP group A
09:08 request volume jumps 10x
09:09 500 errors spike on /checkout and /search
09:10-09:12 system likely unstable/down due to sustained 5xx
09:13 traffic decreases and errors recover
```

## HOW จาก Timeline

ดู top endpoint ช่วง incident:

| ถ้า top endpoint เป็น | อาจแปลว่า |
|---|---|
| `/.env`, `/config.php`, `/backup.zip` | directory/config scanning |
| `/login` POST เยอะ | brute force |
| `/search?q=...UNION...` | SQL injection probing |
| `/download?file=../...` | path traversal |
| endpoint เดิม + 500 spike | crash trigger candidate |

## Output ที่ควรสร้าง

1. `incident_windows.csv`
2. `traffic_timeline.csv`
3. `status_timeline.csv`
4. `incident_summary.md`

## ประโยคสอนทีม

> WHEN ไม่ได้หาโดยเดาเวลา แต่หาโดยทำ time bucket แล้วดูว่า traffic/error เริ่มเบี่ยงจาก baseline ตอนไหน
