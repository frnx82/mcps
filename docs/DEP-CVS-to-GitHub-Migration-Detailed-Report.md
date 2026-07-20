# CVS to GitHub Migration — Detailed Technical Report
## Detroit Engineered Products (DEP) — Morpher C++ Application

> **Prepared for:** DEP Engineering Leadership & Development Team  
> **Date:** July 2026  
> **Scope:** Migration from CVS to GitHub, Copilot Integration, CI/CD, Cost Analysis

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Why Migrate from CVS to GitHub?](#2-why-migrate-from-cvs-to-github)
3. [CVS vs GitHub — Feature Comparison](#3-cvs-vs-github--feature-comparison)
4. [GitHub Copilot — What It Can Do for C++ Code Review](#4-github-copilot--what-it-can-do-for-c-code-review)
5. [Visual Studio C++ Integration — 2017 vs 2022](#5-visual-studio-c-integration--2017-vs-2022)
6. [Copilot vs Traditional VS Debugging — How They Complement Each Other](#6-copilot-vs-traditional-vs-debugging--how-they-complement-each-other)
7. [Cost Analysis — GitHub Enterprise + Copilot for 50–75 Developers](#7-cost-analysis--github-enterprise--copilot-for-5075-developers)
8. [GitHub Copilot vs Cursor AI — Comparison & Why Copilot Wins for DEP](#8-github-copilot-vs-cursor-ai--comparison--why-copilot-wins-for-dep)
9. [Detailed Copilot Usage Cost — Daily / Monthly / Yearly for 50–75 Developers](#9-detailed-copilot-usage-cost--daily--monthly--yearly-for-5075-developers)
10. [GitHub Actions Runners — C++ Build Costs](#10-github-actions-runners--c-build-costs)
11. [Migration Plan — CVS to GitHub](#11-migration-plan--cvs-to-github)
12. [DLL & Library Migration — Complexities & Solutions](#12-dll--library-migration--complexities--solutions)
13. [Build Comparison — CVS vs GitHub](#13-build-comparison--cvs-vs-github)
14. [GitHub Peer Review & Governance Setup](#14-github-peer-review--governance-setup)
15. [Risk Assessment & Mitigation](#15-risk-assessment--mitigation)
16. [Recommended Roadmap & Timeline](#16-recommended-roadmap--timeline)
17. [Conclusion](#17-conclusion)

---

## 1. Executive Summary

Detroit Engineered Products has relied on CVS (Concurrent Versions System) for 20+ years to manage the source code for **Morpher**, a complex C++ desktop application for Computer-Aided Engineering (CAE). While CVS served its purpose, it is now considered **obsolete** by the software industry. Migrating to **GitHub** with **GitHub Copilot** integration will provide:

- **Modern collaboration** — Pull requests, code reviews, branching workflows
- **AI-assisted development** — GitHub Copilot for code suggestions, reviews, and modernization
- **Automated CI/CD** — GitHub Actions for building, testing, and releasing Morpher
- **Enterprise security** — SAML SSO, audit logs, branch protection, IP whitelisting
- **Industry standard tooling** — Access to the world's largest developer ecosystem

> [!IMPORTANT]
> CVS has no active maintenance, no modern tooling support, and no AI integration path. Every year of delay increases the technical debt and makes the eventual migration more complex.

---

## 2. Why Migrate from CVS to GitHub?

### The Problem with CVS in 2026

CVS was created in **1986** and last had a significant release in **2008**. After 20+ years of use:

| Problem | Impact on DEP |
|---------|---------------|
| **No branching model** | CVS branching is slow, error-prone, and discourages parallel development |
| **No atomic commits** | A commit in CVS is per-file, not per-changeset — partial commits can corrupt the repository |
| **No offline work** | Developers need network access to the CVS server for every operation |
| **No code review** | CVS has zero built-in support for peer review or pull requests |
| **No CI/CD integration** | Cannot trigger automated builds, tests, or deployments |
| **No AI tools** | Copilot, CodeQL, and modern AI assistants do not support CVS |
| **Single point of failure** | If the CVS server goes down, all development stops |
| **No talent availability** | New hires will not know CVS — Git is taught in every CS program |
| **Security risks** | CVS has known, unpatched security vulnerabilities |
| **No ecosystem** | No extensions, integrations, or community support |

### What GitHub Brings

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Current State (CVS)                             │
│                                                                     │
│   Developer ──► CVS Server ──► Manual build ──► Manual test         │
│       │              │                                               │
│       │         (single point                                        │
│       │          of failure)        No code review                   │
│       │                             No CI/CD                         │
│       │                             No AI assistance                 │
│       └── Must be online to commit                                   │
└─────────────────────────────────────────────────────────────────────┘

                              ▼▼▼

┌─────────────────────────────────────────────────────────────────────┐
│                     Future State (GitHub)                            │
│                                                                     │
│   Developer ──► Local Git ──► Push ──► GitHub (Cloud)               │
│       │              │                     │                         │
│       │         Works offline        ┌─────┴──────┐                  │
│       │                              │            │                  │
│       │                     Pull Requests    GitHub Actions          │
│       │                     + Copilot Review + Auto Build/Test       │
│       │                              │            │                  │
│       └── Full repo copy       Peer Review    Automated CI/CD       │
│           (distributed)        AI Review      Deploy Pipeline        │
└─────────────────────────────────────────────────────────────────────┘
```

> 📐 **Interactive Diagram:** Open [01-cvs-vs-github-architecture.excalidraw](diagrams/01-cvs-vs-github-architecture.excalidraw) in Excalidraw for the full visual version.

---

## 3. CVS vs GitHub — Feature Comparison

| Feature | CVS (Current) | GitHub + Git (Proposed) |
|---------|---------------|------------------------|
| **Architecture** | Centralized — single server | Distributed — every dev has full copy |
| **Branching** | Slow, complex, error-prone | Instant, lightweight, encouraged |
| **Merging** | Manual, conflict-heavy | Smart 3-way merge, rebase support |
| **Commits** | Per-file (non-atomic) | Per-changeset (atomic) |
| **Offline work** | ❌ Not possible | ✅ Full commit/branch/diff offline |
| **Code review** | ❌ None | ✅ Pull requests with inline comments |
| **AI assistance** | ❌ None | ✅ Copilot for code + review |
| **CI/CD** | ❌ None | ✅ GitHub Actions (built-in) |
| **Security scanning** | ❌ None | ✅ CodeQL, Dependabot, secret scanning |
| **Audit trail** | Basic server logs | Full audit log, SIEM integration |
| **Access control** | Limited | Branch protection, CODEOWNERS, RBAC |
| **Binary file handling** | Stored in repo (bloat) | Git LFS for large files |
| **IDE integration** | Minimal | Native in VS 2022, VS Code, JetBrains |
| **Speed** | Network-bound for every op | Local operations are instant |
| **Disaster recovery** | Server backup only | Every clone is a full backup |
| **Community / Ecosystem** | Dead — no active development | 100M+ developers, largest ecosystem |
| **New hire onboarding** | Training required (nobody knows CVS) | Standard skill — all devs know Git |
| **Status** | ⚠️ Obsolete since ~2008 | ✅ Industry standard |

---

## 4. GitHub Copilot — What It Can Do for C++ Code Review

### 4.1 Overview

GitHub Copilot is an AI-powered development assistant that integrates directly into the IDE and the GitHub pull request workflow. For a C++ CAE application like Morpher, it provides two major capabilities:

1. **In-IDE assistance** — Real-time code suggestions, chat, and modernization
2. **Pull request review** — Automated review comments on every code change

### 4.2 Types of Reviews Copilot Can Perform

#### ✅ What Copilot Handles Well (High Confidence)

| Review Category | Examples for Morpher C++ |
|----------------|--------------------------|
| **Code quality** | Naming conventions, unused variables, dead code detection |
| **Modern C++ patterns** | Suggests `std::unique_ptr` over raw `new/delete`, range-based for loops, `auto` usage |
| **Common bug patterns** | Off-by-one errors, `=` vs `==`, null pointer checks, uninitialized variables |
| **API misuse** | Wrong parameter order, incorrect STL usage, deprecated function calls |
| **Style consistency** | Enforces team coding standards via `.github/copilot-instructions.md` |
| **Boilerplate generation** | Operator overloads, copy/move constructors, serialization code |
| **Documentation** | Generates docstrings, comments, and README content |
| **Refactoring suggestions** | Extract functions, simplify complex conditionals, reduce duplication |
| **Build configuration** | Analyzes CMake/MSBuild files, suggests optimizations |

#### ⚠️ What Copilot Handles Partially (Medium Confidence)

| Review Category | Copilot Capability | Recommendation |
|----------------|--------------------|-----------------| 
| **Memory management** | Can spot obvious leaks (missing `delete`) but misses complex ownership chains | Pair with AddressSanitizer |
| **Thread safety** | Identifies simple race conditions, misses complex concurrent patterns | Use ThreadSanitizer in CI |
| **Performance hotspots** | Suggests basic optimizations (move semantics, reserve) but can't profile | Use VTune/perf for profiling |
| **Template metaprogramming** | Understands basic templates, struggles with heavy TMP | Human review required |
| **Platform-specific code** | Knows Win32 API basics but not deep COM/ATL patterns | Human review required |

#### ❌ What Copilot Cannot Do (Human Review Required)

| Area | Why Copilot Falls Short |
|------|------------------------|
| **CAE algorithm correctness** | Cannot verify finite element math, mesh quality algorithms, or solver convergence |
| **Domain-specific logic** | Doesn't understand engineering physics, material models, or optimization algorithms |
| **Architecture decisions** | Cannot evaluate if a design pattern is appropriate for Morpher's architecture |
| **Security-critical code** | Should not be sole reviewer for licensing, encryption, or auth code |
| **Complex buffer overflows** | Not a formal verification engine — use CodeQL/static analysis tools |
| **Business requirements** | Cannot validate if code meets customer specifications |

### 4.3 Example: Copilot Review on a Morpher Pull Request

```
┌──────────────────────────────────────────────────────────────────┐
│  Pull Request: "Optimize mesh refinement for large models"       │
│  Author: John D. │ Reviewers: AI (Copilot) + Sarah M.          │
│─────────────────────────────────────────────────────────────────│
│                                                                  │
│  🤖 Copilot Review (automated — runs in ~30 seconds):           │
│                                                                  │
│  ⚠️  Line 142: Raw pointer `Node* node = new Node()` — consider │
│     using `std::unique_ptr<Node>` for automatic memory cleanup   │
│     [Apply fix]                                                  │
│                                                                  │
│  ⚠️  Line 267: Loop variable `i` is `int` but compared with     │
│     `size_t` return value — potential signed/unsigned mismatch   │
│     [Apply fix]                                                  │
│                                                                  │
│  💡 Line 389: `std::vector::push_back` in tight loop — consider │
│     `reserve()` before loop for ~2x performance improvement     │
│                                                                  │
│  ✅ Line 450: Good use of move semantics in return value         │
│                                                                  │
│  👤 Human Review (Sarah M. — 45 min):                           │
│                                                                  │
│  "The refinement algorithm looks correct for hex elements but    │
│   doesn't handle degenerate tet cases. Adding unit test for      │
│   collapsed edge case."                                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.4 Complexity Levels Copilot Can Handle

```
Complexity Level    │ Copilot Effectiveness │ Example in Morpher
────────────────────┼───────────────────────┼──────────────────────────────
Low                 │ ████████████ 95%      │ Variable naming, code style,
                    │                       │ missing includes, typos
────────────────────┼───────────────────────┼──────────────────────────────
Medium              │ █████████░░░ 75%      │ STL misuse, simple memory
                    │                       │ leaks, error handling gaps
────────────────────┼───────────────────────┼──────────────────────────────
High                │ █████░░░░░░░ 45%      │ Thread safety, complex
                    │                       │ template code, platform APIs
────────────────────┼───────────────────────┼──────────────────────────────
Domain-Specific     │ ██░░░░░░░░░░ 15%      │ FEA solver math, mesh
                    │                       │ algorithms, CAE physics
```

> [!TIP]
> **The sweet spot**: Copilot handles the "boring but important" 60–70% of code review (style, bugs, patterns) so your senior engineers can focus on the "hard 30–40%" (algorithms, architecture, domain logic).

---

## 5. Visual Studio C++ Integration — 2017 vs 2022

### 5.1 Visual Studio 2022 — Full Copilot Support ✅

GitHub Copilot is **natively integrated** into Visual Studio 2022 (version 17.10+):

| Feature | Availability |
|---------|-------------|
| **Code completions** | ✅ Real-time suggestions as you type |
| **Copilot Chat** | ✅ Ask questions about code in a sidebar |
| **Inline Chat** | ✅ Select code → ask Copilot to explain/refactor/fix |
| **`@Modernize` agent** | ✅ Automated C++ modernization (raw pointers → smart pointers, etc.) |
| **Build error assistance** | ✅ Copilot explains and suggests fixes for MSVC errors |
| **Context-aware** | ✅ Uses IntelliSense engine to understand symbols, headers, dependencies |
| **Cross-file awareness** | ✅ References related headers/source files even if not open |

**How to install:** Copilot is installed via the **Visual Studio Installer** as part of the workload — not from the Extension Marketplace.

### 5.2 Visual Studio 2017 — No Copilot Support ❌

| Feature | Availability |
|---------|-------------|
| **GitHub Copilot** | ❌ **Not supported** |
| **Copilot Chat** | ❌ Not available |
| **Any AI features** | ❌ None |

> [!WARNING]
> **Visual Studio 2017 does NOT support GitHub Copilot.** There is no workaround, extension, or plugin available. To use Copilot, developers **must** use Visual Studio 2022 (17.10+).

### 5.3 Recommendation for DEP

| Current Setup | Recommended Action |
|--------------|-------------------|
| Developers on VS 2017 | **Upgrade to VS 2022** (free Community edition or paid Professional/Enterprise) |
| Developers on VS 2022 | Update to version 17.10+ and enable Copilot via Installer |
| Mixed environment | Standardize on VS 2022 — maintains backward compatibility with VS 2017 projects |

> [!NOTE]
> Visual Studio 2022 opens and builds VS 2017 projects without modification. The migration is typically seamless for `.sln` and `.vcxproj` files.

---

## 6. Copilot vs Traditional VS Debugging — How They Complement Each Other

A common question: *"We already have debugging in Visual Studio. What does Copilot add?"*

**Answer: Copilot and debugging solve different problems at different stages.**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Development Lifecycle                             │
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  Write   │ ──►│  Review  │ ──►│  Build   │ ──►│  Debug   │      │
│  │  Code    │    │  Code    │    │  & Test  │    │  Issues  │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│       ▲               ▲               ▲               ▲            │
│  ┌────┴────┐    ┌─────┴─────┐   ┌────┴────┐    ┌─────┴─────┐     │
│  │ Copilot │    │  Copilot  │   │ GitHub  │    │    VS     │      │
│  │ Suggest │    │  PR Review│   │ Actions │    │ Debugger  │      │
│  │ in IDE  │    │  + Human  │   │  CI/CD  │    │ Breakpts  │      │
│  └─────────┘    └───────────┘   └─────────┘    └───────────┘      │
│                                                                     │
│  ◄──── Copilot (BEFORE bugs exist) ────►  ◄── Debugger (AFTER) ──► │
└─────────────────────────────────────────────────────────────────────┘
```

| Aspect | VS Debugger (Current) | GitHub Copilot (New) |
|--------|----------------------|---------------------|
| **When it helps** | After a bug is found | Before bugs are introduced |
| **What it does** | Steps through running code line-by-line | Reviews code statically before it runs |
| **Breakpoints** | ✅ Set breakpoints, watch variables | ❌ Not applicable |
| **Memory inspection** | ✅ View heap, stack, registers | ❌ Not applicable |
| **Code suggestions** | ❌ None | ✅ Real-time as you type |
| **Code review** | ❌ None | ✅ Automated PR review |
| **Pattern detection** | ❌ None | ✅ Detects anti-patterns, code smells |
| **Learning** | ❌ None | ✅ Explains code, teaches better patterns |
| **Build error help** | Limited error messages | ✅ Explains errors, suggests fixes |
| **Cost of fixing bugs** | High (bug already in code) | Low (caught before merge) |

> [!TIP]
> **They are complementary, not competing.** Think of Copilot as a "pre-debugger" — it catches issues before code is even compiled. The VS debugger remains essential for runtime issues, crash analysis, and performance profiling.

---

## 7. Cost Analysis — GitHub Enterprise + Copilot for 50–75 Developers

### 7.1 Pricing Breakdown (per user/month, billed annually)

| Component | Per User/Month | 50 Users/Month | 75 Users/Month |
|-----------|---------------|----------------|----------------|
| **GitHub Enterprise Cloud** | $21 | $1,050 | $1,575 |
| **GitHub Copilot Business** | $19 | $950 | $1,425 |
| **GitHub Copilot Enterprise** | $39 | $1,950 | $2,925 |

### 7.2 Annual Cost Estimates

#### Option A: GitHub Enterprise + Copilot Business (Recommended to Start)

| Component | 50 Developers | 75 Developers |
|-----------|--------------|--------------|
| GitHub Enterprise Cloud | $12,600/yr | $18,900/yr |
| Copilot Business | $11,400/yr | $17,100/yr |
| **Total** | **$24,000/yr** | **$36,000/yr** |
| **Per developer/year** | **$480/yr** | **$480/yr** |

#### Option B: GitHub Enterprise + Copilot Enterprise (Full Features)

| Component | 50 Developers | 75 Developers |
|-----------|--------------|--------------|
| GitHub Enterprise Cloud | $12,600/yr | $18,900/yr |
| Copilot Enterprise | $23,400/yr | $35,100/yr |
| **Total** | **$36,000/yr** | **$54,000/yr** |
| **Per developer/year** | **$720/yr** | **$720/yr** |

### 7.3 What's Included

| Feature | Enterprise Cloud ($21/user) | Copilot Business ($19/user) | Copilot Enterprise ($39/user) |
|---------|---------------------------|----------------------------|------------------------------|
| Unlimited private repos | ✅ | — | — |
| 50,000 Actions minutes/mo | ✅ | — | — |
| 50 GB Packages storage | ✅ | — | — |
| SAML SSO | ✅ | — | — |
| Audit log / SIEM | ✅ | — | — |
| Branch protection | ✅ | — | — |
| Code completions (unlimited) | — | ✅ | ✅ |
| Copilot Chat in IDE | — | ✅ | ✅ |
| PR code review | — | ✅ | ✅ |
| IP indemnity | — | ✅ | ✅ |
| Admin controls | — | ✅ | ✅ |
| Codebase indexing | — | ❌ | ✅ |
| Fine-tuned models | — | ❌ | ✅ |
| Higher AI credit allotment | — | ❌ | ✅ |

### 7.4 Volume Discount Opportunity

> [!TIP]
> For organizations with 50+ seats, GitHub typically offers **20–35% discounts** through:
> - Multi-year contracts (2–3 years)
> - Bundling with Microsoft Enterprise Agreement (EA)
> - Contact GitHub Sales for a custom quote
>
> **Estimated discounted annual cost (Option A, 75 users): ~$25,000–$29,000/yr**

### 7.5 ROI Justification

| Metric | Without Copilot | With Copilot | Savings |
|--------|----------------|-------------|---------|
| Avg. time per code review | 45 min | 25 min | 44% faster |
| Bugs caught before merge | ~40% | ~65% | 62% improvement |
| Developer onboarding time | 3–4 weeks | 1–2 weeks | 50% faster |
| Time writing boilerplate | ~20% of dev time | ~8% of dev time | 60% reduction |
| Post-release bug fixes | Baseline | ~30% fewer | Cost avoidance |

*Source: GitHub's published research and industry benchmarks. Actual results vary by team.*

---

## 8. GitHub Copilot vs Cursor AI — Comparison & Why Copilot Wins for DEP

### 8.1 What Is Cursor AI?

Cursor is a standalone AI-native code editor built as a **fork of VS Code** (not Visual Studio). It offers powerful AI features — multi-file editing, autonomous agents ("Composer"), and codebase-wide understanding. Some developers consider it the most capable AI coding tool available.

**However, for DEP's specific situation, Cursor has critical limitations.**

### 8.2 The Dealbreaker: Cursor Does NOT Support Visual Studio IDE

> [!CAUTION]
> **Cursor cannot be installed in or integrated with Visual Studio 2022 (or 2017).** It is a completely separate editor. This is the single most important factor for DEP.

| Question | Answer |
|----------|--------|
| Can Cursor run inside Visual Studio 2022? | ❌ **No** — it is a standalone app |
| Can Cursor use the MSVC debugger (`cppvsdbg`)? | ❌ **No** — it uses VS Code's debugger |
| Can Cursor open `.sln` / `.vcxproj` files natively? | ❌ **No** — limited support via extensions |
| Can Cursor use Visual Studio's MSBuild integration? | ❌ **No** — requires manual configuration |
| Is Cursor a replacement for Visual Studio? | ❌ **No** — it replaces VS Code, not Visual Studio |

Developers who use Cursor for C++ typically run a "hybrid workflow":
- **Cursor** open in one window for AI-assisted editing
- **Visual Studio** open in another window for building, debugging, profiling

This adds complexity and friction — especially for a 50–75 developer team that has been using Visual Studio for 20+ years.

### 8.3 Full Feature Comparison

| Feature | GitHub Copilot | Cursor AI | Winner for DEP |
|---------|---------------|-----------|----------------|
| **Visual Studio 2022 support** | ✅ Native integration | ❌ Not supported | 🏆 Copilot |
| **Visual Studio 2017 support** | ❌ Not supported | ❌ Not supported | Tie (both need VS 2022) |
| **MSVC debugger** | ✅ Full access (runs inside VS) | ❌ Cannot use `cppvsdbg` | 🏆 Copilot |
| **MSBuild / .sln support** | ✅ Native in VS | ⚠️ Limited via extensions | 🏆 Copilot |
| **Code completions** | ✅ Unlimited (no credits) | ✅ Unlimited (no credits) | Tie |
| **Chat / Q&A** | ✅ Copilot Chat | ✅ Chat (multi-model) | Tie |
| **Multi-file refactoring** | ⚠️ Growing capability | ✅ Industry-leading (Composer) | Cursor |
| **Agentic coding** | ✅ Copilot Agents | ✅ Agent Mode | Cursor (slightly) |
| **PR code review** | ✅ Built into GitHub PRs | ✅ Bugbot (within Cursor) | 🏆 Copilot (integrated with GitHub) |
| **C++ modernization** | ✅ `@Modernize` agent | ⚠️ General refactoring | 🏆 Copilot |
| **Model choice** | GPT-4o, Claude (fixed) | GPT-4o, Claude, Gemini (switchable) | Cursor |
| **IP indemnity** | ✅ Legal protection for AI code | ❌ Not offered | 🏆 Copilot |
| **Enterprise SSO/SAML** | ✅ Full support | ✅ SAML/OIDC | Tie |
| **Audit logs** | ✅ Full audit trail | ✅ Enterprise only | Tie |
| **SCIM provisioning** | ✅ Supported | ✅ Enterprise only | Tie |
| **GitHub ecosystem integration** | ✅ Native (Issues, PRs, Actions) | ⚠️ Git support only | 🏆 Copilot |
| **Admin spending controls** | ✅ Budget caps, pooled credits | ✅ Usage controls | Tie |
| **Privacy mode** | ✅ Code not used for training | ✅ Code not used for training | Tie |
| **Maturity / stability** | ✅ Backed by Microsoft | ⚠️ Fast-moving startup | 🏆 Copilot |

**Scorecard: Copilot wins 8 categories, Cursor wins 2, Tie on 7.**

### 8.4 Cost Comparison: Copilot vs Cursor

#### Per-User Monthly Cost

| Plan | GitHub Copilot | Cursor AI |
|------|---------------|----------|
| **Team / Business** | $19/user/mo | $40/user/mo |
| **Enterprise** | $39/user/mo | Custom (estimated $50–60+/user/mo) |

> [!NOTE]
> Cursor is **2x the cost** of Copilot Business for equivalent team features.

#### Annual Cost Comparison (50 Developers)

| Component | GitHub (Copilot Business) | Cursor (Teams) |
|-----------|--------------------------|----------------|
| Version control platform | $12,600 (GitHub Enterprise) | $12,600 (GitHub Enterprise)* |
| AI assistant | $11,400 (Copilot Business) | $24,000 (Cursor Teams) |
| **Annual Total** | **$24,000** | **$36,600** |
| **Difference** | — | **+$12,600/yr more** |

*\* Even with Cursor, you still need GitHub (or similar) for version control — Cursor is just an editor, not a platform.*

#### Annual Cost Comparison (75 Developers)

| Component | GitHub (Copilot Business) | Cursor (Teams) |
|-----------|--------------------------|----------------|
| Version control platform | $18,900 (GitHub Enterprise) | $18,900 (GitHub Enterprise)* |
| AI assistant | $17,100 (Copilot Business) | $36,000 (Cursor Teams) |
| **Annual Total** | **$36,000** | **$54,900** |
| **Difference** | — | **+$18,900/yr more** |

### 8.5 The "Hybrid" Argument — Why It Doesn't Work for DEP

Some teams argue: "Use both! GitHub + Copilot for PR reviews, and Cursor for editing."

| Factor | Why This Is Problematic for DEP |
|--------|--------------------------------|
| **Double cost** | Paying for both Copilot ($19) + Cursor ($40) = $59/user/mo |
| **Double training** | Team must learn two AI tools simultaneously |
| **Workflow confusion** | Which tool for which task? Inconsistent across team |
| **Context switching** | Jumping between VS + Cursor + GitHub = friction |
| **Support burden** | IT supports two AI platforms instead of one |
| **For 75 devs** | Extra $36,000/yr for Cursor on top of Copilot |

### 8.6 Recommendation: Copilot for DEP

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   DEP's Stack:   Visual Studio 2022 + C++ + MSBuild + Windows      │
│                                                                     │
│   Copilot:  ✅ Works inside Visual Studio                           │
│             ✅ Uses VS debugger, MSBuild, IntelliSense              │
│             ✅ Reviews PRs on GitHub (where code lives)             │
│             ✅ Half the cost of Cursor                              │
│             ✅ One tool, one login, one workflow                    │
│                                                                     │
│   Cursor:   ❌ Cannot run inside Visual Studio                     │
│             ❌ Requires switching to a separate editor              │
│             ❌ 2x the cost + still need GitHub anyway              │
│             ❌ More complexity for 50-75 developers                 │
│                                                                     │
│   Verdict:  GitHub + Copilot is the clear winner for DEP.          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Cursor is a great tool — but it's designed for VS Code users, not Visual Studio users.** Since DEP's entire workflow is built around Visual Studio C++ (MSBuild, `.sln` projects, MSVC debugger), Copilot is the only AI assistant that integrates directly into that environment without requiring a tool change.

> 📐 **Interactive Diagram:** Open [04-copilot-vs-cursor.excalidraw](diagrams/04-copilot-vs-cursor.excalidraw) in Excalidraw for the full visual comparison.

---

## 9. Detailed Copilot Usage Cost — Daily / Monthly / Yearly for 50–75 Developers

### 9.1 How Copilot Billing Works (2026 Model)

As of June 2026, Copilot uses a **subscription + AI credits** model:

| Component | How It's Billed |
|-----------|----------------|
| **Seat license** | Flat monthly fee per user ($19 Business / $39 Enterprise) |
| **Code completions** | ✅ **Unlimited** — no credits consumed |
| **Next Edit suggestions** | ✅ **Unlimited** — no credits consumed |
| **Copilot Chat** | Consumes AI credits from pool |
| **PR code review** | Consumes AI credits from pool |
| **Agentic workflows** | Consumes AI credits from pool |
| **Copilot CLI** | Consumes AI credits from pool |

### 9.2 AI Credits Included

| Plan | Credits/User/Month | Credit Value | $ Value/User/Month |
|------|-------------------|--------------|--------------------|
| **Copilot Business** | 1,900 credits | 1 credit = $0.01 | $19.00 |
| **Copilot Enterprise** | 3,900 credits | 1 credit = $0.01 | $39.00 |

**Credits are pooled** across the organization — if some developers use fewer credits, others can use more.

| Team Size | Copilot Business Pool | Copilot Enterprise Pool |
|-----------|----------------------|------------------------|
| 50 developers | 95,000 credits/month | 195,000 credits/month |
| 75 developers | 142,500 credits/month | 292,500 credits/month |

### 9.3 Typical Credit Consumption by Activity

| Activity | Approx. Credits | Frequency per Developer |
|----------|----------------|------------------------|
| Simple chat question | 1–5 credits | 10–20x per day |
| Complex code explanation | 5–15 credits | 3–5x per day |
| Inline code fix suggestion | 2–8 credits | 5–10x per day |
| PR code review (small PR) | 10–30 credits | 1–2x per day |
| PR code review (large PR) | 30–100 credits | 1–2x per week |
| Agentic multi-file refactor | 50–200 credits | 1–3x per week |
| Code completions (typing) | **0 credits** | Unlimited |

### 9.4 Usage Scenarios — Daily / Monthly / Yearly Breakdown

#### Scenario A: Light Usage (Most Developers — ~60% of team)

Developers who mainly use code completions + occasional chat.

| Period | Per Developer | 50 Devs (30 light) | 75 Devs (45 light) |
|--------|--------------|--------------------|--------------------|  
| **Per Day** | ~30 credits ($0.30) | 900 credits ($9) | 1,350 credits ($13.50) |
| **Per Month** | ~660 credits ($6.60) | 19,800 credits ($198) | 29,700 credits ($297) |
| **Per Year** | ~7,920 credits ($79.20) | 237,600 credits ($2,376) | 356,400 credits ($3,564) |

#### Scenario B: Moderate Usage (Active Developers — ~30% of team)

Developers who use chat frequently + PR reviews + occasional agents.

| Period | Per Developer | 50 Devs (15 moderate) | 75 Devs (23 moderate) |
|--------|--------------|----------------------|----------------------|
| **Per Day** | ~80 credits ($0.80) | 1,200 credits ($12) | 1,840 credits ($18.40) |
| **Per Month** | ~1,760 credits ($17.60) | 26,400 credits ($264) | 40,480 credits ($404.80) |
| **Per Year** | ~21,120 credits ($211.20) | 316,800 credits ($3,168) | 485,760 credits ($4,857.60) |

#### Scenario C: Power Usage (Senior Devs / Tech Leads — ~10% of team)

Developers who heavily use agents, review large PRs, do complex refactoring.

| Period | Per Developer | 50 Devs (5 power) | 75 Devs (7 power) |
|--------|--------------|-------------------|-------------------|
| **Per Day** | ~200 credits ($2.00) | 1,000 credits ($10) | 1,400 credits ($14) |
| **Per Month** | ~4,400 credits ($44.00) | 22,000 credits ($220) | 30,800 credits ($308) |
| **Per Year** | ~52,800 credits ($528.00) | 264,000 credits ($2,640) | 369,600 credits ($3,696) |

### 9.5 Total Organization Credit Consumption Estimate

#### For 50 Developers (Mixed Usage)

| Usage Tier | Developers | Credits/Month | Credits/Year |
|-----------|-----------|--------------|-------------|
| Light (60%) | 30 | 19,800 | 237,600 |
| Moderate (30%) | 15 | 26,400 | 316,800 |
| Power (10%) | 5 | 22,000 | 264,000 |
| **Total consumed** | **50** | **68,200** | **818,400** |
| **Pool included (Business)** | — | **95,000** | **1,140,000** |
| **Overage** | — | **0 (26,800 surplus)** | **0** |

✅ **50 developers on Copilot Business will stay within included credits.**

#### For 75 Developers (Mixed Usage)

| Usage Tier | Developers | Credits/Month | Credits/Year |
|-----------|-----------|--------------|-------------|
| Light (60%) | 45 | 29,700 | 356,400 |
| Moderate (30%) | 23 | 40,480 | 485,760 |
| Power (10%) | 7 | 30,800 | 369,600 |
| **Total consumed** | **75** | **100,980** | **1,211,760** |
| **Pool included (Business)** | — | **142,500** | **1,710,000** |
| **Overage** | — | **0 (41,520 surplus)** | **0** |

✅ **75 developers on Copilot Business will also stay within included credits.**

### 9.6 Complete Cost of Ownership — Daily / Monthly / Yearly

#### Copilot Business Plan ($19/user/month)

| Cost Item | 50 Developers | 75 Developers |
|-----------|--------------|---------------|
| **Per Day** | | |
| Seat cost | $31.50/day | $47.25/day |
| AI credit overage | $0 (within pool) | $0 (within pool) |
| **Total per day** | **$31.50** | **$47.25** |
| | | |
| **Per Month** | | |
| Seat cost | $950/month | $1,425/month |
| AI credit overage | $0 (within pool) | $0 (within pool) |
| **Total per month** | **$950** | **$1,425** |
| | | |
| **Per Year** | | |
| Seat cost | $11,400/year | $17,100/year |
| AI credit overage | $0 (within pool) | $0 (within pool) |
| **Total per year** | **$11,400** | **$17,100** |

#### Total Cost Including GitHub Enterprise Cloud

| Cost Item | 50 Developers | 75 Developers |
|-----------|--------------|---------------|
| **Per Day** | | |
| GitHub Enterprise seat | $34.50/day | $51.75/day |
| Copilot Business seat | $31.50/day | $47.25/day |
| **Total per day** | **$66.00** | **$99.00** |
| **Per developer per day** | **$1.32** | **$1.32** |
| | | |
| **Per Month** | | |
| GitHub Enterprise seat | $1,050/month | $1,575/month |
| Copilot Business seat | $950/month | $1,425/month |
| **Total per month** | **$2,000** | **$3,000** |
| **Per developer per month** | **$40.00** | **$40.00** |
| | | |
| **Per Year** | | |
| GitHub Enterprise seat | $12,600/year | $18,900/year |
| Copilot Business seat | $11,400/year | $17,100/year |
| **Total per year** | **$24,000** | **$36,000** |
| **Per developer per year** | **$480** | **$480** |

### 9.7 Side-by-Side: Copilot vs Cursor Total Cost

| Period | GitHub + Copilot (50 devs) | GitHub + Cursor (50 devs) | Extra Cost with Cursor |
|--------|--------------------------|--------------------------|------------------------|
| **Per Day** | $66.00 | $100.50 | +$34.50/day |
| **Per Month** | $2,000 | $3,050 | +$1,050/month |
| **Per Year** | $24,000 | $36,600 | +$12,600/year |

| Period | GitHub + Copilot (75 devs) | GitHub + Cursor (75 devs) | Extra Cost with Cursor |
|--------|--------------------------|--------------------------|------------------------|
| **Per Day** | $99.00 | $151.25 | +$52.25/day |
| **Per Month** | $3,000 | $4,575 | +$1,575/month |
| **Per Year** | $36,000 | $54,900 | +$18,900/year |

> [!WARNING]
> **Cursor costs 50–53% more than Copilot** while providing **no Visual Studio IDE integration**. Over 3 years with 75 developers, that's an additional **$56,700** for a tool that can't even run inside your primary IDE.

### 9.8 What If Usage Is Higher Than Expected?

If your team exceeds the included credit pool, overage is billed at **$0.01 per credit**.

| Overage Scenario | Extra Credits/Month | Extra Cost/Month | Extra Cost/Year |
|-----------------|--------------------|-----------------|-----------------|
| 10% over pool (50 devs) | 9,500 credits | $95 | $1,140 |
| 25% over pool (50 devs) | 23,750 credits | $237.50 | $2,850 |
| 10% over pool (75 devs) | 14,250 credits | $142.50 | $1,710 |
| 25% over pool (75 devs) | 35,625 credits | $356.25 | $4,275 |

> [!TIP]
> Even at 25% overage for 75 developers, the additional cost is only ~$4,275/year — still far cheaper than switching to Cursor. GitHub also provides **admin budget controls** to cap spending and prevent surprises.

### 9.9 Available AI Models in Copilot for Visual Studio C++

GitHub Copilot gives developers access to **multiple AI models** directly in the Visual Studio 2022 IDE. Developers can switch models via the **Copilot Chat model picker**.

#### Models Available (as of July 2026)

| Provider | Model | Strengths | Best For | Cost Tier |
|----------|-------|-----------|----------|-----------|
| **OpenAI** | GPT-5 mini | Fast, cheap, good for simple tasks | Quick chat, boilerplate, docs | 💚 Low |
| **OpenAI** | GPT-5.4 | Balanced speed and intelligence | General coding, reviews | 🟡 Medium |
| **OpenAI** | GPT-5.5 | Most capable OpenAI model | Complex refactoring, architecture | 🔴 High |
| **OpenAI** | o3-mini | Reasoning-optimized | Logic-heavy problems, algorithms | 🟡 Medium |
| **Anthropic** | Claude Sonnet 4.6 | Excellent code quality | C++ code generation, reviews | 🟡 Medium |
| **Anthropic** | Claude Opus 4.7 | Most capable Claude model | Deep analysis, large refactors | 🔴 High |
| **Google** | Gemini 2.0 Flash | Fastest, very large context | Quick lookups, large file analysis | 💚 Low |
| **Google** | Gemini 2.5 Pro | Strong reasoning + large context | Complex C++ with many headers | 🟡 Medium |

#### Token Pricing Per Model (per 1 Million Tokens)

| Model | Input Cost | Cached Input | Output Cost | Relative Cost |
|-------|-----------|-------------|-------------|---------------|
| **GPT-5 mini** | $0.25 | $0.025 | $2.00 | 1x (cheapest) |
| **GPT-5.4** | $2.50 | $0.25 | $15.00 | 10x |
| **GPT-5.5** | $5.00 | $0.50 | $30.00 | 20x |
| **Claude Sonnet 4.6** | $3.00 | $0.30 | $15.00 | 12x |
| **Claude Opus 4.7** | $5.00 | $0.50 | $25.00 | 20x |
| **Gemini 2.0 Flash** | $1.50 | — | $9.00 | 6x |
| **Gemini 2.5 Pro** | $2.50 | — | $15.00 | 10x |

> [!IMPORTANT]
> **Model choice directly impacts cost.** A developer using Claude Opus for every chat question will burn through credits **20x faster** than one using GPT-5 mini. Model selection is the biggest controllable cost factor.

#### What Each Model Can and Cannot Do for C++

| Capability | GPT-5 mini | GPT-5.4/5.5 | Claude Sonnet/Opus | Gemini Flash/Pro |
|-----------|-----------|-------------|-------------------|-----------------|
| Code completions | ✅ Unlimited (free) | ✅ Unlimited (free) | ✅ Unlimited (free) | ✅ Unlimited (free) |
| Simple chat ("explain this function") | ✅ Good | ✅ Excellent | ✅ Excellent | ✅ Good |
| Complex refactoring | ⚠️ Struggles | ✅ Good | ✅ Excellent | ✅ Good |
| Multi-file understanding | ⚠️ Limited context | ✅ Good | ✅ Excellent | ✅ Best (large context) |
| Template metaprogramming | ❌ Poor | ⚠️ Partial | ✅ Good | ⚠️ Partial |
| CAE domain understanding | ❌ None | ⚠️ Basic | ⚠️ Basic | ⚠️ Basic |
| Build error diagnosis | ✅ Good | ✅ Excellent | ✅ Excellent | ✅ Good |
| Agentic multi-step tasks | ❌ Too weak | ✅ Good | ✅ Best | ✅ Good |

### 9.10 Model Limitations Developers Must Know

> [!WARNING]
> **No AI model understands CAE physics, FEA algorithms, or Morpher's domain-specific logic.** AI is a coding assistant, not an engineering assistant. The models help with C++ syntax, patterns, and general software engineering — not with finite element math.

| Limitation | Impact on DEP | Mitigation |
|-----------|--------------|-----------|
| **Context window limits** | C++ headers create deep include chains — model may lose context | Use Gemini (largest context) for header-heavy tasks |
| **Hallucinated APIs** | Model may suggest Win32/STL functions that don't exist | Always verify suggestions against MSDN docs |
| **No runtime awareness** | Cannot predict segfaults, memory leaks at runtime | Use AddressSanitizer + VS debugger |
| **Template confusion** | Heavy template metaprogramming may produce incorrect code | Human review required for TMP code |
| **Build system ignorance** | May suggest CMake syntax for MSBuild projects (or vice versa) | Specify build system in copilot-instructions.md |
| **Expensive "thinking" loops** | Agentic mode re-sends entire codebase context repeatedly | Set per-user credit limits |
| **Model deprecation** | Models are periodically retired (e.g., GPT-4.1 deprecated June 2026) | Don't build workflows dependent on a specific model |

### 9.11 Heavy Usage Scenario — "Sole Dependency on Copilot"

**Question: If every developer relies on Copilot heavily for all active code development, how much will costs increase?**

#### What "Sole Dependency" Looks Like

| Activity | Without Copilot | Solely Dependent on Copilot |
|----------|----------------|----------------------------|
| Writing new code | Manual typing | Copilot completions (FREE) + Chat for guidance (credits) |
| Understanding existing code | Read source manually | Ask Copilot to explain (credits) |
| Debugging | VS debugger only | VS debugger + ask Copilot to diagnose (credits) |
| Code review | Human only | Copilot review + human (credits) |
| Refactoring | Manual | Copilot Agent mode (HEAVY credits) |
| Writing tests | Manual | Copilot generates tests (credits) |
| Documentation | Manual | Copilot generates docs (credits) |

#### Credit Consumption: Normal vs Heavy vs Sole Dependency

| Usage Level | Chat/Day | Agents/Day | Reviews/Day | Credits/Dev/Day | Credits/Dev/Month |
|------------|---------|-----------|------------|----------------|------------------|
| **Light** (completions + occasional chat) | 5–10 | 0 | 0 | ~30 | ~660 |
| **Moderate** (regular chat + some agents) | 15–25 | 1–2 | 1–2 | ~80 | ~1,760 |
| **Heavy** (constant chat + agents) | 30–50 | 3–5 | 2–3 | ~200 | ~4,400 |
| **Sole Dependency** (everything via Copilot) | 50–80 | 5–10 | 3–5 | ~400–600 | ~8,800–13,200 |

#### The Critical Difference: Which Model They Use

The same "heavy" developer costs vastly different amounts depending on model choice:

| Developer Profile | Model Used | Credits/Day | Credits/Month | Cost/Month |
|------------------|-----------|------------|--------------|-----------|
| Heavy user, smart model choice | GPT-5 mini + Sonnet for complex | ~150 | ~3,300 | $33 |
| Heavy user, default model | GPT-5.4 | ~300 | ~6,600 | $66 |
| Heavy user, frontier model | Claude Opus for everything | ~600 | ~13,200 | $132 |
| **Sole dependency, frontier** | Opus + heavy agent mode | ~1,000+ | ~22,000+ | $220+ |

### 9.12 The $50K Question — Will Costs Exceed $50,000/Year?

#### Scenario Analysis: 50 Developers

| Scenario | Copilot Credits/Month | Overage/Month | Total/Month | Total/Year | Over $50K? |
|----------|----------------------|--------------|------------|-----------|-----------|
| **A: Recommended (mixed usage)** | 68,200 (pool: 95,000) | $0 | $2,000 | **$24,000** | ❌ No |
| **B: Everyone moderate** | 88,000 (pool: 95,000) | $0 | $2,000 | **$24,000** | ❌ No |
| **C: Everyone heavy** | 220,000 (pool: 95,000) | $1,250 | $3,250 | **$39,000** | ❌ No |
| **D: Everyone sole-dependent (frontier models)** | 500,000+ (pool: 95,000) | $4,050 | $5,000 | **$60,000** | ⚠️ **YES** |

#### Scenario Analysis: 75 Developers

| Scenario | Copilot Credits/Month | Overage/Month | Total/Month | Total/Year | Over $50K? |
|----------|----------------------|--------------|------------|-----------|-----------|
| **A: Recommended (mixed usage)** | 100,980 (pool: 142,500) | $0 | $3,000 | **$36,000** | ❌ No |
| **B: Everyone moderate** | 132,000 (pool: 142,500) | $0 | $3,000 | **$36,000** | ❌ No |
| **C: Everyone heavy** | 330,000 (pool: 142,500) | $1,875 | $4,875 | **$58,500** | ⚠️ **YES** |
| **D: Everyone sole-dependent (frontier models)** | 750,000+ (pool: 142,500) | $6,075 | $9,075 | **$108,900** | ⚠️ **YES** |

#### Answer Summary

```
┌─────────────────────────────────────────────────────────────────────┐
│          Does Copilot cost exceed $50,000/year?                     │
│          (GitHub Enterprise + Copilot Business combined)            │
│                                                                     │
│  50 developers:                                                     │
│  ├── Normal/moderate usage:  $24,000/yr     ✅ Well under $50K     │
│  ├── Heavy usage:            $39,000/yr     ✅ Under $50K          │
│  └── Sole dependency:        $60,000/yr     ⚠️ Exceeds $50K       │
│                                                                     │
│  75 developers:                                                     │
│  ├── Normal/moderate usage:  $36,000/yr     ✅ Under $50K          │
│  ├── Heavy usage:            $58,500/yr     ⚠️ Exceeds $50K       │
│  └── Sole dependency:        $108,900/yr    ⚠️ Exceeds $50K       │
│                                                                     │
│  KEY INSIGHT: Cost only exceeds $50K when developers:               │
│  1. Use expensive models (Opus/GPT-5.5) for EVERY task             │
│  2. Run agent mode extensively (5-10 sessions/day)                  │
│  3. Admin does NOT set spending limits                              │
│                                                                     │
│  SOLUTION: Set per-user credit limits + model policies = stays     │
│            under $50K even with 75 developers.                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 9.13 Admin Controls to Prevent Cost Overruns

GitHub provides **hard spending controls** to guarantee costs stay within budget:

#### Control 1: Per-User Budget Limit (ULB)

Set a maximum credit allowance per developer per month. Once reached, metered features **stop working** (completions still work — they're free).

| Setting | Recommended Value | Effect |
|---------|------------------|--------|
| **Universal per-user limit** | 2,500 credits ($25/mo) | Prevents any single developer from exceeding ~$25/mo |
| **Power user override** | 5,000 credits ($50/mo) | For tech leads who need more agent time |
| **Strict limit** | 1,900 credits ($19/mo) | Stay exactly within included pool — zero overage |

#### Control 2: Enterprise Spending Limit

| Setting | Recommended | Effect |
|---------|------------|--------|
| Hard cap at $0 overage | ✅ Start here | Once pool exhausted, AI features stop. Completions continue. |
| Cap at $500/month overage | Alternative | Allows some flexibility for peak months |

#### Control 3: Model Policy

Admins can **restrict which models** are available to the organization:

| Policy | Setting | Cost Impact |
|--------|---------|------------|
| Allow only GPT-5 mini + Sonnet | Block Opus, GPT-5.5 | Reduces max cost per query by 20x |
| Allow all models, monitor usage | Dashboard alerts | Flexible but requires oversight |
| Default to cheapest model | Set GPT-5 mini as default | Developers must actively switch to expensive models |

#### Recommended Configuration for DEP

```
Enterprise Settings → Billing → GitHub Copilot:

1. ☑ Set spending limit: $0 (no overage beyond included credits)
2. ☑ Set universal per-user limit: 2,500 credits/month
3. ☑ Override for 5-8 power users: 5,000 credits/month
4. ☑ Enable usage dashboard alerts at 80% consumption
5. ☑ Review monthly — adjust limits based on actual usage
```

**With these controls active, the guaranteed maximum annual cost is:**

| Team Size | GitHub Enterprise | Copilot Business | Max Overage | **Guaranteed Max** |
|-----------|-----------------|-----------------|------------|-------------------|
| 50 devs | $12,600 | $11,400 | $0 (hard cap) | **$24,000/year** |
| 75 devs | $18,900 | $17,100 | $0 (hard cap) | **$36,000/year** |

> [!TIP]
> **With a $0 spending limit, it is IMPOSSIBLE for costs to exceed $50K/year for 75 developers.** The included credit pool is generous enough for normal development. Code completions (the most-used feature) remain unlimited regardless of credit balance.

---

## 10. GitHub Actions Runners — C++ Build Costs

### 10.1 GitHub-Hosted Runner Pricing (Windows)

Since Morpher is a Windows C++ application, you'll primarily use Windows runners:

| Runner Size | Per Minute | 30-min Build | 60-min Build | 90-min Build |
|------------|-----------|-------------|-------------|-------------|
| **Windows 2-core** | $0.010 | $0.30 | $0.60 | $0.90 |
| **Windows 4-core** | $0.022 | $0.66 | $1.32 | $1.98 |
| **Windows 8-core** | $0.042 | $1.26 | $2.52 | $3.78 |
| **Windows 16-core** | $0.082 | $2.46 | $4.92 | $7.38 |
| **Windows 32-core** | $0.162 | $4.86 | $9.72 | $14.58 |

### 10.2 Included Minutes

GitHub Enterprise Cloud includes **50,000 minutes/month** for standard runners.

> [!IMPORTANT]
> **Windows minute multiplier:** Windows runners consume minutes at a **2x** rate. So 50,000 included minutes = **25,000 effective Windows minutes** per month.

### 10.3 Monthly Build Cost Estimate for Morpher

Assuming Morpher takes **60 minutes** to build on a Windows 8-core runner:

| Scenario | Builds/Day | Builds/Month | Minutes/Month | Cost/Month |
|----------|-----------|-------------|--------------|-----------|
| **Light** (main branch only) | 3 | 66 | 3,960 | **Included** (within 25K) |
| **Moderate** (main + PRs) | 10 | 220 | 13,200 | **Included** (within 25K) |
| **Heavy** (CI on every push) | 25 | 550 | 33,000 | ~$336/mo overage |

### 10.4 Self-Hosted Runners (Recommended for Morpher)

For a large C++ application like Morpher with specific build dependencies (proprietary compilers, SDKs, DLLs), **self-hosted runners** are recommended:

| Advantage | Detail |
|-----------|--------|
| **Cost** | Currently free (GitHub platform fee) — you pay only for your own hardware |
| **Speed** | Use your existing build servers — no cloud transfer overhead |
| **Dependencies** | Pre-install all SDKs, compilers, DLLs on the machine |
| **Security** | Code never leaves your network |
| **Caching** | Build caches persist between runs (much faster incremental builds) |

**Setup:**
```yaml
# .github/workflows/build.yml
name: Build Morpher
on: [push, pull_request]
jobs:
  build:
    runs-on: self-hosted           # ← Runs on YOUR Windows machine
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: msbuild Morpher.sln /p:Configuration=Release /p:Platform=x64
      - name: Run Tests
        run: vstest.console.exe bin/Release/MorpherTests.dll
```

### 10.5 Build Time Comparison

| Factor | CVS (Current) | GitHub + Self-Hosted Runner |
|--------|--------------|----------------------------|
| Source checkout | Network copy from CVS server | `git clone` (faster, compressed) |
| Incremental builds | Manual | Automatic with build caching |
| Parallel builds | Manual setup | GitHub Actions matrix builds |
| Build trigger | Manual | Automatic on push/PR |
| Build artifacts | Manual copy | Automatic upload & versioning |
| Build logs | Local only | Stored in GitHub, searchable |
| Build notifications | None | Email, Slack, Teams integration |

---

## 11. Migration Plan — CVS to GitHub

### 11.1 Phase Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  Phase 1          Phase 2          Phase 3          Phase 4          │
│  ASSESS           MIGRATE          VALIDATE         CUTOVER          │
│  (2 weeks)        (3-4 weeks)      (2-3 weeks)      (1 week)        │
│                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐       │
│  │ Audit    │    │ Convert  │    │ Verify   │    │ Go Live  │       │
│  │ CVS repo │───►│ history  │───►│ history  │───►│ Switch   │       │
│  │ Plan     │    │ Clean up │    │ CI/CD    │    │ all devs │       │
│  │ Strategy │    │ LFS setup│    │ Train    │    │ Read-only│       │
│  └──────────┘    └──────────┘    └──────────┘    │ CVS      │       │
│                                                   └──────────┘       │
│                                                                      │
│  Total: 8-10 weeks                                                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

> 📐 **Interactive Diagram:** Open [02-migration-roadmap.excalidraw](diagrams/02-migration-roadmap.excalidraw) in Excalidraw for the full visual roadmap.

### 11.2 Phase 1: Assessment & Planning (Weeks 1–2)

| Task | Details |
|------|---------|
| **Audit CVS repository** | Total size, number of files, branches, tags, binary files |
| **Identify binary files** | DLLs, .lib, .exe, .obj, media files — candidates for Git LFS or exclusion |
| **Map authors** | Create CVS username → Git identity mapping file |
| **Decide repo structure** | Mono-repo vs multi-repo (see Section 9.4) |
| **Select migration tool** | `cvs2git` (recommended) or `cvs-fast-export` |
| **Plan Git LFS** | Define which file types go into LFS |
| **Define branching strategy** | GitFlow, trunk-based, or GitHub Flow |
| **Set up GitHub org** | Create organization, teams, permissions |

### 11.3 Phase 2: Migration Execution (Weeks 3–6)

#### Step-by-Step Migration Process

**Step 1: Create a local CVS mirror**
```bash
# Create a safe copy of the CVS repository (NEVER work on production)
rsync -avz user@cvs-server:/cvsroot/morpher /migration/cvs-mirror/
```

**Step 2: Install migration tools**
```bash
# Install cvs2git (part of cvs2svn package)
pip install cvs2svn

# OR use cvs-fast-export (faster for large repos)
apt-get install cvs-fast-export
```

**Step 3: Create author mapping file**
```
# authors.txt — Map CVS usernames to Git identities
jdoe = John Doe <john.doe@dep.com>
ssmith = Sarah Smith <sarah.smith@dep.com>
rjones = Robert Jones <robert.jones@dep.com>
# ... all CVS users
```

**Step 4: Run the conversion**
```bash
# Using cvs2git with options file
cvs2git --options=cvs2git.options

# This produces:
#   git-blob.dat  — All file contents
#   git-dump.dat  — All commits, branches, tags
```

**Step 5: Import into a fresh Git repository**
```bash
git init morpher
cd morpher
cat ../git-blob.dat ../git-dump.dat | git fast-import
git checkout main
```

**Step 6: Clean up large binaries**
```bash
# Remove accidentally imported binaries from history
java -jar bfg.jar --strip-blobs-bigger-than 10M morpher.git

# Set up Git LFS for binary file types
git lfs install
git lfs track "*.dll" "*.lib" "*.exe" "*.pdb" "*.obj"
git add .gitattributes
git commit -m "Configure Git LFS for binary files"
```

**Step 7: Push to GitHub**
```bash
git remote add origin https://github.com/dep-engineering/morpher.git
git push -u origin --all
git push origin --tags
```

### 11.4 Repository Structure Decision

| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **Single mono-repo** | Simple, matches current CVS structure | Large clone size, slower Git operations | ✅ Start here |
| **Multi-repo** | Smaller repos, independent versioning | Complex dependency management | Consider later |

For Morpher, start with a **single repository** that mirrors the current CVS structure. Optimize later if needed.

### 11.5 Phase 3: Validation & Training (Weeks 7–9)

| Task | Details |
|------|---------|
| **Verify history** | Compare file counts, commit history, branch/tag structure between CVS and Git |
| **Set up CI/CD** | Configure GitHub Actions for building Morpher |
| **Developer training** | Git basics, branching, pull requests (2–3 half-day sessions) |
| **Pilot team** | 5–8 developers work in GitHub for 1–2 weeks alongside CVS |
| **Document workflows** | Create internal wiki for Git workflows specific to DEP |

### 11.6 Phase 4: Cutover (Week 10)

| Task | Details |
|------|---------|
| **Final CVS sync** | Import any commits made during pilot period |
| **Set CVS to read-only** | Prevent further CVS commits |
| **Announce cutover** | All development moves to GitHub |
| **Keep CVS archive** | Maintain read-only CVS for historical reference (6–12 months) |

---

## 12. DLL & Library Migration — Complexities & Solutions

### 12.1 The DLL Challenge

After 20+ years, Morpher likely has:

| Binary Type | Example | Challenge |
|------------|---------|-----------|
| **In-house DLLs** | `MorpherCore.dll`, `FEASolver.dll` | Source code should be in Git, binaries should not |
| **Third-party DLLs** | `Intel MKL`, `CUDA`, `Boost` | Should be managed by package manager, not version control |
| **Legacy DLLs** | Old vendor libraries, no source | Must be preserved but tracked with LFS |
| **Debug symbols** | `.pdb` files | Large — use LFS or build artifacts |
| **Static libraries** | `.lib`, `.a` files | Same treatment as DLLs |
| **Test data** | Large CAE model files | Use LFS or external storage |

### 12.2 Solution Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Binary File Strategy                               │
│                                                                     │
│   Source Code (.cpp, .h, .cmake)                                    │
│   └── Stored in Git (normal tracking)                               │
│                                                                     │
│   In-House DLLs (built from source)                                 │
│   └── Source in Git, DLLs built by CI/CD                            │
│   └── Artifacts stored in GitHub Releases or Artifactory            │
│                                                                     │
│   Third-Party Libraries (Intel MKL, Boost, etc.)                    │
│   └── Managed by vcpkg or Conan package manager                     │
│   └── NOT stored in Git at all                                      │
│                                                                     │
│   Legacy / Vendor DLLs (no source available)                        │
│   └── Tracked via Git LFS                                           │
│   └── .gitattributes: *.dll filter=lfs                              │
│                                                                     │
│   Build Outputs (.exe, .pdb, .obj)                                  │
│   └── NEVER stored in Git                                           │
│   └── Uploaded as GitHub Actions artifacts                          │
│                                                                     │
│   Large Test Data (CAE models, meshes)                              │
│   └── Git LFS or external storage (GCS, S3, NAS)                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 12.3 Git LFS (Large File Storage) Configuration

```bash
# .gitattributes (placed in repo root)
# Track binary files with Git LFS
*.dll filter=lfs diff=lfs merge=lfs -text
*.lib filter=lfs diff=lfs merge=lfs -text
*.exe filter=lfs diff=lfs merge=lfs -text
*.pdb filter=lfs diff=lfs merge=lfs -text
*.obj filter=lfs diff=lfs merge=lfs -text
*.so filter=lfs diff=lfs merge=lfs -text
*.a filter=lfs diff=lfs merge=lfs -text

# Large data files
*.stl filter=lfs diff=lfs merge=lfs -text
*.step filter=lfs diff=lfs merge=lfs -text
*.iges filter=lfs diff=lfs merge=lfs -text
*.nas filter=lfs diff=lfs merge=lfs -text
*.bdf filter=lfs diff=lfs merge=lfs -text
```

### 12.4 Third-Party Dependency Management

**Current state (CVS):** Third-party DLLs are likely checked directly into CVS.

**Recommended state (Git):** Use a C++ package manager.

| Package Manager | Best For | Recommendation |
|----------------|----------|----------------|
| **vcpkg** | Microsoft ecosystem, Visual Studio integration | ✅ **Recommended** — native VS integration |
| **Conan** | Cross-platform, supports custom repos | Alternative — more flexible |
| **NuGet** | .NET-style packages in VS | Partial — limited C++ support |

**Example vcpkg integration:**
```json
// vcpkg.json (in repo root)
{
  "name": "morpher",
  "version": "2026.7.0",
  "dependencies": [
    "boost-filesystem",
    "boost-algorithm",
    "eigen3",
    "vtk",
    "opencascade"
  ]
}
```

### 12.5 Migration Complexity Assessment

| Complexity Factor | Low (1–2 weeks) | Medium (3–4 weeks) | High (5–8 weeks) |
|-------------------|-----------------|--------------------|--------------------|
| **Source code** | < 100K LOC, few branches | 100K–500K LOC, 10–20 branches | 500K+ LOC, 50+ branches |
| **Binary files** | Few DLLs, < 1 GB | 10–50 DLLs, 1–5 GB | 100+ DLLs, > 5 GB |
| **Dependencies** | All open source | Mix of open source + commercial | Proprietary vendor libs |
| **Build system** | Simple MSBuild | Multi-project solution | Custom build scripts |
| **Team size** | < 10 developers | 10–50 developers | 50+ developers |
| **CVS history** | < 5 years | 5–15 years | 20+ years ← **DEP is here** |

> [!WARNING]
> **DEP's migration is on the "High" end** due to 20+ years of history, likely many binary files in CVS, and a large team. Plan for **8–10 weeks** with a dedicated migration engineer.

---

## 13. Build Comparison — CVS vs GitHub

| Build Aspect | CVS (Current) | GitHub Actions (Proposed) |
|-------------|---------------|--------------------------|
| **Trigger** | Manual (developer runs build locally or on build server) | Automatic — triggers on push, PR, schedule, or manual |
| **Reproducibility** | Depends on developer's local machine setup | Defined in YAML — same environment every time |
| **Build caching** | Manual | Automatic — caches NuGet, vcpkg, compiled objects |
| **Parallel builds** | Limited | Matrix builds (e.g., Debug + Release, x86 + x64 simultaneously) |
| **Build artifacts** | Copied manually to shared drive | Automatically versioned and downloadable from GitHub |
| **Build logs** | Local only | Stored in GitHub, searchable, accessible to entire team |
| **Build notifications** | None | Email, Slack, Teams, webhook |
| **Build history** | None | Full history with timing, logs, and artifacts |
| **Multi-platform** | Manual setup per platform | Define matrix: Windows, Linux, macOS |
| **Build time** | Same as GitHub (depends on hardware) | Same hardware = same time. Self-hosted runners use your build servers |

> 📐 **Interactive Diagram:** Open [03-build-pipeline.excalidraw](diagrams/03-build-pipeline.excalidraw) in Excalidraw for the visual CI/CD pipeline flow.

### Example Build Workflow for Morpher

```yaml
# .github/workflows/build-morpher.yml
name: Build Morpher

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: self-hosted       # Uses DEP's Windows build server
    
    strategy:
      matrix:
        configuration: [Debug, Release]
        platform: [x64]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          lfs: true            # Pull LFS files (DLLs)

      - name: Setup MSBuild
        uses: microsoft/setup-msbuild@v2

      - name: Restore NuGet packages
        run: nuget restore Morpher.sln

      - name: Build
        run: |
          msbuild Morpher.sln \
            /p:Configuration=${{ matrix.configuration }} \
            /p:Platform=${{ matrix.platform }} \
            /m                 # Parallel build

      - name: Run Unit Tests
        run: |
          vstest.console.exe \
            bin/${{ matrix.configuration }}/MorpherTests.dll \
            --logger:trx

      - name: Upload Build Artifacts
        if: matrix.configuration == 'Release'
        uses: actions/upload-artifact@v4
        with:
          name: morpher-${{ matrix.platform }}-release
          path: bin/Release/
```

---

## 14. GitHub Peer Review & Governance Setup

One of the biggest advantages of migrating to GitHub is establishing a **formal code review process**. CVS has zero support for peer review. GitHub provides a complete governance framework through configuration files and branch protection rules.

### 14.1 Overview — Key Governance Files

These files live in your repository and define how code flows through review:

| File | Location | Purpose |
|------|----------|--------|
| `.github/copilot-instructions.md` | `.github/` | Custom rules for Copilot AI reviews |
| `.github/CODEOWNERS` | `.github/` | Who must approve changes to which files |
| `.github/pull_request_template.md` | `.github/` | Standardized PR description template |
| `.gitignore` | repo root | Prevent build artifacts from being committed |
| `.gitattributes` | repo root | Git LFS tracking, line endings |
| Branch protection rules | GitHub settings | Enforce review requirements before merge |

### 14.2 Branch Protection Rules

Branch protection rules are the **most critical governance feature** in GitHub. They prevent direct pushes to important branches and enforce code review.

#### Recommended Rules for `main` Branch

| Rule | Setting | Why |
|------|---------|-----|
| **Require pull request before merging** | ✅ Enabled | No direct commits to main — everything goes through PR |
| **Required approvals** | 2 | At least 2 developers must approve |
| **Dismiss stale reviews** | ✅ Enabled | If code changes after approval, re-review required |
| **Require review from CODEOWNERS** | ✅ Enabled | Module owners must approve changes to their code |
| **Require status checks** | ✅ Enabled | Build must pass before merge |
| **Require Copilot review** | ✅ Enabled | AI review runs on every PR |
| **Require branches to be up to date** | ✅ Enabled | PR must be rebased on latest main |
| **Restrict who can push** | Admins only | Only admins can bypass rules |
| **Require signed commits** | Optional | For higher security |
| **Include administrators** | ✅ Enabled | Even admins follow the rules |

#### Recommended Rules for `develop` Branch

| Rule | Setting |
|------|--------|
| Require pull request | ✅ Enabled |
| Required approvals | 1 |
| Require status checks (build) | ✅ Enabled |
| Require Copilot review | ✅ Enabled |

#### How to Set Up (GitHub UI)

```
Repository → Settings → Branches → Branch protection rules → Add rule

Branch name pattern: main
☑ Require a pull request before merging
  ☑ Required number of approvals: 2
  ☑ Dismiss stale pull request approvals when new commits are pushed
  ☑ Require review from Code Owners
☑ Require status checks to pass before merging
  ☑ Require branches to be up to date before merging
  Status checks: "Build Morpher", "Run Tests"
☑ Require conversation resolution before merging
☑ Do not allow bypassing the above settings
```

### 14.3 CODEOWNERS File

The `CODEOWNERS` file defines **who must review changes** to specific parts of the codebase. This is critical for Morpher where different engineers own different modules.

```bash
# .github/CODEOWNERS
# ──────────────────────────────────────────────────────────
# Each line defines: <file pattern>  <owners>
# Owners are @github-username or @org/team-name
# Last matching rule wins
# ──────────────────────────────────────────────────────────

# ── Global defaults ───────────────────────────────────────
# These reviewers are required for ANY file change
*                           @dep-engineering/tech-leads

# ── Core Solver Engine ────────────────────────────────────
# FEA solver, mesh algorithms — requires senior review
/src/solver/                @john.doe @sarah.smith
/src/mesh/                  @john.doe @sarah.smith
/src/optimization/          @john.doe

# ── UI / Frontend ─────────────────────────────────────────
/src/ui/                    @dep-engineering/ui-team
/src/dialogs/               @dep-engineering/ui-team
/resources/                 @dep-engineering/ui-team

# ── I/O & File Formats ───────────────────────────────────
/src/io/                    @robert.jones
/src/importers/             @robert.jones
/src/exporters/             @robert.jones

# ── Build System ──────────────────────────────────────────
CMakeLists.txt              @dep-engineering/build-team
*.vcxproj                   @dep-engineering/build-team
*.sln                       @dep-engineering/build-team
*.props                     @dep-engineering/build-team

# ── CI/CD Pipeline ────────────────────────────────────────
/.github/                   @dep-engineering/devops
/.github/workflows/         @dep-engineering/devops

# ── Documentation ─────────────────────────────────────────
/docs/                      @dep-engineering/tech-leads
README.md                   @dep-engineering/tech-leads
```

**How it works:**
- When a PR modifies files in `/src/solver/`, **@john.doe** and **@sarah.smith** are automatically requested as reviewers
- With branch protection rule "Require review from CODEOWNERS" enabled, the PR **cannot be merged** until they approve
- This ensures domain experts always review changes to their modules

### 14.4 Copilot Instructions File (`.github/copilot-instructions.md`)

This is the **custom rules file** that tells GitHub Copilot how to review your code. It's specific to your repository and coding standards.

```markdown
<!-- .github/copilot-instructions.md -->

# Morpher C++ Code Review Instructions

## Project Context
Morpher is a Computer-Aided Engineering (CAE) desktop application built with
Visual C++. It performs finite element analysis, mesh generation, and design
optimization for automotive and aerospace applications.

## Coding Standards

### Memory Management
- All heap allocations MUST use smart pointers (`std::unique_ptr`,
  `std::shared_ptr`). Raw `new`/`delete` is prohibited except in
  performance-critical solver loops where profiling justifies it.
- Flag any raw pointer allocation that is not wrapped in a smart pointer.
- Check for potential memory leaks in constructors that allocate before
  throwing exceptions.

### Error Handling
- All public API functions must validate input parameters.
- Use exceptions for error handling, not return codes.
- Never catch exceptions silently (empty catch blocks).
- Log all caught exceptions with severity level.

### Threading & Concurrency
- Morpher uses OpenMP for parallel solver loops.
- Flag any shared variable access in parallel regions without proper
  synchronization (`#pragma omp critical`, atomics, or mutexes).
- Never use `std::thread` directly — use the Morpher ThreadPool class.

### Performance
- Flag `std::vector::push_back()` in tight loops without prior `reserve()`.
- Suggest move semantics for large objects returned from functions.
- Check for unnecessary copies in range-based for loops (prefer
  `const auto&` over `auto`).
- Flag virtual function calls inside performance-critical solver loops.

### Naming Conventions
- Classes: PascalCase (e.g., `MeshRefinement`)
- Functions: camelCase (e.g., `computeStiffnessMatrix`)
- Member variables: `m_` prefix (e.g., `m_nodeCount`)
- Constants: ALL_CAPS (e.g., `MAX_ITERATIONS`)
- File names: PascalCase matching class name

### Code Style
- Maximum line length: 120 characters
- Use `#pragma once` instead of include guards
- Include order: project headers, third-party headers, standard library
- All switch statements must have a `default` case
- Braces on new line (Allman style)

### Security
- Never hardcode file paths, credentials, or license keys
- Validate all user input from file importers (STL, STEP, IGES, Nastran)
- Check buffer sizes before string operations
- Use `std::filesystem` for path manipulation, not string concatenation

### Documentation
- All public classes and functions must have Doxygen-style doc comments
- Include @brief, @param, @return, and @throws tags
- Document units for numerical parameters (e.g., "@param force Force
  in Newtons")
```

> [!TIP]
> **This file makes Copilot act like a senior DEP engineer.** Instead of generic suggestions, Copilot will enforce your specific coding standards — checking for Morpher's naming conventions, memory management rules, threading patterns, and performance guidelines in every PR review.

### 14.5 Pull Request Template

A PR template ensures developers provide consistent, useful information with every code change.

```markdown
<!-- .github/pull_request_template.md -->

## Description
<!-- What does this PR do? Why is this change needed? -->


## Type of Change
- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing
      functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] ♻️ Refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] 🧪 Test update

## Modules Affected
<!-- Which Morpher modules does this change touch? -->
- [ ] Solver Engine
- [ ] Mesh Generation
- [ ] UI / Dialogs
- [ ] File I/O (Import/Export)
- [ ] Optimization
- [ ] Build System
- [ ] Other: ___________

## Testing
<!-- How was this tested? -->
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] Regression tests pass
- [ ] Tested with sample CAE models

## Checklist
- [ ] My code follows the Morpher coding standards
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly complex areas
- [ ] I have updated the documentation (if applicable)
- [ ] My changes generate no new compiler warnings
- [ ] New and existing unit tests pass locally
- [ ] I have checked for memory leaks (no raw new/delete)

## Screenshots / Results
<!-- If applicable, add screenshots or test results -->


## Related Issues
<!-- Link any related issues: Fixes #123, Related to #456 -->

```

### 14.6 .gitignore for Visual C++ Projects

Prevent build artifacts, debug files, and IDE settings from polluting the repository.

```gitignore
# .gitignore — Visual C++ / Morpher

# ── Build outputs ─────────────────────────────────
[Dd]ebug/
[Rr]elease/
x64/
x86/
[Bb]in/
[Oo]bj/
[Bb]uild/

# ── Visual Studio files ──────────────────────────
*.suo
*.user
*.userosscache
*.sln.docstates
.vs/
*.ncb
*.aps
*.cachefile
*.ipch
*.opensdf
*.sdf
*.log
*.tlog
*.ilk

# ── Compiled binaries (built, not source) ────────
*.obj
*.o
*.pch
*.pdb
*.idb
*.exp

# ── Build outputs (use GitHub Releases instead) ──
# Note: Source DLLs are tracked via Git LFS
# Only EXCLUDE build-generated DLLs here
[Bb]uild/**/*.dll
[Bb]uild/**/*.exe
[Bb]uild/**/*.lib

# ── OS files ─────────────────────────────────────
Thumbs.db
Desktop.ini
.DS_Store

# ── IDE and tools ────────────────────────────────
*.swp
*.bak
*.tmp
*.orig
~$*
```

### 14.7 Merge Strategy & Workflow

DEP should adopt **GitHub Flow** (simplified) for Morpher:

```
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Flow for Morpher                    │
│                                                                 │
│  main ──────●────────●────────●────────●────── (always stable)  │
│              \      /          \      /                          │
│               \    /            \    /                           │
│    feature/    ●──●     feature/ ●──●                           │
│    mesh-fix              solver-opt                              │
│                                                                 │
│  1. Create branch from main                                     │
│  2. Make changes, commit locally                                │
│  3. Push branch, open Pull Request                              │
│  4. Copilot reviews automatically                               │
│  5. CODEOWNERS review (domain experts)                          │
│  6. CI/CD builds and tests                                      │
│  7. Merge to main (squash merge recommended)                    │
│  8. Branch auto-deleted after merge                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Merge Method Recommendation

| Method | When to Use | Recommended for DEP? |
|--------|------------|---------------------|
| **Squash and merge** | Combines all commits into one clean commit | ✅ **Yes — default** |
| **Merge commit** | Preserves full branch history | For large features |
| **Rebase and merge** | Linear history, no merge commits | For small fixes |

> [!TIP]
> **Squash merge** keeps `main` history clean — each PR becomes one commit with the PR title and number. This makes `git log` readable and `git bisect` effective for finding regressions.

### 14.8 Required Status Checks

Configure these checks to run on every PR. The PR cannot be merged until all pass:

| Status Check | What It Does | Tool |
|-------------|-------------|------|
| **Build Morpher** | Compiles the full solution | GitHub Actions (self-hosted) |
| **Run Unit Tests** | Executes test suite | GitHub Actions |
| **Copilot Review** | AI code review | GitHub Copilot |
| **Code Formatting** | Checks style compliance | clang-format |
| **Static Analysis** | Finds bugs and vulnerabilities | CodeQL or clang-tidy |
| **License Check** | Validates license headers | Custom script |

#### Example Workflow with All Checks

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    branches: [main, develop]

jobs:
  build:
    name: Build Morpher
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true
      - name: Build (Release x64)
        run: msbuild Morpher.sln /p:Configuration=Release /p:Platform=x64 /m

  test:
    name: Run Unit Tests
    needs: build
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - name: Run Tests
        run: vstest.console.exe bin/Release/MorpherTests.dll --logger:trx
      - name: Publish Results
        uses: dorny/test-reporter@v1
        if: always()
        with:
          name: Test Results
          path: '**/*.trx'
          reporter: dotnet-trx

  format-check:
    name: Code Formatting
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - name: Check clang-format
        run: |
          find src/ -name '*.cpp' -o -name '*.h' | 
            xargs clang-format --dry-run --Werror

  static-analysis:
    name: Static Analysis
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v4
      - name: Run clang-tidy
        run: |
          clang-tidy src/**/*.cpp -- -std=c++17 \
            -I src/include -I third_party/include
```

### 14.9 Complete Repository Structure After Setup

Here's what Morpher's GitHub repository should look like after applying all governance files:

```
morpher/
├── .github/
│   ├── copilot-instructions.md    ← AI review rules (Section 14.4)
│   ├── CODEOWNERS                 ← Module ownership (Section 14.3)
│   ├── pull_request_template.md   ← PR template (Section 14.5)
│   └── workflows/
│       ├── build.yml              ← Main build pipeline
│       └── pr-checks.yml          ← PR validation checks
├── .gitignore                     ← Exclude build artifacts (Section 14.6)
├── .gitattributes                 ← Git LFS tracking rules
├── .clang-format                  ← Code formatting rules
├── .clang-tidy                    ← Static analysis config
├── CMakeLists.txt                 ← Build configuration
├── Morpher.sln                    ← Visual Studio solution
├── README.md                      ← Project overview
├── docs/                          ← Documentation
├── src/                           ← Source code
│   ├── solver/                    ← FEA engine
│   ├── mesh/                      ← Mesh algorithms
│   ├── ui/                        ← GUI code
│   ├── io/                        ← File import/export
│   └── include/                   ← Header files
├── tests/                         ← Unit tests
├── third_party/                   ← Git LFS tracked vendor DLLs
└── vcpkg.json                     ← C++ package dependencies
```

### 14.10 Quick Reference — Complete Governance Checklist

| ✅ | Item | File / Setting | Status |
|----|------|---------------|--------|
| ☐ | Branch protection on `main` | GitHub Settings | Set up during Week 6 |
| ☐ | Branch protection on `develop` | GitHub Settings | Set up during Week 6 |
| ☐ | CODEOWNERS file | `.github/CODEOWNERS` | Create during Week 5 |
| ☐ | Copilot instructions | `.github/copilot-instructions.md` | Create during Week 6 |
| ☐ | PR template | `.github/pull_request_template.md` | Create during Week 5 |
| ☐ | .gitignore | Root | Create during Week 3 |
| ☐ | .gitattributes (LFS) | Root | Create during Week 3 |
| ☐ | CI/CD pipeline | `.github/workflows/build.yml` | Create during Week 5 |
| ☐ | PR checks pipeline | `.github/workflows/pr-checks.yml` | Create during Week 6 |
| ☐ | Squash merge default | GitHub Settings | Set during Week 6 |
| ☐ | Auto-delete branches | GitHub Settings | Set during Week 6 |
| ☐ | Copilot enabled for org | GitHub Admin | Set during Week 6 |
| ☐ | Developer training | Workshop | Week 7 |

---

## 15. Risk Assessment & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| **History loss during conversion** | Medium | High | Run test conversions first; verify file counts and commit history |
| **Binary file bloat in Git** | High | Medium | Git LFS from day one; clean up with BFG before import |
| **Build breaks after migration** | Medium | High | Set up CI/CD during pilot phase; maintain CVS read-only as fallback |
| **Developer resistance** | Medium | Medium | Training sessions; designate Git champions per team; start with pilot |
| **DLL dependency confusion** | Medium | Medium | Document all dependencies before migration; set up vcpkg |
| **CVS-specific workflows break** | Low | Medium | Identify and document all CVS hooks/scripts; recreate as GitHub Actions |
| **Licensing/compliance issues** | Low | High | Verify GitHub Enterprise meets security/compliance requirements |
| **Network/performance issues** | Low | Low | Self-hosted runners eliminate network concerns; local Git is fast |

---

## 16. Recommended Roadmap & Timeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                    10-Week Migration Roadmap                         │
├──────┬──────────────────────────────────────────────────────────────┤
│ Wk 1 │ ▓▓▓ Assessment: Audit CVS, identify binaries, plan          │
│ Wk 2 │ ▓▓▓ Setup: Create GitHub org, configure SSO, set up LFS     │
│ Wk 3 │ ▓▓▓ Test Migration: First cvs2git run, verify output        │
│ Wk 4 │ ▓▓▓ Refine: Fix author mapping, clean binaries, retry       │
│ Wk 5 │ ▓▓▓ CI/CD: Set up GitHub Actions, self-hosted runner        │
│ Wk 6 │ ▓▓▓ Copilot: Enable Copilot, configure review settings      │
│ Wk 7 │ ▓▓▓ Training: Git workshops for all developers              │
│ Wk 8 │ ▓▓▓ Pilot: 5-8 devs work in GitHub alongside CVS           │
│ Wk 9 │ ▓▓▓ Validate: Final sync, verify everything works           │
│ Wk10 │ ▓▓▓ Cutover: Set CVS read-only, all devs switch to GitHub   │
├──────┼──────────────────────────────────────────────────────────────┤
│ Post │ 30-day support period: troubleshoot, optimize, train         │
└──────┴──────────────────────────────────────────────────────────────┘
```

---

## 17. Conclusion

### Why Now?

| Factor | Impact |
|--------|--------|
| CVS is 38 years old with zero active development | Risk increases every year |
| AI-powered development tools require Git | Copilot, CodeQL, and all modern tools need GitHub |
| New hires don't know CVS | Onboarding friction increases |
| No code review process | Quality and knowledge sharing suffer |
| No CI/CD pipeline | Manual builds are slow and error-prone |
| Competitors are already using modern tools | Industry has moved on |

### Annual Investment Summary

| Item | 50 Devs | 75 Devs |
|------|---------|---------|
| GitHub Enterprise Cloud | $12,600 | $18,900 |
| GitHub Copilot Business | $11,400 | $17,100 |
| GitHub Actions (self-hosted) | $0 (own hardware) | $0 (own hardware) |
| Migration effort (one-time) | ~$15,000–$25,000 | ~$15,000–$25,000 |
| **Year 1 Total** | **~$39,000–$49,000** | **~$51,000–$61,000** |
| **Year 2+ Annual** | **~$24,000/yr** | **~$36,000/yr** |

### Why Not Cursor?

| Factor | Verdict |
|--------|--------|
| Doesn't run inside Visual Studio | ❌ Dealbreaker for DEP |
| 2x the cost of Copilot Business | ❌ $12,600–$18,900/yr more |
| Still requires GitHub for version control | ❌ Adds cost, not replaces |
| Great AI features | ✅ But same capabilities available in Copilot inside VS |
| **Bottom line** | **Cursor is for VS Code shops, not Visual Studio shops** |

### Final Recommendation

> [!IMPORTANT]
> **Migrate to GitHub Enterprise Cloud with Copilot Business.** Start with a 10-week phased migration, use self-hosted runners for CI/CD, and enable Copilot for all developers. The investment of **$1.32 per developer per day** ($480/developer/year) delivers modern version control, AI-assisted development, automated CI/CD, and positions DEP's engineering team for the next 20 years.
>
> **Skip Cursor AI** — it cannot integrate with Visual Studio and costs 50% more while still requiring GitHub underneath.

---

*Document prepared July 2026. Pricing is based on publicly available GitHub/Microsoft rates and may vary with volume discounts or enterprise agreements. Contact GitHub Sales for a custom quote.*
