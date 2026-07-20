# CVS → GitHub Migration — Executive Summary
## Detroit Engineered Products — Morpher Application

> **For:** DEP Engineering Team Presentation  
> **Date:** July 2026 | **Read time:** 5 minutes

---

## The Situation

DEP has used **CVS** for source control for **20+ years**. CVS was created in 1986 and has had no active development since 2008. It is now considered **obsolete**.

**Morpher** is a complex C++ desktop application that needs modern tools to remain competitive.

---

## The Proposal

Migrate from CVS to **GitHub Enterprise Cloud** with **GitHub Copilot** for AI-assisted development.

---

## At a Glance

```
TODAY                                    PROPOSED
─────                                    ────────
CVS (1986, obsolete)             →       GitHub (industry standard)
No code review                   →       Pull requests + AI review
No CI/CD                         →       GitHub Actions (auto build/test)
No AI tools                      →       Copilot in Visual Studio
Manual builds                    →       Automated pipelines
Single server (risk)             →       Distributed (every dev has full copy)
```

---

## Copilot vs Cursor AI — Why Copilot?

The team has asked about Cursor AI as an alternative. Here's the key difference:

| | GitHub Copilot | Cursor AI |
|---|---|---|
| **Works in Visual Studio 2022?** | ✅ **Yes — native** | ❌ **No** |
| **Works in Visual Studio 2017?** | ❌ No | ❌ No |
| **What is it?** | Plugin inside your IDE | Separate editor (VS Code fork) |
| **Cost per user** | $19/mo (Business) | $40/mo (Teams) |
| **Requires GitHub anyway?** | Included | Yes — still need GitHub |
| **IP legal protection** | ✅ Yes | ❌ No |

> **Bottom line:** Cursor cannot run inside Visual Studio. Since DEP's entire team uses Visual Studio for C++ development, **Copilot is the only option that works without changing IDEs**.

---

## What Does Copilot Do in Visual Studio?

| What You Already Have | What Copilot Adds |
|-----------------------|-------------------|
| IntelliSense autocomplete | AI code suggestions (full functions, not just keywords) |
| Manual code review (if any) | Automated PR review (catches bugs, style, patterns) |
| Debugger (breakpoints, watch) | Pre-debugging: catches issues before code runs |
| Error messages | AI explains errors and suggests fixes |
| — | Chat: ask questions about code in the IDE |
| — | C++ modernization agent (auto-upgrade old patterns) |

**Copilot and the debugger are complementary, not competing.**

---

## Cost Summary

### Per Developer

| Period | GitHub + Copilot | GitHub + Cursor | Savings with Copilot |
|--------|-----------------|----------------|---------------------|
| **Per Day** | **$1.32** | $2.01 | $0.69/day |
| **Per Month** | **$40** | $61 | $21/month |
| **Per Year** | **$480** | $732 | $252/year |

### For the Team

| Period | 50 Developers | 75 Developers |
|--------|--------------|---------------|
| **Per Month** | $2,000 | $3,000 |
| **Per Year** | $24,000 | $36,000 |
| **Year 1 (with migration)** | ~$39,000–$49,000 | ~$51,000–$61,000 |

> Code completions (the most-used feature) are **unlimited** — no extra charges.
> AI credits are pooled across the org — most teams stay within the included amount.

---

## Migration: How Hard Is It?

| Question | Answer |
|----------|--------|
| **How long?** | 8–10 weeks (phased approach) |
| **Is it risky?** | Low risk — CVS stays read-only as fallback |
| **Do we lose history?** | No — commit history is preserved during conversion |
| **What about our DLLs?** | Source code in Git, binaries via Git LFS or package manager |
| **What about builds?** | Self-hosted runners = same build servers, now automated |
| **Developer training?** | 2–3 half-day workshops + pilot team first |
| **What tool converts CVS?** | `cvs2git` — industry standard, well-proven |

---

## Build Pipeline (GitHub Actions)

```
Developer pushes code
        ↓
GitHub triggers auto-build  ←── Runs on YOUR existing build servers
        ↓
Copilot reviews the PR     ←── AI catches bugs before human review
        ↓
Human reviews the PR       ←── Focus on architecture & domain logic
        ↓
Tests run automatically
        ↓
Artifacts (EXE/DLL) saved
```

**Self-hosted runners:** Free — uses your own Windows build machines. No per-minute charges.

---

## VS 2017 Users: Action Required

| VS Version | Copilot Support | Action |
|-----------|----------------|--------|
| Visual Studio 2022 (17.10+) | ✅ Full | Enable Copilot |
| Visual Studio 2017 | ❌ None | **Must upgrade to VS 2022** |

> VS 2022 opens VS 2017 projects without modification. The upgrade is seamless.

---

## Key Benefits

| Benefit | Impact |
|---------|--------|
| 🔍 **Code review** | Every code change gets reviewed (AI + human) |
| 🤖 **AI assistance** | Copilot suggests, explains, and modernizes code |
| ⚡ **Faster builds** | Automated CI/CD with caching and parallel builds |
| 🛡️ **Security** | CodeQL scanning, secret detection, Dependabot |
| 📊 **Visibility** | Full audit trail, build history, team metrics |
| 🆕 **Hiring** | Every developer knows Git — zero CVS knowledge needed |
| 💾 **Backup** | Every clone is a full backup (no single point of failure) |
| 🌐 **Ecosystem** | Access to the world's largest developer platform |

---

## Recommendation

✅ **Migrate to GitHub Enterprise Cloud + Copilot Business**

- **$1.32/developer/day** for modern version control + AI
- 10-week phased migration with zero downtime risk
- Self-hosted runners for free CI/CD builds
- Skip Cursor — it doesn't work with Visual Studio

---

*Full technical details available in the [Detailed Report](file:///Users/rajeshellappan/.gemini/antigravity-ide/brain/22393411-b15f-4878-826e-963c89459e12/DEP-CVS-to-GitHub-Migration-Detailed-Report.md).*
