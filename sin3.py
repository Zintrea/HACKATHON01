from datetime import datetime

suspect_ips = {
    # ใส่ 19 IP ที่ได้มา
}

last_record = {}

with open("cart_web.log", encoding="utf-8") as f:
    for line in f:
        p = [x.strip() for x in line.split("|")]

        if len(p) != 6:
            continue

        dt = datetime.strptime(p[0], "%Y-%m-%d %H:%M:%S")
        ip = p[1]
        endpoint = p[3]

        if ip not in suspect_ips:
            continue

        if ip not in last_record or dt > last_record[ip][0]:
            last_record[ip] = (dt, endpoint)

message = ""

for ip in sorted(last_record):
    endpoint = last_record[ip][1]
    message += endpoint[-1]

print(message)