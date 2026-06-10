# Debug Guide — วิธี debug ทีละส่วน

## Run tests

```bash
cd /mnt/c/Users/boony/Desktop/H01/H1/Dorm/code
python3 -m unittest discover -s tests -v
```

## Debug with first N lines

```bash
python3 run_analysis.py ../../cart_web.log --output output_debug --max-lines 100000
```

## Run full log

```bash
python3 run_analysis.py ../../cart_web.log --output output
```

## Check outputs quickly

```bash
head -5 output/attacker_ips.csv
head -5 output/incident_windows.csv
head -20 output/h1_summary.md
```

## If results look weird

1. Check `malformed_lines`
2. Check `status_counts` in `h1_summary.md`
3. Open `suspicious_requests.csv` to inspect evidence
4. Tune patterns/thresholds only after seeing evidence
