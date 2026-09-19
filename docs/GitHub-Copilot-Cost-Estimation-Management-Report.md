# GitHub Enterprise & Copilot — Cost Estimation for CAE Software Development

> **Prepared for:** Management Review
> **Date:** September 2026
> **Context:** CVS-to-GitHub migration for a Computer Aided Engineering (CAE) software development team
> **Current Status:** GitHub Enterprise + Copilot trial completed successfully with Visual Studio 2026 Professional
> **GitHub Sales Contact:** Donovan Borje (pricing confirmed via email)

---

## Executive Summary

This document estimates the total cost of adopting GitHub Enterprise and GitHub Copilot for our C++ CAE development team, starting with a 5-user pilot. It covers licensing, AI token usage, repository hosting, build infrastructure, and provides a recommendation based on cost-efficiency.

| Scenario | Annual Cost (5 Users) | Monthly/User |
|---|---|---|
| **Option A:** GitHub Enterprise + Copilot Enterprise + $250 token budget | **$19,260** | **$321** |
| **Option B:** Copilot Business only + $250 token budget | **$16,140** | **$269** |
| **Option C:** GitHub Enterprise + Copilot Business + $250 token budget | **$17,940** | **$299** |
| **Recommended:** Option C for pilot phase | **$17,940** | **$299** |

---

## 1. Licensing Costs — GitHub Enterprise & Copilot

### Per-User Monthly Rates (Confirmed by GitHub Sales)

| Product | Monthly/User | Annual/User | Requires |
|---|---|---|---|
| **GitHub Enterprise** (repository hosting, security, SSO) | $21 | $252 | — |
| **Copilot Business** (AI coding assistant) | $19 | $228 | Any GitHub org (Free/Team/Enterprise) |
| **Copilot Enterprise** (AI + codebase indexing) | $39 | $468 | GitHub Enterprise required |

> **Key Insight from GitHub Sales (Donovan Borje):** "Model parity and functionality between Copilot Business and Enterprise will be the same" — the primary difference is the AI token allocation. Copilot Business does NOT require GitHub Enterprise.

### 5-User Cost Comparison

| Configuration | GitHub Enterprise | Copilot | Total Monthly | Total Annual |
|---|---|---|---|---|
| **GH Enterprise + Copilot Enterprise** | 5 × $21 = $105 | 5 × $39 = $195 | **$300** | **$3,600** |
| **GH Enterprise + Copilot Business** | 5 × $21 = $105 | 5 × $19 = $95 | **$200** | **$2,400** |
| **Copilot Business only** (no GH Enterprise) | $0 | 5 × $19 = $95 | **$95** | **$1,140** |

### What GitHub Enterprise Adds (vs. Free Org)

| Feature | Free/Team Org | GitHub Enterprise |
|---|---|---|
| Private repositories | ✅ | ✅ |
| Copilot Business | ✅ | ✅ |
| GitHub Actions CI/CD | ✅ (2,000 min) | ✅ (50,000 min) |
| SAML SSO / SCIM | ❌ | ✅ |
| Audit log API | ❌ | ✅ |
| IP allow lists | ❌ | ✅ |
| Advanced Security (code scanning) | ❌ | ✅ |
| Enterprise-managed policies | ❌ | ✅ |
| Git LFS included storage | 1 GB | 250 GB |

> **Recommendation:** Start with GitHub Enterprise + Copilot Business. Enterprise is needed for the 1.2 GB repository (LFS storage), 50,000 Actions minutes, and corporate SSO integration. Copilot Enterprise is not needed initially — Business provides the same AI functionality.

---

## 2. AI Token (Credit) Allocation

### What's Included with Each Plan

| | Copilot Business | Copilot Enterprise |
|---|---|---|
| **Monthly AI credits/user** | 1,900 | 3,900 |
| **Credit value** | $19.00 | $39.00 |
| **Credits pooled across org** | ✅ Yes | ✅ Yes |
| **5-user pool** | 9,500 credits ($95) | 19,500 credits ($195) |
| **Promotional (Jun-Aug 2026)** | 3,000/user | 7,000/user |
| **Standard (Sep 2026 onwards)** | 1,900/user | 3,900/user |
| **1 AI Credit** | = $0.01 USD | = $0.01 USD |

### What's Free (Unlimited) vs. What Uses Credits

| Feature | Uses Credits? | Impact |
|---|---|---|
| **Code completions** (inline autocomplete) | ❌ **FREE — Unlimited** | Most-used feature, no cost |
| **Next Edit Suggestions** | ❌ **FREE — Unlimited** | No cost |
| **Copilot Chat** | ⚠️ Yes | ~1-50 credits per question |
| **Agent Mode** (multi-step coding) | ⚠️ Yes — Heavy | ~50-1,000 credits per session |
| **PR Code Review** | ⚠️ Yes | ~10-100 credits per review |
| **Copilot CLI** | ⚠️ Yes | ~1-10 credits per command |

---

## 3. Token Consumption — C++ CAE Developer Working 5 Hours/Day

### Estimated Daily Token Usage

| Activity | Frequency (5hr day) | Credits/Instance | Daily Credits | Monthly (22 days) |
|---|---|---|---|---|
| **Code completions** | Continuous | **0** (free) | **0** | **0** |
| **Chat — simple questions** | 8-10/day | ~3-10 | ~30-100 | ~660-2,200 |
| **Chat — C++ reasoning (heavy)** | 5-8/day | ~20-80 | ~100-640 | ~2,200-14,080 |
| **Agent Mode — bug fixes** | 2-3/day | ~100-300 | ~200-900 | ~4,400-19,800 |
| **Agent Mode — complex refactoring** | 1-2/day | ~300-800 | ~300-1,600 | ~6,600-35,200 |
| **PR Code Reviews** | 1/day | ~30-100 | ~30-100 | ~660-2,200 |
| **Documentation generation** | 2-3/day | ~20-50 | ~40-150 | ~880-3,300 |
| **Total per developer** | | | **~700-3,490** | **~15,400-76,780** |

### Monthly Token Requirement by Usage Profile

| Developer Profile | Daily Credits | Monthly Credits | Monthly Cost (credits × $0.01) |
|---|---|---|---|
| **Light** (mostly completions + occasional chat) | ~200-500 | ~4,400-11,000 | $44-110 |
| **Moderate** (daily chat + weekly agent mode) | ~700-1,500 | ~15,400-33,000 | $154-330 |
| **Heavy C++ reasoning** (daily agent + reviews) | ~1,500-3,500 | ~33,000-77,000 | $330-770 |

> **Assessment:** The included 1,900 credits (Business) or 3,900 credits (Enterprise) will **NOT** be sufficient for active C++ development. A developer doing 5 hours of heavy AI-assisted work will need approximately **30,000-50,000 credits/month** ($300-500). The included allocation covers only 4-13% of heavy usage.

---

## 4. $250 Token Budget Per Developer — Efficiency Analysis

### What $250 Buys

| Component | Copilot Business | Copilot Enterprise |
|---|---|---|
| **Included credits** | 1,900 | 3,900 |
| **$250 overage budget** | 25,000 credits | 25,000 credits |
| **Total available/month** | **26,900 credits** | **28,900 credits** |

### How Far 26,900 Credits Go (Copilot Business + $250 Budget)

| Activity | Credits Used | How Many Per Month |
|---|---|---|
| Simple chat questions (~5 credits) | 5 | ~5,380 questions |
| Complex C++ reasoning (~50 credits) | 50 | ~538 questions |
| Agent Mode sessions (~200 credits) | 200 | ~134 sessions |
| Agent Mode complex (~500 credits) | 500 | ~54 sessions |
| PR reviews (~50 credits) | 50 | ~538 reviews |

### Realistic Daily Budget with $250/Month

```
26,900 credits ÷ 22 working days = ~1,223 credits/day

A developer can do:
  ✅ 10 simple chat questions           =  50 credits
  ✅ 5 complex C++ reasoning chats      = 250 credits
  ✅ 2 Agent Mode bug fixes             = 400 credits
  ✅ 1 complex Agent Mode refactoring   = 400 credits
  ✅ 1 PR code review                   =  50 credits
  ─────────────────────────────────────
  Total:                                1,150 credits/day ✅ Within budget

  Remaining buffer:                       73 credits/day (safety margin)
```

### Efficiency Assessment

| Metric | Value |
|---|---|
| **Is $250 sufficient?** | ✅ Yes, for moderate-to-heavy C++ development |
| **Daily capacity** | ~1,200 credits/day = robust AI-assisted workflow |
| **Risk of exhaustion** | Low if Agent Mode is used judiciously |
| **Optimization tip** | Use lightweight models for simple tasks → stretch budget 2-3× |

> **Verdict:** A $250/month token budget provides a developer with approximately **1,200 credits/day**, which supports a full 5-hour day of AI-assisted C++ development including chat, agent mode, and code review. This is a **cost-effective allocation** that balances productivity with budget control.

---

## 5. Total Monthly Cost Per Developer

### With $250 Token Budget

| Component | GH Enterprise + Copilot Enterprise | GH Enterprise + Copilot Business | Copilot Business Only |
|---|---|---|---|
| GitHub Enterprise seat | $21 | $21 | $0 |
| Copilot license | $39 | $19 | $19 |
| $250 token budget | $250 | $250 | $250 |
| **Total per user/month** | **$310** | **$290** | **$269** |
| **Total per user/year** | **$3,720** | **$3,480** | **$3,228** |

### 5-User Annual Cost

| Configuration | Licensing | Token Budget | **Total Annual** |
|---|---|---|---|
| **GH Enterprise + Copilot Enterprise** | $3,600 | $15,000 | **$18,600** |
| **GH Enterprise + Copilot Business** | $2,400 | $15,000 | **$17,400** |
| **Copilot Business only** | $1,140 | $15,000 | **$16,140** |

> **Note:** The actual token overage will likely be **less than $250/user/month** because:
> - Credits are **pooled** across the org — light users offset heavy users
> - Not every developer uses AI at maximum intensity every day
> - **Code completions are free** and represent the majority of daily AI interactions

---

## 6. Repository Hosting Cost (1.2 GB C++ Codebase)

### Current Repository Size: ~1.2 GB

| Storage Scenario | Included | Overage | Monthly Cost | Annual Cost |
|---|---|---|---|---|
| **Repo as-is (1.2 GB, all in Git)** | ⚠️ Exceeds 1 GB recommendation | Performance risk | Technically $0* | $0* |
| **Repo + Git LFS** (large files in LFS) | 250 GB LFS storage (Enterprise) | $0 (within limit) | **$0** | **$0** |
| **Repo + Artifactory** (libraries external) | Repo < 1 GB | Artifactory cost separate | Varies | Varies |

*\* GitHub does not charge per-GB for standard Git repositories but strongly recommends keeping repos under 1-5 GB. Files over 100 MB are blocked and MUST use Git LFS.*

### Recommended Approach: Git LFS for Large Files

| What | Size Estimate | Storage Type | Cost |
|---|---|---|---|
| Source code (.cpp, .h, .py, etc.) | ~200-400 MB | Standard Git | $0 (included) |
| Libraries / dependencies (.lib, .dll, .so) | ~600-800 MB | **Git LFS** | $0 (within 250 GB Enterprise limit) |
| Test data / mesh files (.inp, .msh, .dat) | ~100-200 MB | **Git LFS** | $0 (within 250 GB Enterprise limit) |
| **Total** | **~1.2 GB** | Mixed | **$0/month** |

> **With GitHub Enterprise's 250 GB LFS allowance, your 1.2 GB repository costs $0 additional for storage.** The LFS storage is more than sufficient. If you exceed 250 GB in the future, additional LFS storage costs $0.07/GiB/month.

### Alternative: Libraries in Artifactory

| Approach | Pros | Cons | Cost Impact |
|---|---|---|---|
| **Git LFS** (keep in GitHub) | Simpler workflow, one tool | Repo clone is still large | $0 (included) |
| **Artifactory** (external) | Repo stays small, versioned binary management | Separate infrastructure, build complexity | $500-2,000/year (Artifactory license) |

> **Recommendation:** Start with Git LFS (free with Enterprise). Move to Artifactory only if you need binary package management beyond simple storage.

---

## 7. Build Infrastructure — Cloud vs. On-Premise Runners

### GitHub-Hosted Runners (Cloud)

| Item | Details | Cost |
|---|---|---|
| **Included with Enterprise** | 50,000 minutes/month | $0 |
| **Runner type** | Ubuntu Linux, 2-core, 7 GB RAM | Standard |
| **Overage rate** | $0.006/minute (Linux 2-core) | Per-minute |
| **Larger runners** | 4-core: $0.016/min, 8-core: $0.032/min | Per-minute |

### C++ Build Time Estimation

| Build Type | Estimated Time | Monthly Frequency | Minutes/Month |
|---|---|---|---|
| Full C++ build (1.2 GB codebase) | 30-60 min | 20 builds | 600-1,200 min |
| Incremental build | 5-15 min | 100 builds | 500-1,500 min |
| Unit tests | 10-20 min | 100 runs | 1,000-2,000 min |
| **Total estimate** | | | **2,100-4,700 min/month** |

> **Verdict:** 50,000 included minutes is **more than sufficient** for a 5-developer team. You will not incur overage charges for builds.

### On-Premise (Self-Hosted) Runners — Cost Comparison

| Factor | GitHub-Hosted (Cloud) | Self-Hosted (On-Premise) |
|---|---|---|
| **Cost for 5,000 min/month** | **$0** (within 50K included) | Hardware + maintenance |
| **Setup effort** | Zero | Server setup, runner agent install |
| **Maintenance** | Zero | OS patches, monitoring, troubleshooting |
| **Build speed** | Standard (2-core shared VM) | **Faster** (dedicated hardware, NVMe SSD) |
| **Specialized toolchains** | Limited (standard Ubuntu) | **Full control** (custom C++ compilers, CAE tools) |
| **Cost at scale (50+ devs)** | May exceed 50K minutes → overage | Fixed cost regardless of usage |

### Self-Hosted Runner Recommendation for C++ CAE

| Scenario | Recommendation | Reason |
|---|---|---|
| **5-user pilot** | ✅ **Use GitHub-hosted** | Free (within 50K minutes), zero maintenance |
| **50-user rollout** | ⚠️ **Hybrid approach** | Simple builds in cloud, heavy C++ builds on-premise |
| **Specialized CAE toolchains** | ✅ **Self-hosted required** | Commercial solvers, custom compilers not available in cloud |
| **Air-gapped / compliance** | ✅ **Self-hosted required** | Code cannot leave corporate network |

> **Recommendation for pilot (5 users):** Use GitHub-hosted runners. Your ~5,000 min/month is well within the 50,000 included minutes. Switch to self-hosted later if build times become a bottleneck or you need specialized toolchains.

---

## 8. Complete Cost Summary — 5 Users, Year 1

### Recommended Configuration: GitHub Enterprise + Copilot Business + $250 Token Budget

| Cost Category | Monthly | Annual | Notes |
|---|---|---|---|
| **GitHub Enterprise** (5 users) | $105 | $1,260 | Repository hosting, SSO, 50K Actions minutes |
| **Copilot Business** (5 users) | $95 | $1,140 | AI coding assistant, 1,900 credits/user |
| **Token overage budget** (5 × $250) | $1,250 max | $15,000 max | Per-user budget caps, actual likely lower |
| **Git LFS storage** (1.2 GB) | $0 | $0 | Within 250 GB Enterprise allowance |
| **GitHub Actions** (~5K min/mo) | $0 | $0 | Within 50K included minutes |
| **Self-hosted runners** | $0 | $0 | Not needed for pilot |
| **Total (maximum)** | **$1,450** | **$17,400** | |
| **Total (realistic estimate)** | **~$950-1,200** | **~$11,400-14,400** | Token usage likely below max budget |

### Cost Per Developer Per Day

| Component | Daily Cost |
|---|---|
| GitHub Enterprise | $0.70 |
| Copilot Business | $0.63 |
| Token budget (max $250/mo) | $11.36 |
| **Total per developer per day** | **~$12.70** |

> **Context:** If Copilot saves each developer just **30 minutes per day** (conservative estimate for C++ development), and the fully-loaded cost of a developer is $80-120/hour, the daily savings are **$40-60** vs. a cost of **$12.70** — a **3-5× return on investment**.

---

## 9. Scaling Projections

| Team Size | GH Enterprise | Copilot Business | Token Budget ($250/user) | **Total Annual** |
|---|---|---|---|---|
| **5 users** | $1,260 | $1,140 | $15,000 | **$17,400** |
| **10 users** | $2,520 | $2,280 | $30,000 | **$34,800** |
| **25 users** | $6,300 | $5,700 | $75,000 | **$87,000** |
| **50 users** | $12,600 | $11,400 | $150,000 | **$174,000** |

> **Note:** At scale, token costs can be optimized by:
> - Reducing per-user budget from $250 to $150-200 based on actual usage data
> - Enabling auto-model selection (GitHub's recommended approach — potential 10% savings)
> - Setting team-level budgets that leverage credit pooling

---

## 10. Recommendation & Phased Approach

### Phase 1: Pilot (Months 1-3) — 5 Users

| Item | Cost | Action |
|---|---|---|
| GitHub Enterprise | $315 (3 months) | Upgrade from trial to paid |
| Copilot Business | $285 (3 months) | Enable for 5 developers |
| Token overage cap | $100/user/month | Conservative budget while measuring usage |
| **Phase 1 Total** | **~$2,100** | Validate productivity gains |

### Phase 2: Expansion (Months 4-12) — 10-25 Users

| Item | Action |
|---|---|
| Increase seats | Add developers based on pilot results |
| Adjust token budgets | Use Phase 1 data to set optimal per-user budgets |
| Evaluate self-hosted runners | If build times are a bottleneck |
| Consider Copilot Enterprise | Only if codebase indexing proves valuable |

### Phase 3: Full Rollout (Year 2) — 50 Users

| Item | Action |
|---|---|
| Negotiate volume pricing | Contact GitHub Sales for 50+ seat discounts |
| Implement self-hosted runners | For specialized C++ builds |
| Optimize token usage | Model selection, team budgets, usage policies |

---

## 11. Frequently Asked Questions (Q&A)

### Licensing

**Q: Can we use Copilot Business without GitHub Enterprise?**
A: Yes. Copilot Business ($19/user/month) works with any GitHub organization, including the free tier. GitHub Enterprise ($21/user/month) is only required for Copilot Enterprise ($39/user) or if you need SSO, audit logs, and advanced security features.

**Q: If we start with Copilot Enterprise, can we downgrade to Business later?**
A: Yes. Per GitHub Sales (Donovan Borje): "Remove all organizations from the Enterprise account and downgrade to GitHub Copilot Business."

**Q: Do all team members need GitHub Enterprise licenses, or just Copilot users?**
A: GitHub Enterprise bills for every member in the org. If you add 50 people, you pay 50 × $21 even if only 5 use Copilot. Copilot seats are assigned independently to specific users.

**Q: Is there a minimum number of seats for GitHub Enterprise?**
A: No minimum. You can start with 1 seat.

---

### Tokens & Credits

**Q: What happens when a developer runs out of tokens?**
A: Code completions (inline autocomplete) continue working — they're always free and unlimited. Chat, Agent Mode, and Code Review are blocked until the next billing cycle OR until overage billing is enabled.

**Q: Are tokens per-user or pooled?**
A: Pooled across the organization. A team of 5 users with Copilot Business shares 9,500 credits. Light users' unused credits offset heavy users' consumption.

**Q: What does 1 AI Credit cost?**
A: $0.01 USD. So 25,000 credits = $250.

**Q: Why did we run out of tokens during the trial?**
A: The trial allocation was 1,900 credits per user (standard rate). Agent Mode, which is extremely useful for C++ development, consumes 50-1,000 credits per session — meaning 2-3 agent sessions per day can exhaust the monthly allocation in under a week. This is normal for active development teams.

**Q: Can we set a hard spending cap to prevent surprise bills?**
A: Yes. Go to Org Settings → Billing → Budgets → set a monthly cap with "Stop usage when budget limit is reached" enabled. You can also set per-user limits.

---

### Repository & Storage

**Q: Our repository is 1.2 GB. Is that a problem?**
A: GitHub recommends repos under 1 GB. Individual files over 100 MB are blocked. Solution: Move large files (libraries, test data) to Git LFS. With GitHub Enterprise, you get 250 GB of LFS storage included — your 1.2 GB repo costs $0 additional.

**Q: Should we use Git LFS or Artifactory for our libraries?**
A: Start with Git LFS (free with Enterprise, simpler workflow). Consider Artifactory only if you need versioned binary package management, which adds $500-2,000/year in licensing.

**Q: How much does it cost to host a 1.2 GB repository on GitHub?**
A: $0 for the repository itself. GitHub does not charge per-GB for standard Git storage. With Enterprise, LFS storage (250 GB included) covers your large files at no extra cost.

---

### Builds & CI/CD

**Q: How many build minutes are included with GitHub Enterprise?**
A: 50,000 minutes/month on GitHub-hosted runners (Linux). For a 5-developer team building a C++ project, expected usage is ~5,000 min/month — well within the included allowance.

**Q: Is it cheaper to build C++ code on self-hosted runners?**
A: For a 5-user team, NO — use GitHub-hosted runners (free within 50K minutes). At scale (50+ users or specialized toolchains), self-hosted runners become cost-effective because you avoid per-minute charges and can use dedicated high-performance hardware.

**Q: Can we use our existing on-premise build servers as GitHub Actions runners?**
A: Yes. Install the GitHub Actions runner agent on any Linux/Windows/macOS server. Self-hosted runner usage on private repos is currently free from GitHub platform charges.

---

### Migration

**Q: How do we migrate from CVS to GitHub?**
A: Convert CVS history to Git using `cvs2git` or `cvs-fast-export`, then push to GitHub. A detailed migration guide has been prepared separately (see CVS-to-GitHub-Migration-Detailed-Report.md).

**Q: What about files over 100 MB?**
A: Track them with `git lfs track` BEFORE committing to Git. Order matters: configure LFS tracking → commit `.gitattributes` → then add large files.

---

### Visual Studio 2026

**Q: Does Visual Studio 2026 Professional include Copilot?**
A: Visual Studio 2026 includes the Copilot extension, but a Copilot subscription (Business or Enterprise) is required separately. The IDE license and Copilot license are independent costs.

**Q: How does Copilot index our C++ project in VS 2026?**
A: VS 2026 automatically indexes your solution in the background. Use `@workspace` or `#codebase` in Copilot Chat to query across all project files. Ensure all source files are included in your .sln/.vcxproj.

---

> *This document is part of the GitHub Enterprise & Copilot evaluation documentation suite.*
> *Related documents:*
> - *[Copilot Business Token Credit Allocation](Copilot-Business-Token-Credit-Allocation.md)*
> - *[Copilot C++ Review, Models & Cost Guide](Copilot-CPP-Review-Models-Cost-Guide.md)*
> - *[Copilot How It Works — Dev Team FAQ](Copilot-How-It-Works-Dev-Team-FAQ.md)*
> - *[CVS to GitHub Migration Report](CVS-to-GitHub-Migration-Detailed-Report.md)*
> - *[Copilot Security Assessment](Copilot-Security-Assessment.md)*
