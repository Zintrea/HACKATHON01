# H1 Dorm Code — Story-driven Log Analyzer

> โค้ดชุดนี้ใช้วิเคราะห์ `cart_web.log` แบบ reproducible เพื่อช่วยตอบโจทย์ H1: **WHO**, **WHEN & HOW**, **TELL PEOPLE**, และ **HIDDEN BONUS**

## ใช้ภาษาอะไร

ใช้ **Python 3 / standard library only** เพื่อให้รันใน Linux/WSL/contest environment ได้ง่าย ไม่ต้องติดตั้ง dependency เพิ่ม

## โครงสร้าง

```text
code/
├── README.md
├── run_analysis.py              # CLI entrypoint
├── h1_analyzer/
│   ├── models.py                # dataclass: LogRequest, RequestScore, IpStats
│   ├── parser.py                # raw line -> structured request
│   ├── patterns.py              # red flag detection
│   ├── scoring.py               # explainable suspicion scoring
│   ├── aggregators.py           # aggregate by IP/time/endpoint
│   ├── timeline.py              # incident window builder
│   ├── hidden_bonus.py          # hidden clue hunter
│   ├── reports.py               # CSV/JSON/Markdown writers
│   └── runner.py                # full pipeline connector
├── tests/                       # unittest tests for each core layer
├── docs/
│   ├── code-walkthrough.md
│   ├── debug-guide.md
│   ├── evidence-playbook.md
│   ├── output-data-dictionary.md
│   ├── presentation-cheatsheet.md
│   ├── presentation-code-story.md
│   └── scoring-rules.md
├── sanity_check.py              # validate output schemas and key invariants
└── output/                      # generated when running full analysis
```

## Code Story สำหรับสอนคนอื่น

```text
Raw log
→ Parser
→ Red Flag Detector
→ Scoring
→ IP Aggregation
→ Timeline / Incident Windows
→ Hidden Bonus Hunting
→ CSV/JSON/Markdown Reports
→ Dashboard-ready data
```

## Important docs for teaching/presentation

| File | ใช้ทำอะไร |
|---|---|
| `docs/output-data-dictionary.md` | อธิบายทุก output file และทุก column ว่ามาจากไหน/แปลว่าอะไร |
| `docs/scoring-rules.md` | อธิบาย scoring, thresholds, และวิธี defend คะแนน |
| `docs/evidence-playbook.md` | วิธีไล่หลักฐานจาก output เพื่อพิสูจน์ WHO/WHEN/HOW |
| `docs/presentation-cheatsheet.md` | ชีทสั้นสำหรับพรีเซนต์และตอบกรรมการ |
| `docs/code-walkthrough.md` | อธิบาย code แต่ละ module |
| `docs/debug-guide.md` | วิธี debug และตรวจ output |

## Run tests

```bash
cd /mnt/c/Users/boony/Desktop/H01/H1/Dorm/code
python3 -m unittest discover -s tests -v
```

## Debug run แบบเร็ว

ใช้ตอนอยากเช็ก logic ก่อนรันไฟล์ใหญ่:

```bash
python3 run_analysis.py ../../cart_web.log --output output_debug --max-lines 100000
```

## Run full log

```bash
python3 run_analysis.py ../../cart_web.log --output output
```

## Sanity check outputs

ใช้หลังรัน analyzer เพื่อเช็กว่า output shape ถูกต้องและไม่เกิดปัญหาแบบ endpoint summary หลอกตา:

```bash
python3 sanity_check.py output
```

ผลที่ดีควรมี:

```text
status=PASS
```

## Output format

หลังรัน จะได้ไฟล์เหล่านี้:

| File | ใช้ตอบ | อ่านยังไง |
|---|---|---|
| `attacker_ips.csv` | WHO ARE THEY | suspicious IP ranking, label, score, reasons |
| `traffic_timeline.csv` | WHEN | full traffic/error/suspicious requests ราย minute |
| `incident_windows.csv` | WHEN | ช่วงเวลาผิดปกติที่ merge แล้ว |
| `endpoint_summary.csv` | HOW | endpoint ไหนถูกยิง/มี payload/error |
| `suspicious_requests.csv` | HOW evidence | request ตัวอย่างที่มี red flags |
| `hidden_bonus_candidates.csv` | HIDDEN BONUS | clue candidates + confidence |
| `dashboard_data.json` | TELL PEOPLE | compact dashboard data: top attackers + sampled timeline + evidence |
| `h1_summary.md` | Presentation | summary อ่านเร็วสำหรับเล่าเรื่อง |

## ข้อจำกัดที่ต้องพูดตอนนำเสนอ

- log นี้มี response latency อยู่ field สุดท้าย (`latency_ms`) ดังนั้นช่วงหน่วงสามารถอ้างอิง latency ที่วัดได้จริงร่วมกับ traffic/error spikes
- log นี้ไม่มี User-Agent และ request body จึงวิเคราะห์จาก endpoint/status/rate เป็นหลัก
- score เป็น explainable heuristic สำหรับจัดลำดับ evidence ไม่ใช่คำตัดสิน 100% จาก signal เดียว
