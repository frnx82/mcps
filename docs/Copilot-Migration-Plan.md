# GitHub Copilot Enterprise — Migration & Implementation Plan
## Prerequisites, Phase-by-Phase Rollout & Cost Estimation

> **For:** Engineering & Management Teams  
> **Date:** August 2026  
> **Scope:** Layer 1 — GitHub Copilot Enterprise for 50+ C++ developers  
> **Timeline:** 15-day demo → phased production rollout

---

## Table of Contents

1. [Two Scenarios — With GitHub vs With CVS](#1-two-scenarios)
2. [Prerequisites — What You Need Before Starting](#2-prerequisites)
3. [Phase 0: Demo in 15 Days (Proof of Concept)](#3-phase-0-demo-in-15-days)
4. [Phase 1: Foundation Setup (Weeks 1-2)](#4-phase-1-foundation-setup)
5. [Phase 2: Pilot Rollout (Weeks 3-4)](#5-phase-2-pilot-rollout)
6. [Phase 3: Full Migration — CVS to GitHub (Weeks 5-8)](#6-phase-3-full-migration)
7. [Phase 4: Full Copilot Rollout (Weeks 9-10)](#7-phase-4-full-copilot-rollout)
8. [Phase 5: Optimization & CVS Decommission (Weeks 11-12)](#8-phase-5-optimization)
9. [Cost Estimation — Enterprise + Consulting](#9-cost-estimation)
10. [Timeline Summary](#10-timeline-summary)

---

## 1. Two Scenarios

### Scenario A: CVS → GitHub Migration + Copilot Enterprise (Recommended)

```
CURRENT STATE:                       TARGET STATE:
  CVS (source control)                 GitHub Enterprise Cloud (source control)
  Visual Studio 2022 (IDE)    →        Visual Studio 2022 + Copilot Enterprise
  Manual code reviews                  Copilot-powered PR reviews
  No CI/CD automation                  GitHub Actions CI/CD
```

**Why recommended:** Copilot PR reviews, code search, and codebase indexing only work with code on GitHub. Full value of the $39/user investment.

### Scenario B: Keep CVS + Add Copilot Enterprise (Partial Value)

```
CURRENT STATE:                       TARGET STATE:
  CVS (source control — kept)          CVS (unchanged)
  Visual Studio 2022 (IDE)    →        Visual Studio 2022 + Copilot Enterprise
  Manual code reviews                  Manual code reviews (unchanged)
```

**What works:** Inline completions, Copilot Chat, code generation — all work on LOCAL files regardless of source control.

**What doesn't work without GitHub:**
- ❌ Copilot PR code reviews (requires GitHub PRs)
- ❌ Copilot code search (requires GitHub-hosted repos)
- ❌ Codebase indexing (Enterprise feature, GitHub repos only)
- ❌ GitHub Actions CI/CD

**You get ~60% of Copilot's value with CVS vs ~100% with GitHub.**

> **Recommendation:** Start with Scenario B for the 15-day demo (zero migration risk), then proceed with Scenario A for full value.

---

## 2. Prerequisites — What You Need Before Starting

### Mandatory Prerequisites

| # | Prerequisite | Status | Who Owns It | Effort |
|---|---|---|---|---|
| 1 | **GitHub Enterprise Cloud account** | ☐ Pending | IT / Admin | 1 day |
| 2 | **GitHub Organization** created under Enterprise | ☐ Pending | IT / Admin | 1 hour |
| 3 | **Copilot Enterprise** licenses purchased (50+ seats at $39/user/mo) | ☐ Pending vendor pricing | Management | 1 day |
| 4 | **Visual Studio 2022 v17.8+** on all developer machines | ☐ Verify | IT / Desktop Support | 1-3 days |
| 5 | **GitHub accounts** for all 50+ developers | ☐ Pending | IT / Admin | 1 day |
| 6 | **SAML/SSO** identity provider configured (Azure AD, Okta, etc.) | ☐ Pending | IT Security | 2-3 days |
| 7 | **Management approval** for code in cloud (GitHub's Azure servers) | ☐ Pending | CISO / Management | Decision |
| 8 | **Content exclusion list** — which code directories to block from Copilot | ☐ Pending | Tech Lead | 1 day |
| 9 | **Network access** — developers can reach `github.com` and `copilot.github.com` | ☐ Verify | Network / Firewall team | 1 day |

### For Demo Only (Scenario B — CVS Stays)

| # | Prerequisite | Status | Who Owns It | Effort |
|---|---|---|---|---|
| 1 | GitHub Enterprise trial or paid account | ☐ Pending | Admin | 1 day |
| 2 | Copilot Enterprise license (5-10 seats for demo) | ☐ Pending | Admin | 1 day |
| 3 | Visual Studio 2022 17.8+ (5-10 developer machines) | ☐ Verify | IT | 1 day |
| 4 | GitHub accounts for demo participants | ☐ Pending | Admin | 1 hour |
| 5 | Sample C++ project (non-sensitive) for demo | ☐ Prepare | Tech Lead | 1 day |

### For Full Migration (Scenario A — CVS to GitHub)

| # | Additional Prerequisite | Status | Who Owns It | Effort |
|---|---|---|---|---|
| 10 | **CVS repository audit** — total size, number of modules, branch count, history depth | ☐ Pending | Consultant | 1-2 days |
| 11 | **cvs2git or cvs-fast-export** tool installed and tested | ☐ Pending | Consultant | 1 day |
| 12 | **Git training plan** for developers (CVS → Git workflow changes) | ☐ Pending | Consultant | 1 day |
| 13 | **Branch strategy** decision (trunk-based, GitFlow, or GitHub Flow) | ☐ Pending | Tech Lead + Consultant | Decision |
| 14 | **CI/CD requirements** documented (current build process) | ☐ Pending | Build Engineer | 1 day |
| 15 | **Parallel run window** agreed (how long CVS and GitHub run side-by-side) | ☐ Pending | Management | Decision |

---

## 3. Phase 0: Demo in 15 Days (Proof of Concept)

> **Goal:** Show management and developers that Copilot Enterprise works with their C++ CAE code in Visual Studio 2022. No migration required.

### Day 1-3: Setup

| Day | Task | Owner |
|---|---|---|
| 1 | Request GitHub Enterprise trial (or purchase) | Admin |
| 1 | Create GitHub org, enable Copilot Enterprise | Admin + Consultant |
| 2 | Create GitHub accounts for 5-10 demo participants | Admin |
| 2 | Assign Copilot Enterprise licenses to demo users | Admin |
| 3 | Install/verify Visual Studio 2022 17.8+ on demo machines | IT |
| 3 | Sign in to GitHub from Visual Studio, enable Copilot extension | Demo users |

### Day 4-5: Prepare Demo Environment

| Day | Task | Owner |
|---|---|---|
| 4 | Create a sample GitHub repo with representative C++ code | Consultant |
| 4 | Upload `copilot-instructions.md` with CAE-specific review rules | Consultant |
| 5 | Configure content exclusion for sensitive directories (if any) | Admin + Consultant |
| 5 | Test Copilot completions, chat, and review on sample code | Consultant |

### Day 6-10: Developer Trial

| Day | Task | Owner |
|---|---|---|
| 6-10 | 5-10 developers use Copilot on their daily C++ work | Demo users |
| 6-10 | Developers work on LOCAL files from CVS (no migration needed) | Demo users |
| 6-10 | Consultant collects feedback — what worked, what didn't | Consultant |
| 8 | Mid-trial check-in with team | Consultant |

### Day 11-13: Demonstrate Value

| Day | Task | Owner |
|---|---|---|
| 11 | Compile developer feedback and productivity observations | Consultant |
| 12 | Prepare demo presentation with before/after examples | Consultant |
| 13 | Create a sample PR on GitHub to show Copilot PR review capability | Consultant |

### Day 14-15: Management Presentation

| Day | Task | Owner |
|---|---|---|
| 14 | Present demo results to management | Consultant + Tech Lead |
| 15 | Go/No-Go decision for full rollout | Management |

### Demo Deliverables

- ✅ Working Copilot Enterprise in Visual Studio 2022
- ✅ Developer feedback report (5-10 developers, 5 days of usage)
- ✅ Sample `copilot-instructions.md` tailored for the C++ CAE codebase
- ✅ Copilot PR review demo on sample GitHub repo
- ✅ Security configuration demonstration (content exclusion, audit logs)
- ✅ Cost projection for 50+ developer full rollout

---

## 4. Phase 1: Foundation Setup (Weeks 1-2)

> **After demo approval.** Set up GitHub Enterprise and security controls.

| Week | Task | Owner | Deliverable |
|---|---|---|---|
| 1 | Purchase GitHub Enterprise Cloud (50+ seats) | Admin / Procurement | Active Enterprise account |
| 1 | Purchase Copilot Enterprise licenses (50+ seats) | Admin / Procurement | Licenses provisioned |
| 1 | Configure SAML/SSO integration | IT Security | SSO login working |
| 1 | Set up Enterprise Managed Users (if chosen) | IT / Admin | Managed user accounts |
| 2 | Create GitHub organization structure (teams, repos) | Consultant | Org configured |
| 2 | Configure content exclusion policies | Admin + Tech Lead | Sensitive paths excluded |
| 2 | Enable audit logging | Admin | Audit trail active |
| 2 | Set organization-wide Copilot policies | Admin | Policies enforced |

---

## 5. Phase 2: Pilot Rollout — Copilot on CVS (Weeks 3-4)

> **All 50+ developers get Copilot.** Code stays on CVS. No migration yet.

| Week | Task | Owner | Deliverable |
|---|---|---|---|
| 3 | Install VS 2022 Copilot extension on all developer machines | IT + Developers | All devs connected |
| 3 | Deploy `copilot-instructions.md` with C++ CAE rules | Consultant | Review rules active |
| 3 | Deploy path-specific instruction files (solver, mesh, IO) | Consultant | Module rules active |
| 3 | Developer training session (1 hour) — Copilot basics | Consultant | Team trained |
| 4 | Monitor usage, collect feedback | Consultant | Usage report |
| 4 | Tune copilot-instructions based on developer feedback | Consultant | Optimized rules |
| 4 | Address issues and edge cases | Consultant | Issues resolved |

> At this point, all developers have Copilot working on their LOCAL C++ files from CVS. Inline completions, chat, and code generation are fully functional. PR reviews are NOT available yet (need GitHub).

---

## 6. Phase 3: Full Migration — CVS to GitHub (Weeks 5-8)

> **The big migration.** CVS history is converted to Git and pushed to GitHub.

### Week 5: CVS Audit & Preparation

| Task | Owner | Deliverable |
|---|---|---|
| Full CVS repository audit (modules, size, branch count) | Consultant | Audit report |
| Identify CVS modules to migrate (priority order) | Tech Lead + Consultant | Migration priority list |
| Install and test cvs2git / cvs-fast-export | Consultant | Tool ready |
| Define Git branch strategy (GitHub Flow recommended) | Consultant + Tech Lead | Branch strategy doc |
| Set up GitHub repos (one per CVS module or monorepo) | Consultant | Repos created |

### Week 6: Migration Execution (Non-Production First)

| Task | Owner | Deliverable |
|---|---|---|
| Convert first CVS module to Git (with full history) | Consultant | First repo migrated |
| Validate history, branches, tags are correct | Consultant + Tech Lead | Validation report |
| Push to GitHub, set up branch protection rules | Consultant | Protected main branch |
| Set up CODEOWNERS file | Tech Lead | Review assignments |
| Create PR template with checklist | Consultant | PR template ready |

### Week 7: Migration Execution (Remaining Modules)

| Task | Owner | Deliverable |
|---|---|---|
| Convert remaining CVS modules to Git | Consultant | All repos migrated |
| Set up GitHub Actions CI/CD (MSBuild + tests) | Consultant | CI pipeline active |
| Configure Copilot PR reviews on migrated repos | Consultant | PR reviews enabled |
| Developer training session (1 hour) — Git workflow, PRs | Consultant | Team trained on Git |

### Week 8: Parallel Run & Validation

| Task | Owner | Deliverable |
|---|---|---|
| Parallel run: developers commit to both CVS and GitHub | All developers | Dual-commit workflow |
| Validate builds work from GitHub (MSBuild via Actions) | Consultant + Build Engineer | Build validated |
| Test Copilot PR reviews on real PRs | Developers | PR reviews working |
| Address migration issues | Consultant | Issues resolved |

---

## 7. Phase 4: Full Copilot Rollout (Weeks 9-10)

> **Copilot now has full power** — PR reviews, codebase indexing, search.

| Week | Task | Owner | Deliverable |
|---|---|---|---|
| 9 | Enable codebase indexing (Enterprise feature) | Admin | Indexing active |
| 9 | All developers switch primary source to GitHub | All developers | CVS → GitHub cutover |
| 9 | Copilot PR review training session | Consultant | Team trained |
| 10 | Monitor full-stack usage (completions + chat + PR reviews) | Consultant | Usage dashboard |
| 10 | Tune content exclusion and review rules based on real PRs | Consultant | Optimized config |
| 10 | Knowledge transfer to internal admin | Consultant | Admin self-sufficient |

---

## 8. Phase 5: Optimization & CVS Decommission (Weeks 11-12)

| Week | Task | Owner | Deliverable |
|---|---|---|---|
| 11 | Final CVS sync — ensure all commits are in GitHub | Consultant | Sync verified |
| 11 | Set CVS to read-only | Admin | CVS locked |
| 11 | Productivity report — before vs after metrics | Consultant | ROI report |
| 12 | CVS archive (keep backup for compliance) | Admin | CVS archived |
| 12 | Project close, final documentation | Consultant | Project complete |

---

## 9. Cost Estimation

### GitHub Enterprise + Copilot Licensing

| Item | Per User/Month | 50 Users/Month | Annual (50 users) |
|---|---|---|---|
| GitHub Enterprise Cloud | $21 | $1,050 | $12,600 |
| Copilot Enterprise | $39 | $1,950 | $23,400 |
| **Total licensing** | **$60** | **$3,000** | **$36,000** |

> ⚠️ Pricing under negotiation with vendor. Volume discounts may apply for 50+ seats.

### Demo Phase Licensing (15 Days, 10 Users)

| Item | 10 Users × 1 Month | Notes |
|---|---|---|
| GitHub Enterprise Cloud | $210 | 1 month trial or paid |
| Copilot Enterprise | $390 | 10 seats × $39 |
| **Demo phase total** | **$600** | One-time for 15-day demo |

### Total Project Cost — Year 1

| Cost Category | Demo Only | Demo + Copilot (CVS stays) | Full Package (Migration + Copilot) |
|---|---|---|---|
| **GitHub Enterprise licensing** | $210 (1 mo, 10 users) | $12,600/year (50 users) | $12,600/year |
| **Copilot Enterprise licensing** | $390 (1 mo, 10 users) | $23,400/year (50 users) | $23,400/year |
| **Total Year 1** | **$600** | **$36,000** | **$36,000** |
| **Ongoing annual (Year 2+)** | — | $36,000 (licensing only) | $36,000 (licensing only) |

> ⚠️ Migration execution costs (tooling, CI/CD setup, training) are separate and depend on whether internal teams or external support handles the work.

### Cost Per Developer Per Month

| Scenario | Monthly/Dev | Annual/Dev |
|---|---|---|
| Demo only (10 devs) | $60 (licensing) | $720 |
| Copilot on CVS (50 devs) | $60 (licensing) | $720 |
| Full migration (50 devs) | $60 (licensing) | $720 |

---

## 10. Timeline Summary

```
AGGRESSIVE TIMELINE — 14 WEEKS TOTAL

Week  0         Demo Prep ░░░
Week  1-2       PHASE 0: 15-Day Demo ████████████████
                ↓ Management Go/No-Go Decision
Week  3-4       PHASE 1: Foundation ████████
Week  5-6       PHASE 2: Copilot on CVS ████████
Week  7-10      PHASE 3: CVS → GitHub Migration ████████████████
Week  11-12     PHASE 4: Full Copilot Rollout ████████
Week  13-14     PHASE 5: Optimization & Close ████████

KEY MILESTONES:
  Day 15:    Demo complete → Go/No-Go
  Week 6:    All 50 devs have Copilot (on CVS)
  Week 10:   All code on GitHub, PR reviews active
  Week 14:   CVS decommissioned, project complete
```

### If CVS Stays (No Migration)

```
SHORTER TIMELINE — 6 WEEKS

Week  0         Demo Prep ░░░
Week  1-2       PHASE 0: 15-Day Demo ████████████████
                ↓ Management Go/No-Go Decision
Week  3-4       PHASE 1: Foundation + Copilot Setup ████████
Week  5-6       PHASE 2: Full Rollout + Optimization ████████
                ↓ Done (but no PR reviews or code search)
```

---

> **Next step:** Complete prerequisites (Section 2), then kick off Phase 0 demo. The 15-day demo requires minimal licensing investment ($600) and gives management concrete evidence to approve the full rollout.
