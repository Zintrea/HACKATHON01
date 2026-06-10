# Presentation Code Story — เล่า code ให้กรรมการเข้าใจ

> เราไม่ได้อ่าน log manual แต่สร้าง pipeline ที่อ่านทุกบรรทัดแล้วสรุปเป็น evidence

1. Parser: แปลง raw text เป็น structured request
2. Pattern detector: หา red flags ต่อ request
3. Scoring: รวม red flags เป็นคะแนน explainable
4. Aggregator: รวมพฤติกรรมต่อ IP เพื่อตอบ WHO
5. Timeline: รวมต่อ minute เพื่อตอบ WHEN
6. Hidden bonus hunter: หา clue/signature ที่ซ่อนอยู่
7. Reports: export CSV/JSON/Markdown ให้ dashboard ใช้ต่อ

ประโยคสำคัญ:

```text
The score is not a guess. It is a reproducible explanation of why each IP is suspicious.
```
