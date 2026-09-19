# GitHub Enterprise & Copilot — Cost Estimation for CAE Software Development

> **Prepared for:** Management Review
> **Date:** September 2026
> **Context:** CVS-to-GitHub migration for a Computer Aided Engineering (CAE) software development team
> **Current Status:** GitHub Enterprise + Copilot trial completed successfully with Visual Studio 2026 Professional
> **GitHub Sales Contact:** Donovan Borje (pricing confirmed via email)

---

## Executive Summary

Buy 5 GitHub Enterprise seats with **Copilot Business** — not Copilot Enterprise — at **$200/month ($2,400/year)**, set a **$500/month team AI budget**, and run C++ builds on an on-premises runner. Expected all-in cost is **$482/month ($5,784/year)** for the whole team.

GitHub Support has confirmed that Copilot Business and Enterprise have **identical model availability and identical functionality**. The only difference is the included credit allowance. Choosing Business saves **$1,200/year** with no loss of capability.

| Line Item | Monthly | Annual | Note |
|---|---|---|---|
| GitHub Enterprise, 5 seats @ $21 | $105 | $1,260 | 50,000 Actions minutes, 50 GB packages, 250 GiB Git LFS |
| Copilot Business, 5 seats @ $19 | $95 | $1,140 | 9,500 pooled AI credits ($95 of model usage) |
| AI usage above included credits (expected) | $282 | $3,384 | Modelled team mix on a Claude Sonnet / GPT-5.4 class model |
| Repository hosting for the 1.2 GB repo | $0 | $0 | Git storage is not metered |
| CI builds on one on-prem runner | $0 | $0 | Self-hosted runner minutes are not billed |
| **Expected total** | **$482** | **$5,784** | |
| Worst case if every budget cap is hit | $1,450 | $17,400 | 5 × $250 AI budget fully consumed |

---

## 1. Understanding AI Credits vs. Tokens

GitHub Support calls them "tokens" and the figures they gave — 1,900 for Business and 3,900 for Enterprise — are correct. In GitHub's billing documentation the same units are called **AI credits**. They are **not tokens in the AI sense.**

> **1 AI credit = $0.01 USD.** A credit is a unit of money. A token is a unit of text. How many tokens one credit buys depends entirely on the model selected — from 2,000 tokens on Claude Opus to 50,000 on GPT-5.4 nano.

### How Many Tokens Does One Credit Buy?

| Model | 1 credit buys (fresh input) | 1 credit buys (cached input) | 1 credit buys (output) | 1 credit buys (typical agent mix) |
|---|---|---|---|---|
| GPT-5.4 nano | 50,000 tokens | 500,000 tokens | 8,000 tokens | ~64,000 tokens |
| Claude Haiku 4.5 | 10,000 | 100,000 | 2,000 | ~13,900 |
| Gemini 3.1 Pro | 5,000 | 50,000 | 833 | ~6,500 |
| GPT-5.4 (default) | 4,000 | 40,000 | 667 | ~5,200 |
| Claude Sonnet 4.5 / 4.6 | 3,333 | 33,333 | 667 | ~4,650 |
| Claude Opus 5 | 2,000 | 20,000 | 400 | ~2,800 |

---

## 2. Copilot Business vs. Enterprise — Why Business Is the Right Choice

|  | Copilot Business | Copilot Enterprise |
|---|---|---|
| Price per seat / month | $19 | $39 |
| Included AI credits / seat / month | 1,900 | 3,900 |
| Dollar value of included credits | $19 | $39 |
| Overage rate | $0.01 per credit | $0.01 per credit |
| **Model availability** | **Identical** | **Identical** |
| **Core functionality** | **Identical** | **Identical** |
| Requires GitHub Enterprise | No | **Yes** |
| Code completions & next-edit suggestions | Unlimited, never billed | Unlimited, never billed |
| Credits roll over | No | No |

### Copilot Enterprise Is Never Cheaper Than Business

Both plans include credits worth exactly their seat price. Both bill overage at $0.01 per credit. So the monthly cost is simply whichever is larger — the seat price, or what the developer consumed.

| Developer's actual model usage | Copilot Business cost | Copilot Enterprise cost | Business saving |
|---|---|---|---|
| $10 (light user) | $19 | $39 | **$20** |
| $19 | $19 | $39 | **$20** |
| $30 | $30 | $39 | **$9** |
| $39 | $39 | $39 | $0 |
| $75 | $75 | $75 | $0 |
| $108 (modelled heavy developer) | $108 | $108 | $0 |

Across 5 seats, Enterprise wastes up to **$1,200/year** in over-provisioned credits.

---

## 3. Purchase Options for 5 Users

| Option | Composition | Per User/Month | 5 Users/Month | 5 Users/Year |
|---|---|---|---|---|
| 1. Copilot only | GitHub Team $4 + Copilot Business $19 | $23 | $115 | $1,380 |
| **2. Enterprise + Business (recommended)** | **GitHub Enterprise $21 + Copilot Business $19** | **$40** | **$200** | **$2,400** |
| 3. Enterprise + Copilot Enterprise | GitHub Enterprise $21 + Copilot Enterprise $39 | $60 | $300 | $3,600 |

### GitHub's Own Pricing Examples (Confirmed by Donovan Borje)

| Users | GitHub Enterprise/Year | Copilot/Year | Total/Year |
|---|---|---|---|
| **5 (your deployment)** | **$1,260** | **$1,140** | **$2,400** |
| 10 | $2,520 | $2,280 | $4,800 |
| 50 | $12,600 | $11,400 | $24,000 |
| 75 | $18,900 | $17,100 | $36,000 |

---

## 4. How Many Tokens Does a C++ Developer Actually Use?

A developer doing **5 hours/day** of AI-assisted C++ work plus documentation consumes roughly **50 million tokens a month**, costing **$95-110 of AI credits** on a mainstream model (Claude Sonnet class).

### Bottom-Up Daily Consumption Model

| Activity | Times/Day | Tokens/Interaction | Daily Tokens |
|---|---|---|---|
| Agent-mode task (implement, refactor, fix, write tests) | 6 | ~320,000 | 1,920,000 |
| Copilot Chat question against the codebase | 25 | ~16,500 | 412,500 |
| Documentation / comment generation | 2 | ~46,000 | 92,000 |
| Code review assistance on a pull request | 1 | ~65,000 | 65,000 |
| **Total per developer per day** | | | **~2,490,000** |
| **Total per developer per month** (21 working days) | | | **~52,000,000** |

> **Note:** Code completions (inline autocomplete) are **free and unlimited** on every paid plan. They are not counted above because they never touch the budget.

### Monthly Cost Per Developer, by Intensity and Model

| Usage Tier | Tokens/Month | Haiku 4.5 | Gemini 3.1 Pro | GPT-5.4 | Sonnet 4.5/4.6 | Opus 5 |
|---|---|---|---|---|---|---|
| Light — 2 h/day, mostly chat | 15M | $11 | $23 | $29 | $32 | $54 |
| Moderate — 3-4 h/day, mixed | 30M | $22 | $46 | $57 | $65 | $108 |
| **Heavy — 5 h/day, agent-first** | **50M** | **$36** | **$76** | **$96** | **$108** | **$179** |
| Very heavy — parallel agents | 80M | $57 | $122 | $153 | $172 | $287 |

### What the Included Allowance Covers

| Model | Copilot Business (1,900 credits) | Copilot Enterprise (3,900 credits) | Days of heavy use covered |
|---|---|---|---|
| Claude Haiku 4.5 | 26.5M tokens | 54.4M tokens | 10.6 / 21.8 |
| Gemini 3.1 Pro | 12.4M | 25.5M | 5.0 / 10.2 |
| GPT-5.4 (default) | 9.9M | 20.4M | 4.0 / 8.2 |
| Claude Sonnet 4.5 / 4.6 | 8.8M | 18.1M | 3.5 / 7.3 |
| Claude Opus 5 | 5.3M | 10.9M | 2.1 / 4.4 |

> **Assessment:** On a mainstream model (Sonnet class), the Business allowance covers about **3.5 working days** and Enterprise covers **7.3 days**. Neither is sufficient for a full month of active C++ development. This confirms that a token overage budget is essential.

---

## 5. Model Choice Matters More Than Licence Tier

The cost spread across models is **46×**. This is the biggest cost lever, not the licence tier.

| Policy | Default Model | Expected Cost, 5 Developers, 175M tokens/month |
|---|---|---|
| Cost-first | Claude Haiku 4.5 / GPT-5.4 mini | $126/month |
| Balanced (recommended) | Gemini 3.1 Pro or GPT-5.4 | $267-334/month |
| Quality-first | Claude Sonnet 4.6 | $377/month |
| Unconstrained | Claude Opus 5 | $628/month |

**Practical policy:** Set a mid-tier default, let developers switch to a premium model for genuinely hard solver, numerical, or refactoring work, and review the usage dashboard monthly.

---

## 6. How Efficient Is a $250/Developer Budget?

A $250 monthly budget is a **cap on overage, not a committed spend**. GitHub bills only what is consumed.

|  | Copilot Business |
|---|---|
| Included credits | 1,900 |
| Budget credits ($250 @ $0.01) | 25,000 |
| **Total credits available/developer/month** | **26,900** |
| Expected consumption (heavy dev, Sonnet class) | 10,760 credits |
| **Budget utilisation** | **36% of the $250** |
| Expected actual overage billed | **$89** |

### Why $250 Per Developer Is the Wrong Shape

Credits pool at the org level. Five separate $250 caps create a $1,250 ceiling nobody will reach. A single **$500/month team budget** with a $150 per-user ceiling covers modelled demand and is a cap, not a committed spend.

### Modelled Team of 2 Heavy + 2 Moderate + 1 Light Developer (175M tokens/month)

| Model Used | Team Model Spend | Business Pool (9,500 cr) | Team Overage |
|---|---|---|---|
| Claude Haiku 4.5 | $126 | partially covers | $31 |
| Gemini 3.1 Pro | $267 | covers $95 | $172 |
| GPT-5.4 | $334 | covers $95 | $239 |
| Claude Sonnet 4.5 / 4.6 | $377 | covers $95 | **$282** |
| Claude Opus 5 | $628 | covers $95 | $533 |

---

## 7. Total Cost of Ownership — 5 Developers

### What You Ask Finance to Approve (Budget Ceiling)

| Line Item | Opt 1: Team + Copilot Business | **Opt 2: Enterprise + Copilot Business** | Opt 3: Enterprise + Copilot Enterprise |
|---|---|---|---|
| Platform licence, 5 users | $20 | **$105** | $105 |
| Copilot licence, 5 seats | $95 | **$95** | $195 |
| AI budget ceiling, 5 × $250 | $1,250 | **$1,250** | $1,250 |
| Repository hosting & LFS | $0 | **$0** | $0 |
| CI builds (self-hosted runner) | $0 | **$0** | $0 |
| **Maximum monthly cost** | **$1,365** | **$1,450** | **$1,550** |
| **Maximum annual cost** | **$16,380** | **$17,400** | **$18,600** |

### What You Will Actually Pay (Expected Spend)

| Line Item | Opt 1: Team + Business | **Opt 2: Enterprise + Business** | Opt 3: Enterprise + Copilot Enterprise |
|---|---|---|---|
| Platform licence, 5 users | $20 | **$105** | $105 |
| Copilot licence, 5 seats | $95 | **$95** | $195 |
| AI usage above pooled credits | $282 | **$282** | $182 |
| Repository hosting & LFS | $0 | **$0** | $0 |
| CI builds (self-hosted runner) | $0 | **$0** | $0 |
| **Expected monthly cost** | **$397** | **$482** | **$482** |
| **Expected annual cost** | **$4,764** | **$5,784** | **$5,784** |
| Per developer per month | $79 | **$96** | $96 |

> **Key insight:** Options 2 and 3 cost exactly the same at modelled usage. Enterprise moves $100/month from overage to the licence line and changes nothing else. The moment usage drops, Option 3 becomes more expensive.

---

## 8. Repository Hosting (1.2 GB Codebase)

**Hosting the repository costs nothing extra.** GitHub does not meter ordinary Git storage.

| Item | GitHub's Position | Your 1.2 GB Repo |
|---|---|---|
| Git repository storage | Not metered, no per-GB billing | **$0** |
| Recommended maximum repo size | 10 GB on-disk | Well inside |
| **Hard file size limit** | **100 MB per object — pushes rejected above this** | **Check before migrating** |
| Git LFS storage included | 250 GiB | **$0** |
| Git LFS bandwidth included | 250 GiB/month | **$0** |
| LFS above allowance | $0.07 per GiB/month | n/a |

> ⚠️ **Before migrating:** Inventory the CVS tree for files over 100 MB. Any single file above that will be rejected on push and the migration stalls.

---

## 9. Build Infrastructure — On-Premise Is Better for C++ CAE

### Standard 2-Core Runners Are Too Slow

Cloud runners are billed per minute and C++ builds are minute-hungry. At realistic build volumes the charge lands between **$98 and $807/month** depending on runner size.

| Runner | Rate/Minute | Monthly Cost (9,840 min) | Suitable for 1.2 GB C++ CAE? |
|---|---|---|---|
| Windows 2-core (standard) | $0.010 | $98 | ❌ No — build times 2-3x too long |
| Windows 4-core | $0.022 | $216 | ⚠️ Marginal |
| Windows 8-core | $0.042 | $413 | ✅ Realistic choice |
| Windows 16-core | $0.082 | $807 | ✅ Fastest |

> ⚠️ **Important:** Larger runners are always billed. The 50,000 included minutes only apply to standard 2-core runners, which are too slow for this build.

### Cost Comparison: Cloud vs. Self-Hosted (9,840 min/month)

|  | GitHub-Hosted Windows 8-core | Self-Hosted Windows 16-core |
|---|---|---|
| Actions minute charges | $413/month | **$0** |
| Hardware (16-core, 64 GB RAM, 2 TB NVMe) | — | $3,500 capex, ~$97/month over 3 years |
| Electricity (~250 W average) | included | ~$22/month |
| Rack space, network, UPS | included | ~$20/month |
| Administration (~2 h/month) | — | ~$100/month |
| **Total monthly cost** | **$413** | **$239** |
| **Monthly cash saving** | | **$271** |
| **Payback on new hardware** | | **12.9 months** |
| **Annual saving from year 2** | | **$3,252** |

### Why Self-Hosted Is Technically Superior for CAE

| Factor | GitHub-Hosted | Self-Hosted |
|---|---|---|
| Incremental C++ builds | ❌ Not possible — clean image each run | ✅ 4-8× faster |
| 1.2 GB repo checkout | Full clone every run | Warm working tree |
| Licensed CAE / third-party SDKs | Must install per run | Installed once |
| Visual Studio toolchain | Preinstalled versions only | Exact version developers use |
| Maintenance burden | None | Patching, disk, agent upgrades |

> **Recommendation:** Run everything that touches the C++ toolchain on a self-hosted Windows runner. Keep lightweight jobs (linting, markdown checks, release notes) on GitHub-hosted Linux runners where they fit inside the included allowance at no cost.

---

## 10. Bottom Line — What 5 Developers Cost Per Month and Annually

### Expected Monthly Cost: $482

| | Monthly | Annual |
|---|---|---|
| **Licences** (GitHub Enterprise + Copilot Business) | **$200** | **$2,400** |
| **AI token overage** (expected, Sonnet-class model) | **$282** | **$3,384** |
| **Repository hosting** | **$0** | **$0** |
| **Builds** (self-hosted runner) | **$0** | **$0** |
| **Total (expected)** | **$482** | **$5,784** |
| Per developer per month | **$96** | **$1,157** |

### With a Cost-First Model Policy: $316/month

If the team defaults to Gemini 3.1 Pro instead of Claude Sonnet:

| | Monthly | Annual |
|---|---|---|
| Licences | $200 | $2,400 |
| AI token overage | $116 | $1,392 |
| **Total** | **$316** | **$3,792** |

### Worst-Case (All Budgets Hit): $1,450/month

| | Monthly | Annual |
|---|---|---|
| Licences | $200 | $2,400 |
| AI budget ceiling (5 × $250) | $1,250 | $15,000 |
| **Total (maximum)** | **$1,450** | **$17,400** |

### ROI Context

> If Copilot saves each developer **3 hours a week** at a $50/hour loaded rate, that is **$3,000/month** of recovered capacity against an expected **$482/month** of cost — a **6× return on investment**.

---

## 11. Frequently Asked Questions

**Q: Why are we paying twice — once for GitHub and once for Copilot?**
A: They are separate products. GitHub Enterprise is where the code lives. Copilot is the AI assistant in Visual Studio. Copilot Business can be bought without GitHub Enterprise; Copilot Enterprise cannot.

**Q: Is the $250/developer budget an actual cost?**
A: No. It is a spending cap. GitHub bills only credits consumed. At modelled usage the team will use about $282/month of the $1,250 ceiling — roughly a quarter of the cap.

**Q: What happens when a developer runs out of tokens?**
A: You choose in advance: either usage stops until the next cycle, or it continues at $0.01/credit against a budget. Code completions keep working either way — they are free and unlimited.

**Q: Why Copilot Business rather than Enterprise?**
A: Enterprise costs $20 more per seat and delivers exactly $20 more in credits, with identical models and features. It can never come out cheaper. For any developer using less than $39/month of models it is strictly more expensive. Across 5 seats that is up to $1,200/year of avoidable spend.

**Q: Then why buy GitHub Enterprise at all?**
A: For single sign-on, the enterprise audit log, IP allow lists, 50,000 Actions minutes, and 50 GB of package storage. It has to justify itself on those grounds, not on Copilot. The net premium over GitHub Team is $1,020/year.

**Q: GitHub Support said "tokens." This document says "credits." Which is it?**
A: The same thing. GitHub's billing documentation calls the unit an AI credit and fixes it at $0.01. It is a unit of money, not text. The number of actual tokens it buys ranges from 2,000 on Claude Opus to 50,000 on GPT-5.4 nano — which is why model policy matters more than licence tier.

**Q: We saw 3,000 and 7,000 credits during the trial. Where did they go?**
A: Those were promotional allowances for June-August. They reverted to 1,900 and 3,900 on 1 September. The trial extension adds no credits — it only extends the period.

**Q: Do we get more AI models if we buy GitHub Enterprise?**
A: No. Every model in the catalogue is available on both plans at the same credit rates.

**Q: Our earlier estimate was $3,540/year. Why has it changed?**
A: That figure read GitHub's $2,280 Copilot line as 5 users at $38. It is actually 10 users at $19 — confirmed by the "Copilot only" examples. For 5 users: $2,400/year (Business) or $3,600/year (Enterprise).

**Q: Our repository is 1.2 GB. What does GitHub charge to host it?**
A: Nothing. Git repository storage is not metered. The only storage charges are LFS above 250 GiB and Packages above 50 GB. Neither is triggered by a 1.2 GB codebase.

**Q: Will the 1.2 GB repository even work on GitHub?**
A: Yes, well within GitHub's 10 GB guidance. The one blocker is the 100 MB per-file hard limit — any single library binary above that will be rejected on push.

**Q: Should we move libraries to Git LFS or Artifactory?**
A: Not for cost reasons — both are effectively free at this scale. Do it for clone times and developer experience.

**Q: Why on-prem build runners rather than the cloud?**
A: Two reasons. GitHub charges nothing for self-hosted runner minutes, saving about $271/month. More importantly, cloud runners are wiped between jobs, so every C++ build is a full rebuild. A persistent runner does incremental builds, typically 4-8× faster.

**Q: Can we start with fewer than 5 licences?**
A: Yes. Seats are monthly and can be added or removed. Starting with 3 heavy users and adding the rest after a month is a reasonable de-risking step.

**Q: Can we cancel if it doesn't work out?**
A: Yes. Copilot Business seats bill monthly and can be dropped. GitHub Support confirmed you can remove orgs from the Enterprise account and fall back to Copilot Business standalone. The repository is standard Git and can be moved to any other host without data loss.

**Q: How do we pay for Copilot Business?**
A: Credit card or Azure subscription only — GitHub does not offer annual invoicing for Business seats. If finance requires a single annual invoice, routing Copilot through an existing Azure agreement is the cleanest answer.

**Q: What is the return on this spend?**
A: Expected cost is $482/month for the team. If Copilot saves each developer 3 hours/week at $50/hour loaded rate, that is ~$3,000/month of recovered capacity — roughly **6× the cost**.

**Q: How do we know these token estimates are right?**
A: We don't — and that is stated plainly. This is a bottom-up model, not measured data. The trial is running, so one month of real usage dashboard data will replace the model. Budget for month 1 using this document, then re-forecast.

---

> *Sources: GitHub Support correspondence with Donovan Borje; [GitHub Pricing](https://github.com/pricing); [Copilot Plans](https://docs.github.com/en/copilot/get-started/plans); [Copilot Models & Pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing); [Actions Runner Pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing). All prices in USD.*
>
> *Related documents: [Copilot Business Token Credit Allocation](Copilot-Business-Token-Credit-Allocation.md) · [Copilot C++ Review, Models & Cost Guide](Copilot-CPP-Review-Models-Cost-Guide.md) · [CVS to GitHub Migration Report](CVS-to-GitHub-Migration-Detailed-Report.md)*
