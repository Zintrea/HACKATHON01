# Data Pipeline — จาก Raw Log ไป Dashboard

## Pipeline Overview

```text
cart_web.log
  ↓
parse line by line
  ↓
request feature extraction
  ↓
IP aggregation + timeline aggregation
  ↓
scoring + classification
  ↓
incident window detection
  ↓
hidden bonus hunting
  ↓
CSV/JSON/Markdown outputs
  ↓
Dashboard + Presentation
```

## Stage 1: Parsing

Input line:

```text
timestamp | ip | method | endpoint | status | size
```

Output object:

```text
{
  timestamp,
  minute,
  ip,
  method,
  endpoint,
  status,
  size
}
```

## Stage 2: Feature Extraction

Add flags:

```text
is_path_traversal
is_sqli
is_xss
is_sensitive_endpoint
is_4xx
is_5xx
request_score
reasons
```

## Stage 3: Aggregation

### By IP

- total requests
- status counts
- payload counts
- sensitive hits
- requests per minute
- evidence examples

### By Minute

- total requests
- status counts
- unique IPs
- suspicious request count
- top IPs

## Stage 4: Scoring

Combine:

```text
ip_score = request_signal_score + rate_score + incident_overlap_score + hidden_bonus_score
```

## Stage 5: Incident Detection

Detect minutes where:

- request count > baseline threshold
- 5xx count > baseline threshold
- suspicious requests spike

Merge adjacent abnormal minutes into windows

## Stage 6: Dashboard Export

Create compact outputs:

- aggregated timeline
- top N attackers
- top N evidence lines
- hidden bonus candidates

## Key Rule

Raw log ใหญ่ แต่ dashboard data ต้องเล็กและ meaningful
