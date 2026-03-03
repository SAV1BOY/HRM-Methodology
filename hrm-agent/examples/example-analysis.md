# Example Session: Data Analysis Task

> **User Task:** "Analyze 500 customer support tickets to identify the top complaint categories, sentiment trends, and actionable recommendations for the product team."

## Task Analysis

```yaml
task_type: data-extraction
complexity: complex
constraints:
  latency: relaxed
  token_budget: large
  quality: high
  tools_available: [code_interpreter]
output_format: structured report
data_volume: 500 records
```

## Technique Selection

| Rank | Technique | Score | Rationale |
|------|-----------|-------|-----------|
| 1 | Prompt Chaining | 0.95 | Multi-stage analysis pipeline needed |
| 2 | Few-Shot Prompting | 0.90 | Classification requires format examples |
| 3 | Chain-of-Thought | 0.88 | Reasoning about trends and patterns |
| 4 | Program of Thoughts | 0.85 | Statistical analysis via code |
| 5 | Self-Refine | 0.80 | Polish final recommendations |

**Playbook match:** `playbooks/data-extraction.md` — partial match, customized pipeline.

## Pipeline Design

```
Prompt Chaining: Classify → Aggregate → Analyze Trends → Generate Recommendations
```

```
┌─────────────────────────────┐
│  500 Support Tickets        │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│  1. Few-Shot Classification  │  Classify each ticket into
│     (batched, 50 per call)  │  category + sentiment + urgency
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│  2. Program of Thoughts     │  Aggregate results via code:
│     (code interpreter)      │  counts, percentages, trends
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│  3. Chain-of-Thought        │  Reason about patterns,
│     Analysis                │  correlations, root causes
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│  4. Self-Refine             │  Polish recommendations
│     Recommendations         │  for actionability
└─────────────┴───────────────┘
```

## Execution Trace

### Step 1: Few-Shot Classification (Batched)

**Prompt (repeated for each batch of 50 tickets):**
```
Classify each customer support ticket below into:
- category: one of [billing, bug, feature_request, performance, onboarding,
  documentation, security, integration, account, other]
- sentiment: one of [angry, frustrated, neutral, satisfied, confused]
- urgency: one of [critical, high, medium, low]
- key_issue: one phrase summarizing the core complaint

EXAMPLES:

Ticket: "I've been charged twice for my subscription this month. This is
the third time this has happened. I want a refund immediately."
→ category: billing
→ sentiment: angry
→ urgency: high
→ key_issue: duplicate subscription charge

Ticket: "The dashboard takes 30+ seconds to load since last week's update.
It was fine before."
→ category: performance
→ sentiment: frustrated
→ urgency: high
→ key_issue: dashboard load time regression

Ticket: "How do I connect my Slack workspace? I can't find the setting."
→ category: onboarding
→ sentiment: confused
→ urgency: low
→ key_issue: Slack integration discovery

NOW CLASSIFY THESE TICKETS:

{batch_of_50_tickets}

Output as JSON array:
[{"ticket_id": "...", "category": "...", "sentiment": "...", "urgency": "...",
  "key_issue": "..."}, ...]
```

**Output (sample from batch 1):**
```json
[
  {
    "ticket_id": "T-001",
    "category": "performance",
    "sentiment": "frustrated",
    "urgency": "high",
    "key_issue": "API response time degradation after v2.3 release"
  },
  {
    "ticket_id": "T-002",
    "category": "billing",
    "sentiment": "angry",
    "urgency": "critical",
    "key_issue": "charged after cancellation"
  },
  {
    "ticket_id": "T-003",
    "category": "feature_request",
    "sentiment": "neutral",
    "urgency": "low",
    "key_issue": "wants CSV export for reports"
  }
]
```

### Step 2: Program of Thoughts (Aggregation)

**Prompt:**
```
Using the classified ticket data below, write Python code to compute:
1. Category distribution (count and percentage)
2. Sentiment distribution per category
3. Urgency breakdown
4. Week-over-week trend (if timestamps available)
5. Top 10 most common key_issues

CLASSIFIED DATA:
{all_classified_tickets_json}

Write the code, execute it, and present the results as tables.
```

**Output:**
```python
import pandas as pd
from collections import Counter

df = pd.DataFrame(classified_tickets)

# 1. Category distribution
category_dist = df['category'].value_counts()
print("=== Category Distribution ===")
print(category_dist.to_frame().assign(
    pct=lambda x: (x['count'] / len(df) * 100).round(1)
))

# Results:
# category         count    pct
# performance       127    25.4%
# billing            98    19.6%
# bug                84    16.8%
# feature_request    63    12.6%
# onboarding         45     9.0%
# integration        32     6.4%
# documentation      22     4.4%
# security           15     3.0%
# account            10     2.0%
# other               4     0.8%

# 2. Sentiment by category (cross-tab)
sentiment_by_cat = pd.crosstab(df['category'], df['sentiment'], normalize='index')
print("\n=== Sentiment by Category ===")
print((sentiment_by_cat * 100).round(1))

# 3. Urgency breakdown
urgency_dist = df['urgency'].value_counts()
# critical: 47 (9.4%), high: 156 (31.2%), medium: 198 (39.6%), low: 99 (19.8%)

# 4. Top key issues
top_issues = Counter(df['key_issue']).most_common(10)
print("\n=== Top 10 Issues ===")
for issue, count in top_issues:
    print(f"  {count:3d}x  {issue}")
```

### Step 3: Chain-of-Thought Analysis

**Prompt:**
```
Analyze the following aggregated support ticket data step by step.
Identify patterns, correlations, and root causes.

AGGREGATED DATA:
{aggregation_output}

Think through the following questions:
1. What is the most concerning category and why?
2. Are there correlations between categories and sentiment?
3. What do the top issues suggest about systemic problems?
4. What trends would you expect if these issues are not addressed?

Reason step by step, citing specific numbers from the data.
```

**Output:**
```
Step 1: Most Concerning Category
Performance issues lead at 25.4% (127 tickets), but more critically,
billing issues (19.6%, 98 tickets) have the highest proportion of
"angry" sentiment (43%) and "critical" urgency (28%). This combination
suggests billing issues have the highest churn risk.

Step 2: Sentiment-Category Correlation
- Performance: 67% frustrated, 18% angry → indicates regression, not
  baseline expectations
- Billing: 43% angry, 31% frustrated → emotionally charged, time-sensitive
- Onboarding: 62% confused, 24% neutral → information gap, not anger
- Feature requests: 71% neutral → normal enhancement requests

Step 3: Systemic Problems from Top Issues
The top 3 issues account for 34% of all tickets:
1. "API response time degradation" (52 tickets) → likely a v2.3 regression
2. "Charged after cancellation" (38 tickets) → billing system bug
3. "Dashboard load time" (28 tickets) → related to #1, same root cause?

The API and dashboard issues may share a common cause (the v2.3 release),
which would mean 80 tickets (16%) stem from a single deployment.

Step 4: Projected Trends
Without intervention:
- Performance issues will drive feature-engaged users to competitors
- Billing issues will generate refund requests and negative reviews
- The onboarding confusion suggests documentation debt that compounds
  as the user base grows
```

### Step 4: Self-Refine (Recommendations)

**First draft → Refined recommendations:**
```
## Actionable Recommendations for Product Team

### P0 — Immediate (This Sprint)
1. **Investigate v2.3 performance regression**
   - 80+ tickets (16%) likely trace to the v2.3 release
   - Roll back or hotfix API response time and dashboard loading
   - Owner: Backend team
   - Metric: P95 API latency back to pre-v2.3 baseline

2. **Fix billing cancellation bug**
   - 38 tickets for "charged after cancellation" = revenue risk + legal
   - Audit all cancellations in the past 30 days
   - Issue proactive refunds before customers escalate
   - Owner: Billing team

### P1 — High Priority (Next Sprint)
3. **Overhaul onboarding integration discovery**
   - 45 tickets (9%) from confused new users
   - Add setup wizard with integration quick-links
   - Update docs with video walkthroughs
   - Owner: Product + DevRel

4. **Add CSV export for reports**
   - 63 feature requests (12.6%), most requested enhancement
   - Low engineering effort, high customer satisfaction impact
   - Owner: Frontend team

### P2 — Medium Priority (Next Quarter)
5. **Proactive billing communication**
   - Send email confirmation for every charge and cancellation
   - Add billing history page with downloadable invoices
   - Goal: Reduce billing tickets by 50%

### Metrics to Track
| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| Performance tickets/week | ~32 | <5 | 2 weeks |
| Billing complaint rate | 19.6% | <5% | 1 month |
| Onboarding confusion tickets | 9% | <3% | 2 months |
| Overall ticket volume | 500/month | <300/month | 3 months |
```

## Pipeline Cost Summary

| Step | API Calls | Tokens Used | Latency |
|------|-----------|------------|---------|
| Few-Shot Classification | 10 (batched) | ~15000 | ~40s |
| Program of Thoughts | 1 | ~2000 | ~8s |
| Chain-of-Thought | 1 | ~1500 | ~6s |
| Self-Refine | 2 | ~2000 | ~8s |
| **Total** | **14** | **~20500** | **~62s** |

## Technique Alternatives

| Scenario | Pipeline Modification |
|----------|----------------------|
| **Real-time dashboard** | Skip Self-Refine, stream classification results |
| **Higher accuracy** | Add Self-Consistency to classification (3 passes, majority vote) |
| **Multilingual tickets** | Add Role Prompting ("You are a multilingual support analyst") |
| **Smaller budget** | Use Chain-of-Draft instead of full CoT for analysis step |
| **Compliance audit** | Add Source-Grounded Generation to cite specific ticket IDs |
