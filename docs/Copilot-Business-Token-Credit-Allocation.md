# Copilot Business — Token/Credit Allocation Guide

> **Last Updated:** September 2026
> **Applies to:** GitHub Copilot Business ($19/user/month)
> **Billing Model:** Usage-based AI Credits (effective June 1, 2026)

---

## 1. What Each User Gets

### Monthly AI Credit Allowance

| Plan | Price | Credits/User/Month | Credit Value | Credits Pooled? |
|---|---|---|---|---|
| **Copilot Business** | $19/user/month | 1,900 | $19.00 | ✅ Yes — org-wide pool |
| **Copilot Enterprise** | $39/user/month | 3,900 | $39.00 | ✅ Yes — org-wide pool |

**1 AI Credit = $0.01 USD**

### Pooled Credits — How It Works

Credits are **shared across your entire organization**, not isolated per user. A team of 5 developers shares the combined monthly allowance:

```
5 users × 1,900 credits = 9,500 pooled credits/month ($95 value)

This means:
  Light user consuming 500 credits → leaves 1,400 for others
  Heavy user consuming 3,500 credits → draws from the shared pool
  As long as the TOTAL doesn't exceed 9,500, no overage
```

---

## 2. What's Free (Unlimited) vs. What Uses Credits

| Feature | Uses Credits? | Details |
|---|---|---|
| ✅ **Code completions** (inline autocomplete) | **NO — Unlimited** | Free on all paid plans, no limits |
| ✅ **Next Edit Suggestions** | **NO — Unlimited** | Free on all paid plans |
| ⚠️ **Copilot Chat** | **YES** | Each chat message consumes tokens |
| ⚠️ **Agent Mode** (multi-step coding) | **YES — Heavy** | Can be 10-1,000× more tokens than chat |
| ⚠️ **Copilot Code Review** (PR reviews) | **YES** | Each review consumes tokens |
| ⚠️ **Copilot Cloud Agent** | **YES — Heavy** | Autonomous sessions are expensive |
| ⚠️ **Copilot CLI** | **YES** | Command-line interactions |

> **Key Insight:** The feature developers use **most** (code completions) is **free and unlimited**. Credits only apply to Chat, Agent Mode, Code Review, and CLI.

---

## 3. How Many Credits Each Activity Uses

### Credit Consumption Per Activity

| Activity | Typical Token Usage | Approx Credit Cost | Example |
|---|---|---|---|
| Simple chat question | ~1K-3K tokens | ~1-5 credits ($0.01-0.05) | "How do I use std::variant?" |
| Code explanation (1 file) | ~5K-15K tokens | ~5-30 credits ($0.05-0.30) | "Explain this function" |
| PR code review | ~10K-50K tokens | ~10-100 credits ($0.10-1.00) | Depends on PR size |
| Agent mode (simple) | ~50K-200K tokens | ~50-300 credits ($0.50-3.00) | Fix a bug, write a test |
| Agent mode (complex) | ~500K-2M+ tokens | ~100-1,000+ credits ($1.00-10.00+) | Multi-file refactoring |
| Cloud agent (autonomous) | ~1M-5M+ tokens | ~500-5,000+ credits ($5.00-50.00+) | Repository-wide tasks |

### Credit Cost Varies by Model

| Model Category | Example Models | Input ($/1M tokens) | Output ($/1M tokens) | Credit Impact |
|---|---|---|---|---|
| **Lightweight** | GPT-5 mini, Claude Haiku | ~$0.25 | ~$2.00 | 💚 Cheapest |
| **Versatile** | GPT-4o/5.4, Claude Sonnet | ~$2.50 | ~$15.00 | 🟡 Moderate |
| **Powerful** | GPT-5.3 Codex | ~$1.75 | ~$14.00 | 🟠 Moderate-High |
| **Ultra-Premium** | Claude Opus, o3 | Higher | Higher | 🔴 Most Expensive |

> **Tip:** Use lightweight models for simple questions and save premium models for complex tasks. This can stretch your credit pool 5-10×.

---

## 4. What Happens When Credits Run Out

### Default Behavior (No Overage Configured)

```
Credits exhausted mid-month:
  ✅ Code completions — STILL WORK (unlimited, always)
  ✅ Next Edit Suggestions — STILL WORK (unlimited, always)
  ❌ Copilot Chat — BLOCKED until next billing cycle
  ❌ Agent Mode — BLOCKED
  ❌ PR Code Review — BLOCKED
  ❌ Cloud Agent — BLOCKED
  ❌ Copilot CLI — BLOCKED
```

### With Overage Enabled

```
Credits exhausted mid-month:
  ✅ Code completions — STILL WORK
  ✅ Chat, Agent, Review — CONTINUE WORKING
  💰 Additional usage billed at $0.01 per credit (same rate)
  🛑 Stops only when your budget cap is reached
```

---

## 5. How to Enable Overage (Additional Tokens)

### Step 1: Enable Paid Overage

```
Go to: Org Settings → Copilot → AI Controls

Find: "AI credits paid usage" policy
  → ENABLE to allow usage beyond included credits
  → Overage billed to your org's payment method at $0.01/credit
```

### Step 2: Set a Spending Cap (CRITICAL)

```
Go to: Org Settings → Billing → Budgets

Create a budget:
  Name: "Copilot Monthly Cap"
  Amount: $50/month (or your preferred limit)
  
  ⚠️ ENABLE "Stop usage when budget limit is reached"
  
  WITHOUT this toggle → budget only SENDS A NOTIFICATION
  and charges KEEP ACCUMULATING! This is the #1 mistake.
```

### Step 3: Set Per-User Limits (Recommended)

```
Go to: Org Settings → Copilot → AI Controls

Set Universal User-Level Budget (ULB):
  Default: 3,000 credits/user/month
  
  This prevents ONE heavy user from draining the entire pool.
  ULBs are ALWAYS hard stops — usage is blocked when hit.
  
  Override for power users:
    Set individual overrides (e.g., 5,000 credits for tech leads)
```

### Summary of Controls

| Control | What It Does | Hard Stop? | How to Set |
|---|---|---|---|
| **AI Credits Paid Usage Policy** | Master on/off for overage | Yes (if disabled) | AI Controls |
| **Org Budget** | Cap total org overage | Only if "Stop usage" enabled | Billing → Budgets |
| **User-Level Budget (ULB)** | Cap per-user consumption | **Always** | AI Controls |

---

## 6. Cost Scenarios

### 5 Users — Copilot Business

| Scenario | Seats | Included Credits | Overage | Monthly Total | Annual |
|---|---|---|---|---|---|
| **Light usage** (mostly completions) | $95 | 9,500 | $0 | **$95** | **$1,140** |
| **Moderate** (daily chat + weekly agent) | $95 | 9,500 | ~$15 | **~$110** | **~$1,320** |
| **Heavy** (daily agent mode) | $95 | 9,500 | ~$50 | **~$145** | **~$1,740** |
| **With $50 cap** (heavy, capped) | $95 | 9,500 | max $50 | **max $145** | **max $1,740** |

### 50 Users — Copilot Business

| Scenario | Seats | Included Credits | Overage | Monthly Total | Annual |
|---|---|---|---|---|---|
| **Light usage** | $950 | 95,000 | $0 | **$950** | **$11,400** |
| **Moderate** | $950 | 95,000 | ~$300 | **~$1,250** | **~$15,000** |
| **Heavy** | $950 | 95,000 | ~$800 | **~$1,750** | **~$21,000** |
| **Hard cap ($0 overage)** | $950 | 95,000 | $0 | **$950** | **$11,400** |

### Typical User Distribution (50 Developers)

| Usage Profile | % of Devs | Users | Credits/User/Mo | Total Credits |
|---|---|---|---|---|
| **Light** (completions + occasional chat) | 40% | 20 | ~500 | 10,000 |
| **Moderate** (daily chat + weekly agent) | 40% | 20 | ~2,500 | 50,000 |
| **Heavy** (daily agent + PR reviews) | 15% | 7-8 | ~5,000 | 37,500 |
| **Power** (continuous agentic workflows) | 5% | 2-3 | ~10,000+ | 25,000+ |
| | | **Total** | | **~122,500** |

With 95,000 credits included → ~27,500 overage → ~$275/month overage.

---

## 7. Recommended Configuration

### For a 5-User Pilot

```
1. Enable Copilot Business ($95/month)
2. Enable paid overage (AI Controls → Enable)
3. Set org budget: $50/month cap with "Stop usage" ON
4. Set per-user ULB: 3,000 credits/user
5. Tell developers:
   → Completions are unlimited — use freely
   → Use lightweight models for simple questions
   → Save Agent Mode for complex tasks
   
Expected monthly cost: $95-145
```

### For 50-User Full Rollout

```
Month 1-2: HARD CAP ($0 overage)
  → Measure actual usage patterns
  → Identify heavy vs. light users
  → Fixed cost: $950/month ($11,400/year)

Month 3+: SET OVERAGE BUDGET
  → Based on data, set $300-500/month overage cap
  → Set ULBs to prevent pool drain
  → Expected: $1,250-1,750/month ($15,000-21,000/year)

Ongoing: OPTIMIZE
  → Encourage lightweight models for routine tasks
  → Reserve premium models for complex C++ reasoning
  → Use "auto model selection" for potential 10% discount
```

---

## 8. Quick Reference — Admin Checklist

```
□ Org Settings → Copilot → Enable Copilot Business
□ Assign seats (all members or specific users)
□ Billing → Add payment method
□ AI Controls → Enable/disable paid overage
□ Billing → Budgets → Set monthly cap + enable "Stop usage"
□ AI Controls → Set Universal User-Level Budget (ULB)
□ Monitor: Billing → AI Usage dashboard (check weekly)
```

---

## 9. GitHub Copilot vs. Enterprise — Do You Need Both?

```
Copilot Business ($19/user):
  → Works with GitHub Free, Team, OR Enterprise orgs
  → Does NOT require GitHub Enterprise ($21/user)
  → Same completions, chat, agent, PR review
  
Copilot Enterprise ($39/user):
  → REQUIRES GitHub Enterprise Cloud ($21/user)
  → Adds: server-side codebase indexing, knowledge bases
  → Total: $21 + $39 = $60/user/month

Recommendation:
  Start with: GitHub Free Org + Copilot Business = $19/user
  Upgrade when: You need SSO, audit logs, or codebase indexing
```

---

> *This document is part of the Copilot documentation suite. See also:*
> - *[Copilot C++ Review, Models & Cost Guide](Copilot-CPP-Review-Models-Cost-Guide.md)*
> - *[Copilot How It Works — Dev Team FAQ](Copilot-How-It-Works-Dev-Team-FAQ.md)*
> - *[AI Coding Agents — C++ CAE Comparison](AI-Coding-Agents-CPP-CAE-Comparison.md)*
> - *[Copilot Security Assessment](Copilot-Security-Assessment.md)*
