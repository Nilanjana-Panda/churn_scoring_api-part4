# D2C Customer Churn Capstone — Data Dictionary

**Snapshot date:** `2025-09-30`
**Target window:** 60 days after the snapshot date (i.e., `2025-10-01` to `2025-11-29`)
**Primary key across all files:** `customer_id`

---

## ⚠️ Leakage Rule (Critical)

Use **only** data available on or before `2025-09-30` as model features.
`orders.csv` contains rows dated after the snapshot; those rows exist **only** to explain how churn labels were created. Do **not** include them as features.

---

## File Overview

| File | Rows | Description |
|---|---|---|
| `customers.csv` | 2,400 | Static customer profile and acquisition attributes |
| `orders.csv` | ~10,009 | Full order-level transaction history (pre- and post-snapshot) |
| `support_tickets.csv` | ~1,921 | Customer-service interactions |
| `web_events_snapshot.csv` | 2,400 | 30-day web/app activity as of snapshot date |
| `churn_labels.csv` | 2,400 | Target variable and train/val/test split assignment |
| `rfm_modeling_snapshot.csv` | 2,400 | Pre-built, feature-engineered modeling table |
| `intervention_history.csv` | 2,400 | Most recent campaign/intervention per customer |

---

## 1. `customers.csv` (2,400 rows)

**Description:** One row per customer. All columns reflect the state at or before the snapshot date.

| Column | Type | Nullable | Description | Sample Values |
|---|---|---|---|---|
| `customer_id` | string | No | Unique customer identifier | `CUST00001` – `CUST02400` |
| `signup_date` | date | No | Date customer created account | `2024-01-01` – `2025-09-15` |
| `city_tier` | categorical | No | City market size classification | `Tier 1`, `Tier 2`, `Tier 3` |
| `age_group` | categorical | No | Age bracket | `18-24`, `25-34`, `35-44`, `45+` |
| `acquisition_channel` | categorical | No | Marketing channel | `Google Search`, `Instagram`, `Influencer`, `Referral`, `Marketplace`, `Organic` |
| `loyalty_tier` | categorical | **Yes** (~1,386 nulls) | Loyalty program tier | `Silver`, `Gold`, `Platinum` |
| `preferred_category` | categorical | No | Product category preference | `Skin Care`, `Hair Care`, `Makeup`, `Fragrance`, `Wellness`, `Baby Care` |
| `skin_type` | categorical | **Yes** (~401 nulls) | Self-reported skin type | `Normal`, `Dry`, `Oily`, `Combination`, `Sensitive`, `NA` |
| `marketing_consent` | categorical | No | Marketing opt-in status | `Yes`, `No` |

**Data Quality Notes:**
- ~1,386 nulls in `loyalty_tier` (58%): Customers not enrolled in loyalty program
- ~401 nulls in `skin_type` (17%): Customer-provided data, not mandatory at signup

---

## 2. `orders.csv` (~10,009 rows)

**Description:** One row per order. Contains both pre-snapshot orders (use as features) and post-snapshot orders (for label construction only — DO NOT use as features).

| Column | Type | Nullable | Description | Sample Values |
|---|---|---|---|---|
| `order_id` | string | No | Unique order identifier | `ORD000001` – `ORD009997` (some with `_DUP` suffix) |
| `customer_id` | string | No | Links to `customers.csv` | `CUST00001` – `CUST02400` |
| `order_date` | date | No | Date order was placed | `2024-01-09` – `2025-11-29` |
| `category` | categorical | No | Product category ordered | `Skin Care`, `Hair Care`, `Makeup`, `Fragrance`, `Wellness`, `Baby Care` |
| `quantity` | integer | No | Units ordered | 1 – 4 |
| `gross_amount` | float | No | Order value before discount (INR) | 149.0 – 24,789.38 |
| `discount_pct` | float | No | Discount fraction | 0.0 – 0.7 (0.20 = 20% off) |
| `delivery_days` | integer | No | Days from order to delivery | 1 – 11 |
| `returned` | binary | No | Order returned? | `0` (no), `1` (yes) |
| `rating` | integer | **Yes** (~80 nulls) | Customer satisfaction rating | 1 – 5 |

**Data Quality Notes:**
- **Post-snapshot orders:** `order_date > 2025-09-30` must NOT be used as model features
- ~80 nulls in `rating` (0.8%): Customers who didn't leave ratings
- **Duplicate-like records:** Some `order_id` values end with `_DUP` (intentional data quality issue to handle)
- **Outliers:** `gross_amount` has intentional high-value outliers (e.g., ₹24,789) for data quality exploration

**Feature Engineering Window:**
- Use only orders with `order_date <= 2025-09-30` for model features
- Compute RFM and behavioral metrics from orders in lookback windows (180-day, 90-day, 30-day)

---

## 3. `support_tickets.csv` (~1,921 rows)

**Description:** One row per support ticket. A customer can have multiple tickets.

| Column | Type | Nullable | Description | Sample Values |
|---|---|---|---|---|
| `ticket_id` | string | No | Unique ticket identifier | `TKT000001` – `TKT001921` |
| `customer_id` | string | No | Links to `customers.csv` | `CUST00001` – `CUST02398` |
| `ticket_date` | date | No | Date ticket was raised | `2024-01-13` – `2025-09-30` |
| `issue_type` | categorical | No | Nature of complaint | `damaged_item`, `late_delivery`, `refund_delay`, `wrong_item`, `product_reaction`, `payment_issue`, `general_query` |
| `support_channel` | categorical | No | Submission channel | `chat`, `call`, `email` |
| `resolution_hours` | float | No | Time to resolution (hours) | 1.0 – 74.6 |
| `sentiment_score` | float | No | Ticket sentiment (NLP-derived) | -1.0 (very negative) to +1.0 (very positive) |
| `reopened` | binary | No | Ticket reopened after closure? | `0` (no), `1` (yes) |

**Data Quality Notes:**
- **Sparse coverage:** Only ~1,921 tickets for 2,400 customers (~80% have no tickets)
- **Sentiment score interpretation:** Negative scores indicate dissatisfied customers (churn risk signal)
- **Reopened tickets:** Flag customers with service dissatisfaction

**Feature Engineering:**
- Aggregate by customer for 90-day window before snapshot (e.g., ticket count, negative ticket rate, avg resolution time)

---

## 4. `web_events_snapshot.csv` (2,400 rows)

**Description:** One row per customer. All metrics are for the **30-day window ending on snapshot date** (`2025-09-01` to `2025-09-30`).

| Column | Type | Nullable | Description | Sample Values |
|---|---|---|---|---|
| `customer_id` | string | No | Links to `customers.csv` | `CUST00001` – `CUST02400` |
| `snapshot_date` | date | No | Always this date | `2025-09-30` |
| `sessions_30d` | integer | No | Web/app sessions in last 30 days | ≥ 0 (range: 0–19) |
| `product_views_30d` | integer | No | Product detail page views | ≥ 0 (range: 0–88) |
| `cart_adds_30d` | integer | No | Items added to cart | ≥ 0 (range: 0–7) |
| `wishlist_adds_30d` | integer | No | Items added to wishlist | ≥ 0 (range: 0–5) |
| `abandoned_carts_30d` | integer | No | Incomplete checkout sessions | ≥ 0 (range: 0–4) |
| `email_opens_30d` | integer | No | Marketing emails opened | ≥ 0 (range: 0–10) |
| `campaign_clicks_30d` | integer | No | Clicks on campaign links | ≥ 0 (range: 0–4) |
| `last_visit_days_ago` | integer | No | Days since last visit from snapshot date | ≥ 0 (range: 0–60) |

**Data Quality Notes:**
- **Zero engagement:** Many customers have zero sessions, product views (high dormancy signal)
- **High `last_visit_days_ago`:** Indicates inactive customers (potential churn risk)

**Feature Engineering:**
- Use as-is (already aggregated at customer level)
- High engagement (sessions, product views, cart adds) → lower churn risk
- High `last_visit_days_ago` → higher churn risk

---

## 5. `churn_labels.csv` (2,400 rows)

**Description:** Target variable and train/validation/test split. **Authoritative source for labels.**

| Column | Type | Nullable | Description | Sample Values |
|---|---|---|---|---|
| `customer_id` | string | No | Links to `customers.csv` | `CUST00001` – `CUST02400` |
| `snapshot_date` | date | No | Always this date | `2025-09-30` |
| `churn_next_60d` | binary | No | **TARGET VARIABLE** | `0` (no churn), `1` (churn) |
| `split` | categorical | No | Data split assignment | `train`, `validation`, `test` |

**Target Definition:**
- **`churn_next_60d = 1`:** Customer made NO purchase in 60-day window (`2025-10-01` to `2025-11-29`)
- **`churn_next_60d = 0`:** Customer made AT LEAST ONE purchase in same window

**Split Distribution:**
- `train`: ~60% of customers (for model training)
- `validation`: ~20% of customers (for hyperparameter tuning)
- `test`: ~20% of customers (for final evaluation)

**Data Quality Notes:**
- **Class imbalance:** Check proportion of churners vs. non-churners
- **Use provided split:** Do NOT create your own train/test split; use the `split` column

---

## 6. `rfm_modeling_snapshot.csv` (2,400 rows)

**Description:** Pre-built feature table combining all data sources as of snapshot date. **Safe to use directly as model input (no leakage).**

**Columns from other tables:**
- `customer_id`, `snapshot_date`
- `city_tier`, `age_group`, `acquisition_channel`, `loyalty_tier`, `preferred_category`, `marketing_consent` (from `customers`)
- `sessions_30d`, `product_views_30d`, `cart_adds_30d`, `wishlist_adds_30d`, `abandoned_carts_30d`, `email_opens_30d`, `campaign_clicks_30d`, `last_visit_days_ago` (from `web_events_snapshot`)

**Pre-computed RFM and behavioral features:**

| Column | Type | Description | Notes |
|---|---|---|---|
| `recency_days` | integer | Days since last pre-snapshot order | Lower = more recent |
| `frequency_180d` | integer | Orders in 180 days before snapshot | Purchase frequency |
| `monetary_180d` | float | Total gross spend in 180 days (INR) | Customer lifetime value signal |
| `return_rate_180d` | float | Proportion of returned orders (180-day) | 0.0–1.0 |
| `avg_discount_pct_180d` | float | Average discount on orders (180-day) | 0.0–1.0 |
| `avg_rating_180d` | float | Average order rating (180-day) | 1.0–5.0 (null if no ratings) |
| `category_diversity_180d` | integer | Number of distinct categories purchased (180-day) | ≥ 1 |
| `ticket_count_90d` | integer | Support tickets in 90 days before snapshot | Service complaints |
| `negative_ticket_rate_90d` | float | Proportion of negative-sentiment tickets (90-day) | 0.0–1.0 |
| `avg_resolution_hours_90d` | float | Average ticket resolution time (90-day) | 0 if no tickets |
| `days_since_signup` | integer | Days from signup to snapshot | Customer tenure |
| `churn_next_60d` | binary | **TARGET (do not use as feature)** | — |
| `split` | categorical | Train/val/test assignment | — |

**Best Use:** Start with this table for Parts 3 & 4 if you want to skip raw data engineering.

---

## 7. `intervention_history.csv` (2,400 rows)

**Description:** Most recent retention campaign sent to each customer before snapshot.

| Column | Type | Nullable | Description | Sample Values |
|---|---|---|---|---|
| `customer_id` | string | No | Links to `customers.csv` | `CUST00001` – `CUST02400` |
| `snapshot_date` | date | No | Always this date | `2025-09-30` |
| `last_campaign_received` | categorical | No | Most recent campaign type | `welcome_offer`, `free_shipping`, `bundle_discount`, `new_launch`, `none` |
| `last_campaign_cost` | integer | No | Campaign cost (INR) | 0 (if `none`), else 1–40 |
| `manual_priority_bucket` | categorical | No | CRM team's priority label | `high`, `medium`, `low` |

**Data Quality Notes:**
- **Baseline signal:** `manual_priority_bucket` is useful for Part 2 (validation of segment quality)
- **Campaign cost:** Varies by campaign type; may correlate with customer value

---

## Known Data Quality Issues (Intentional for Part 1)

| Issue | File(s) | Column(s) | Handling Strategy |
|---|---|---|---|
| **Duplicate-like records** | `orders.csv` | `order_id` | Some IDs end with `_DUP`. Deduplicate or aggregate as needed. |
| **Missing values** | `customers.csv` | `loyalty_tier`, `skin_type` | Handle via imputation or indicator flags. |
| **Missing ratings** | `orders.csv` | `rating` | Exclude from rating aggregates or mark separately. |
| **Outlier order values** | `orders.csv` | `gross_amount` | Investigate; decide if remove, cap, or transform. |
| **Post-snapshot orders** | `orders.csv` | `order_date` | **CRITICAL:** Filter out for model features. |
| **Sparse support data** | `support_tickets.csv` | All | ~80% of customers have zero tickets. |
| **High dormancy** | `web_events_snapshot.csv` | `sessions_30d`, `last_visit_days_ago` | Many zeros indicate inactive customers. |

---

## Join Guide

All tables join on `customer_id`. Recommended join order:

```
customers (left join)
  ├── orders
  ├── support_tickets
  ├── web_events_snapshot
  ├── churn_labels
  ├── rfm_modeling_snapshot
  └── intervention_history
```

**Note:** Not every customer has support tickets (expected). Use **left joins** to preserve all 2,400 customers.

---

## Feature Engineering Windows (for Part 1 EDA)

- **180-day window:** `2025-04-03` to `2025-09-30` (for RFM)
- **90-day window:** `2025-07-02` to `2025-09-30` (for support/service metrics)
- **30-day window:** `2025-09-01` to `2025-09-30` (for web activity, already aggregated in snapshot)
- **Entire history:** From signup to `2025-09-30` (for tenure, lifetime metrics)

---

## Churn Label Construction (Reference Only)

For context, churn labels were created by:
1. Taking each customer as of snapshot date (`2025-09-30`)
2. Checking if they had ANY order in window `2025-10-01` to `2025-11-29`
3. If NO order: `churn_next_60d = 1`
4. If ≥1 order: `churn_next_60d = 0`

**Do NOT use orders from `2025-10-01` onwards as model features.**

---

## Summary Stats (Quick Reference)

| Metric | Value |
|---|---|
| Total customers | 2,400 |
| Total orders | ~10,009 |
| Total support tickets | ~1,921 |
| Churners (approx.) | ~1,200 (50%) |
| Non-churners (approx.) | ~1,200 (50%) |
| Date range | `2024-01-01` – `2025-11-29` |
| Snapshot date | `2025-09-30` |
