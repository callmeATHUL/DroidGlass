# User & CLI Guide: `bq-desktop-ai`

## 1. CLI Commands

### Generate SQL from Natural Language
```bash
bq-ai sql "Calculate daily active users for the last 30 days and forecast next week"
```

### Dry-run and Validate Query from Clipboard
Copy any BigQuery SQL query to your clipboard, then run:
```bash
bq-ai clip
# or press SUPER + ALT + B in Hyprland
```

### Explain & Optimize SQL
```bash
bq-ai explain "SELECT * FROM `my_project.analytics.events` WHERE user_id IS NOT NULL"
```

### Time-Series Forecasting (`AI.FORECAST`)
```bash
bq-ai forecast \
  --table "my_project.sales.daily_revenue" \
  --time-col "date" \
  --data-col "revenue" \
  --horizon 14
```

### Anomaly Detection (`AI.DETECT_ANOMALIES`)
```bash
bq-ai anomaly \
  --table "my_project.infra.cpu_usage" \
  --time-col "timestamp" \
  --data-col "usage_pct" \
  --contamination 0.02
```

### Text Classification (`AI.CLASSIFY`)
```bash
bq-ai classify \
  --table "my_project.support.tickets" \
  --text-col "message" \
  --categories "Billing" "Technical" "Account" "Feature Request"
```

### Vector Search (`VECTOR_SEARCH`)
```bash
bq-ai search \
  --table "my_project.docs.embeddings" \
  --query "How to configure VPC Service Controls"
```

---

## 2. Desktop & Omarchy Integration

1. **Hyprland Shortcuts**:
   - `SUPER + ALT + B`: Instantly inspects and validates the SQL code currently selected/copied in your clipboard.
   - `SUPER + ALT + S`: Launches a floating terminal with `bq-ai`.

2. **Quickshell Bar Widget**:
   - Click the database icon in the Omarchy bar to trigger clipboard evaluation and display desktop notification feedback.
