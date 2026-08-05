# AI Coding Agents for C++ CAE Development
## Beyond Copilot — Claude Code, Cursor, Windsurf & More

> **Companion to:** [Copilot-CPP-Review-Models-Cost-Guide.md](Copilot-CPP-Review-Models-Cost-Guide.md)  
> **For:** the organization — Engineering & Management Teams  
> **Date:** August 2026  
> **Focus:** Alternative AI coding agents that can integrate with VC++ workflows for complex CAE C++ development

---

## Table of Contents

1. [Why Look Beyond Copilot?](#1-why-look-beyond-copilot)
2. [The Four Major AI Coding Agents](#2-the-four-major-ai-coding-agents)
3. [VC++ Integration — How Each Tool Fits](#3-vc-integration--how-each-tool-fits)
4. [Head-to-Head Comparison for CAE C++](#4-head-to-head-comparison-for-cae-c)
5. [Cost Analysis — 50 Developers](#5-cost-analysis--50-developers)
6. [CAE-Specific C++ Effectiveness](#6-cae-specific-c-effectiveness)
7. [Benefits & Drawbacks Summary](#7-benefits--drawbacks-summary)
8. [Recommendation for the Organization](#8-recommendation-for-the-organization)
9. [Security, Privacy & Data Training — Will They Learn Your Code?](#9-security-privacy--data-training--will-they-learn-your-code)
10. [GitHub Enterprise — Cloud vs Server](#10-github-enterprise--cloud-vs-server)

---

## 1. Why Look Beyond Copilot?

The [Copilot guide](Copilot-CPP-Review-Models-Cost-Guide.md) established that Copilot is effective for code review, completions, and enforcing C++ standards. However, the CAE development landscape has unique challenges that push beyond what Copilot alone offers:

| CAE C++ Challenge | Copilot Limitation |
|---|---|
| Multi-file refactoring across solver/mesh/IO modules | Copilot works file-by-file, limited cross-file awareness |
| Debugging complex build failures (MSBuild, linker errors) | Copilot can't run commands or iterate on build logs |
| Large legacy codebase understanding (20+ years of C++) | Limited context window (~8K-32K tokens depending on model) |
| Template metaprogramming (TMP) heavy code | Moderate effectiveness (as documented in companion guide) |
| Autonomous multi-step tasks (refactor → build → test → fix) | Copilot is reactive, not agentic |

**The question isn't "which is best?" — it's "which combination gives maximum effectiveness for CAE C++ development?"**

---

## 2. The Four Major AI Coding Agents

### Overview

| Tool | Type | How It Works | Primary Strength |
|---|---|---|---|
| **GitHub Copilot** | IDE Extension | Plugs into Visual Studio, VS Code, JetBrains | Fast completions, PR reviews, lowest friction |
| **Cursor** | AI-Native IDE | Standalone editor (VS Code fork) | Multi-file editing, Composer mode |
| **Claude Code** | Terminal Agent | CLI tool, reads/writes/executes in your repo | Deep reasoning, autonomous multi-step tasks |
| **Windsurf (Devin Desktop)** | AI-Native IDE | Standalone editor (VS Code fork) | Autonomous "Cascade" multi-file editing |

### How They Differ Fundamentally

```
COPILOT                           CURSOR
  You type → it suggests             You describe → it edits multiple files
  Works INSIDE your IDE              IS the IDE (replaces VS Code)
  Reactive (you lead)                Collaborative (it leads with you)

CLAUDE CODE                       WINDSURF
  You describe → it executes         You describe → it cascades changes
  Works in your TERMINAL             IS the IDE (replaces VS Code)
  Fully autonomous (agent)           Semi-autonomous (cascade agent)
  Reads, writes, builds, tests       Multi-file coordinated edits
```

---

## 3. VC++ Integration — How Each Tool Fits

> **Critical context:** The application is built in Visual Studio (MSVC 2022) with MSBuild. The team uses Visual Studio as their primary IDE. Any tool must work WITH this workflow, not replace it.

### Integration Matrix

| Tool | Visual Studio Integration | VC++ Build Support | C++ Debugging | Workflow Impact |
|---|---|---|---|---|
| **GitHub Copilot** | ✅ Native extension for VS 2022 | ❌ Can't run builds | ❌ No debug integration | **Zero disruption** — installs as extension |
| **Cursor** | ⚠️ Separate IDE (VS Code fork) | ⚠️ Can run MSBuild via terminal | ⚠️ Basic C++ debug only | **High disruption** — requires switching editors |
| **Claude Code** | ✅ Works alongside VS (terminal) | ✅ Can run MSBuild, read logs | ❌ No debug integration | **Low disruption** — runs in terminal while you use VS |
| **Windsurf** | ⚠️ Separate IDE (VS Code fork) | ⚠️ Can run MSBuild via terminal | ⚠️ Basic C++ debug only | **High disruption** — requires switching editors |

### The VC++ Problem for Cursor & Windsurf

Both Cursor and Windsurf are **VS Code forks**. This means:

- ❌ **No MSVC-specific debug engine** — VS Code's C++ debugger is basic compared to Visual Studio's
- ❌ **No MSBuild project system** — .sln/.vcxproj files open but lack full IntelliSense parity
- ❌ **No Visual Studio-specific extensions** — VsIntelliCode, VS profiler, etc. don't work
- ⚠️ **C++ IntelliSense differs** — VS Code uses clangd-based IntelliSense vs VS's proprietary engine

**For a VC++ shop, Cursor and Windsurf require a "hybrid workflow":**
```
Write/Edit code → Cursor or Windsurf (AI-assisted)
Build/Debug code → Visual Studio (native toolchain)
```

**This is a significant workflow friction** that must be weighed against the AI benefits.

### Claude Code — The Terminal Companion

Claude Code has a unique advantage for VC++ teams:

```
Developer's setup:
  Terminal 1: Claude Code (agentic assistant)
  Window 2:   Visual Studio 2022 (primary IDE)

Claude Code can:
  ✅ Read any file in the repo
  ✅ Run MSBuild from terminal: "msbuild morpher.sln /p:Configuration=Release"
  ✅ Parse build errors and fix them iteratively
  ✅ Run unit tests and analyze failures
  ✅ Search across the entire codebase (grep, find)
  ✅ Make multi-file edits that you review in VS
  
Claude Code cannot:
  ❌ Provide inline completions (use Copilot for that)
  ❌ Show visual diff in VS (you review in VS after)
  ❌ Interact with VS debugger
```

---

## 4. Head-to-Head Comparison for CAE C++

### Capability Comparison

| Capability | Copilot | Cursor | Claude Code | Windsurf |
|---|---|---|---|---|
| **Inline autocomplete** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ N/A | ⭐⭐⭐⭐ |
| **PR code review** | ⭐⭐⭐⭐ | ❌ N/A | ❌ N/A | ❌ N/A |
| **Multi-file refactoring** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Large codebase understanding** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Build error diagnosis** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Template metaprogramming** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Autonomous task execution** | ❌ N/A | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Memory management analysis** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Custom review rules** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **VS 2022 integration** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐ |

### CAE C++ Scenario Testing

| Scenario | Best Tool | Why |
|---|---|---|
| "Fix this stiffness matrix assembly" (single file) | **Copilot** | Inline suggestion, zero context switch |
| "Refactor Element hierarchy across 15 files" | **Claude Code** or **Cursor** | Multi-file awareness + autonomous execution |
| "Debug why MSBuild fails with LNK2019 errors" | **Claude Code** | Can run msbuild, parse output, iterate |
| "Add OpenMP parallelization to solver loop" | **Copilot** | Quick inline suggestion with context |
| "Migrate raw pointers to smart pointers in mesh module" | **Claude Code** | Can scan entire module, make changes, build, verify |
| "Write unit tests for element stiffness functions" | **Cursor** or **Claude Code** | Multi-file test generation |
| "Review PR for memory leaks and thread safety" | **Copilot** | Native GitHub PR review integration |
| "Understand how the legacy I/O parser works" | **Claude Code** | Can read entire module, trace call chains |

---

## 5. Cost Analysis — 50 Developers

### Per-Developer Monthly Cost

| Tool | Plan | Monthly/User | Annual/User | Notes |
|---|---|---|---|---|
| **GitHub Copilot** | Business | $19 | $228 | Unlimited completions. Chat/agent uses AI Credits |
| **GitHub Copilot** | Enterprise | $39 | $468 | + codebase indexing, policy controls |
| **Cursor** | Teams Standard | $40 | $480 | Credit pool for frontier models |
| **Cursor** | Teams Premium | $120 | $1,440 | 5x usage limits |
| **Claude Code** | Pro (individual) | $20 | $240 | Shared with Claude chat. Light usage |
| **Claude Code** | Max 5x | $100 | $1,200 | Heavy agentic coding usage |
| **Claude Code** | Max 20x | $200 | $2,400 | Unlimited-feel for power users |
| **Windsurf** | Pro | $20 | $240 | Daily/weekly quota limits |
| **Windsurf** | Teams | $40 | $480 | Team admin + quotas |

### 50 Developer Annual Cost Scenarios

| Scenario | Tools | Annual Cost | Per Dev/Year |
|---|---|---|---|
| **Copilot Only** (current guide recommendation) | Copilot Business | **$11,400** | $228 |
| **Copilot + Claude Code (light)** | Copilot Biz + Claude Pro (10 devs) | **$13,800** | $276 avg |
| **Copilot + Claude Code (heavy)** | Copilot Biz + Claude Max 5x (10 devs) | **$23,400** | $468 avg |
| **Cursor Only** (all switch) | Cursor Teams Standard | **$24,000** | $480 |
| **Copilot + Cursor** (hybrid) | Copilot Biz + Cursor Teams (15 devs) | **$18,600** | $372 avg |
| **Full Stack** (Copilot + Claude Code for leads) | Copilot Biz + Claude Max (5 leads) | **$17,400** | $348 avg |

### Cost-Effectiveness Ranking

| Rank | Strategy | Cost | Effectiveness for CAE C++ |
|---|---|---|---|
| 🥇 | **Copilot (all) + Claude Code Max (5 senior devs)** | $17,400/yr | Best balance — completions for everyone, deep reasoning for complex tasks |
| 🥈 | **Copilot Business (all)** | $11,400/yr | Most economical, covers 80% of daily needs |
| 🥉 | **Copilot (all) + Cursor Teams (15 devs)** | $18,600/yr | Good if team is willing to switch IDEs for editing |

---

## 6. CAE-Specific C++ Effectiveness

### What Each Tool Handles in CAE Code

| CAE Domain | Copilot | Claude Code | Cursor |
|---|---|---|---|
| **FEA Solver Code** | Catches style/safety issues. Won't verify math. | Can trace through solver logic, identify numerical issues. Won't verify physics. | Good at refactoring solver structure. Won't verify math. |
| **Mesh Generation** | Standard code review. Good at catching memory issues. | Can understand mesh data structures across files. Good at migration tasks. | Good at multi-file mesh refactoring. |
| **Template Metaprogramming** | Moderate — struggles with deep TMP. | Strong — large context helps with complex template chains. | Good — Composer can edit related templates together. |
| **OpenMP Parallelism** | Good at flagging thread safety basics. | Can analyze entire parallel regions, suggest fixes. | Good at adding parallelism to existing code. |
| **Build System (MSBuild)** | No build integration. | Can run builds, parse errors, iterate fixes. | Can run builds via terminal. |
| **Legacy Code (20+ yr)** | Limited context for understanding legacy patterns. | Best at understanding large legacy codebases (1M+ token context). | Good with Composer for targeted legacy updates. |

### None of Them Understand Physics

> **Critical reminder (same as companion guide):** No AI coding agent understands finite element theory, structural mechanics, or CAE physics. They all catch **software engineering issues** — memory leaks, thread safety, style violations, performance anti-patterns. A human domain expert must validate any changes to solver algorithms, element formulations, or numerical methods.

---

## 7. Benefits & Drawbacks Summary

### GitHub Copilot

| ✅ Benefits | ❌ Drawbacks |
|---|---|
| Native Visual Studio 2022 integration | Limited cross-file awareness |
| Zero workflow disruption | Can't run builds or tests |
| PR review automation (GitHub) | Smaller context window |
| Lowest cost ($19/user/mo) | Reactive only — not agentic |
| Enterprise compliance (IP indemnity, SOC 2) | Less effective on complex TMP |
| Model flexibility (GPT-4o, Claude, Gemini) | Usage-based credit system for advanced features |

### Claude Code

| ✅ Benefits | ❌ Drawbacks |
|---|---|
| Massive context window (1M+ tokens) | Terminal-only — no IDE UI |
| Can run MSBuild, parse errors, iterate | No inline completions |
| Best for legacy codebase understanding | Higher cost for heavy usage ($100-200/mo) |
| Autonomous multi-step tasks | Requires developer trust in autonomous edits |
| Works alongside VS (no IDE switch) | No PR review integration |
| Best reasoning on complex C++ logic | Learning curve for terminal workflow |

### Cursor

| ✅ Benefits | ❌ Drawbacks |
|---|---|
| Best multi-file editing (Composer) | **Cannot replace Visual Studio for VC++** |
| Model-agnostic (switch between best models) | Requires IDE switch (workflow disruption) |
| Visual diff review | No MSVC debug engine |
| Good for refactoring tasks | No native MSBuild project system |
| Familiar VS Code interface | Higher team cost ($40-120/user/mo) |
| Tab autocomplete | IntelliSense differs from VS |

### Windsurf (Devin Desktop)

| ✅ Benefits | ❌ Drawbacks |
|---|---|
| Autonomous "Cascade" multi-file editing | Same VS Code limitations as Cursor |
| Good at coordinated changes | Daily/weekly usage quotas |
| Integrated agent experience | Acquired by Cognition — uncertain roadmap |
| Decent pricing ($20-40/user/mo) | Not purpose-built for C++ |
| | Smaller user community than Copilot/Cursor |

---

## 8. Recommendation for the Organization

### The Layered Approach

Given that the application is a VC++ project built in Visual Studio, the recommended strategy is a **layered approach**, not a wholesale tool switch:

```
LAYER 1: GitHub Copilot Business ($19/user) — ALL 50 DEVELOPERS
  ├── Inline completions while writing C++ in Visual Studio
  ├── PR code reviews on GitHub (automated)
  ├── Chat for quick questions ("how do I use std::variant here?")
  └── Custom review rules via copilot-instructions.md

LAYER 2: Claude Code Max ($100/user) — 5-10 SENIOR DEVELOPERS
  ├── Complex multi-file refactoring tasks
  ├── Legacy code understanding and migration
  ├── Build error diagnosis and iterative fixing
  ├── Large-scale changes (pointer migration, API updates)
  └── Runs in terminal alongside Visual Studio (no IDE switch)

LAYER 3 (Optional): Cursor Teams ($40/user) — EVALUATE WITH 3-5 DEVELOPERS
  ├── Trial for developers who are comfortable with VS Code
  ├── Useful for test writing and documentation tasks
  └── Evaluate if Composer adds value beyond Claude Code
```

### Why NOT Switch Entirely to Cursor or Windsurf

For a team that:
- Has 20+ years invested in Visual Studio workflows
- Uses MSVC-specific features (debug engine, profiler, static analysis)
- Relies on MSBuild project system (.sln/.vcxproj)
- Has complex build configurations and dependencies

**Switching IDEs is too disruptive.** The productivity loss from losing VS-specific tooling would outweigh the AI gains from Cursor/Windsurf.

### Recommended Budget

| Layer | Users | Monthly | Annual |
|---|---|---|---|
| Copilot Business | 50 | $950 | $11,400 |
| Claude Code Max 5x | 5 senior | $500 | $6,000 |
| Cursor Teams (trial) | 3 eval | $120 | $1,440 |
| **Total** | | **$1,570** | **$18,840** |

**Cost per developer (blended): ~$377/year = ~$31/month**

### Decision Matrix

| If your priority is... | Go with... |
|---|---|
| Minimum cost, maximum coverage | Copilot Business only ($228/dev/year) |
| Best ROI for complex C++ work | Copilot + Claude Code for leads ($348/dev/year avg) |
| Maximum AI capability regardless of cost | Copilot + Claude Code + Cursor trial ($377/dev/year avg) |
| Enterprise compliance & IP protection | Copilot Enterprise ($468/dev/year) |

---

## 9. Security, Privacy & Data Training — Will They Learn Your Code?

> **This is the #1 concern for enterprise CAE code.** Your C++ solver algorithms, mesh generation logic, and proprietary FEA implementations are trade secrets. Here's the honest breakdown.

### The Big Question: Does My Code Get Used for Training?

| Plan Type | Copilot | Claude Code | Cursor | Windsurf |
|---|---|---|---|---|
| **Enterprise/Business** | ❌ **No training** | ❌ **No training** | ❌ **No training** | ❌ **No training** |
| **Individual Pro/Free** | ⚠️ **Yes by default** (opt-out available) | ⚠️ **Yes if opted in** | ⚠️ **Depends on model provider** | ⚠️ **Depends on model provider** |

> **Critical rule: ALL developer seats MUST be on Enterprise/Business/Team plans.** Individual/Pro accounts on corporate machines = your proprietary C++ code potentially enters training pipelines.

### Data Privacy Comparison — Enterprise Plans

| Security Aspect | GitHub Copilot Enterprise | Claude Code (Enterprise/API) | Cursor Teams | Windsurf Teams |
|---|---|---|---|---|
| **Code used for training?** | ❌ No | ❌ No | ❌ No | ❌ No |
| **Code stored at rest?** | Transient only (discarded after response) | 30-day retention, then deleted. ZDR available | Transient | Transient |
| **IP Indemnification** | ✅ Yes (legal protection against copyright claims) | ⚠️ Via commercial terms only | ⚠️ Via commercial terms | ❌ Not established |
| **SOC 2 Type 2** | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Not confirmed |
| **ISO 27001** | ✅ Yes | ✅ Yes | ❌ Not confirmed | ❌ Not confirmed |
| **Admin audit logs** | ✅ Yes | ⚠️ Requires AI gateway | ✅ Yes (Teams) | ✅ Yes (Teams) |
| **SSO/SAML** | ✅ Enterprise only | ✅ Enterprise only | ✅ Teams | ✅ Enterprise |
| **Content exclusion** | ✅ Can exclude repos/paths | ⚠️ Developer-managed | ⚠️ Manual via .cursorignore | ⚠️ Manual |
| **Zero Data Retention (ZDR)** | ✅ Available | ✅ Available (API) | ❌ Not available | ❌ Not available |
| **Data Processing Agreement (DPA)** | ✅ Yes | ✅ Yes (commercial) | ✅ Yes (Teams/Enterprise) | ⚠️ Contact sales |

### Claude Code — Specific Security Concerns

Claude Code is uniquely different because it's an **autonomous agent with filesystem and shell access**. This introduces risks that IDE-based tools don't have:

#### What Claude Code Can Access

```
When you run Claude Code in your repo, it can:

  ✅ READ any file in the project directory (and subdirectories)
     → Your entire C++ codebase is readable
     → Headers, source files, build configs, scripts
     
  ✅ EXECUTE shell commands (with your permission)
     → msbuild, make, cmake, git, etc.
     → Could theoretically run ANY command
     
  ✅ WRITE/MODIFY files
     → Can edit source code directly
     → Can create new files
     
  ✅ SEND code to Anthropic's servers for LLM processing
     → Code is sent as context for the AI to reason about
     → On Enterprise: NOT used for training
     → On Pro/Max: MAY be used for training (opt-out available)
```

#### What Anthropic Does With Your Code (Enterprise/API)

```
YOUR CODE → sent to Anthropic API → processed by Claude model → response returned
                    │
                    ├── NOT stored for training ✅
                    ├── NOT shared with other customers ✅
                    ├── NOT accessible to Anthropic employees ✅ (except safety review)
                    ├── Retained for up to 30 days (abuse prevention) ⚠️
                    ├── ZDR option: zero retention after response ✅
                    └── Safety-flagged content: retained up to 2 years ⚠️
```

#### The "Shadow AI" Risk

> **Biggest real-world risk:** A developer installs Claude Code on their personal laptop, uses their personal Pro ($20/mo) account, and opens the proprietary C++ repo. Their code IS potentially used for training because they're on a consumer plan.

**Mitigation:**
- Enforce enterprise accounts via IT policy
- Block personal AI tool installations on corporate machines
- Use an AI Gateway (middleware) to route all AI requests through sanctioned channels
- Periodic audits of installed AI tools on developer machines

### Copilot — Security Advantages for Enterprise

GitHub Copilot has the most mature enterprise security story because of Microsoft's enterprise DNA:

| Feature | Why It Matters for CAE Code |
|---|---|
| **Content exclusion policies** | Admin can exclude `src/solver/**` from Copilot context — keeps proprietary algorithms out of AI entirely |
| **IP Indemnification** | If Copilot suggests code that violates someone's copyright, Microsoft provides legal protection |
| **Audit logs** | CISO can see who used Copilot, how often, what models — compliance-ready |
| **Organization-wide policies** | Force specific settings across all 50 developers — no individual overrides |
| **GitHub-native** | Code never leaves the GitHub ecosystem — no third-party data sharing |

### Risk Matrix for CAE C++ Code

| Risk | Copilot Enterprise | Claude Code Enterprise | Claude Code Pro (Individual) |
|---|---|---|---|
| Code used for training | ✅ Safe | ✅ Safe | ⚠️ **Risk — opt-out required** |
| Code stored on vendor servers | ✅ Transient only | ⚠️ Up to 30 days | ⚠️ Up to 30 days |
| Unauthorized code access | ✅ Low (IDE-only) | ⚠️ Medium (filesystem access) | ⚠️ Medium |
| Accidental code modification | ✅ Low (suggestions only) | ⚠️ Medium (autonomous edits) | ⚠️ Medium |
| Compliance audit trail | ✅ Full | ⚠️ Requires AI gateway | ❌ None |
| IP indemnification | ✅ Yes | ⚠️ Commercial terms | ❌ No |

### Recommendations for Protecting CAE Code

```
MANDATORY (before any tool deployment):
  1. ALL seats on Enterprise/Business/Team plans — NEVER individual accounts
  2. Corporate IT policy prohibiting personal AI tools on work machines
  3. Legal review of vendor DPA (Data Processing Agreement)
  4. Define which code directories are AI-accessible vs excluded

FOR COPILOT:
  5. Enable content exclusion for most sensitive solver/IP code
  6. Enable audit logging
  7. Set organization-wide model and feature policies

FOR CLAUDE CODE:
  8. Use API access (not Pro/Max consumer accounts) for best data controls
  9. Consider Zero Data Retention (ZDR) option
  10. Implement .claude/settings.json to restrict file access patterns
  11. Train developers: always review autonomous changes before committing
  12. Consider running Claude Code in a sandboxed container/VM

FOR MAXIMUM SECURITY:
  13. Deploy via AWS Bedrock or Google Cloud Vertex AI
      → Anthropic never sees your data at all
      → Code processed within YOUR cloud environment
      → Full compliance with internal security policies
```

### The AWS Bedrock / Vertex AI Option

For organizations with the strictest security requirements, both Copilot and Claude models can be deployed through cloud intermediaries:

| Deployment | How It Works | Security Benefit |
|---|---|---|
| **Claude via AWS Bedrock** | Claude model runs in YOUR AWS account. Code never reaches Anthropic. | Maximum isolation. Full AWS compliance (FedRAMP, HIPAA, etc.) |
| **Claude via Google Vertex AI** | Claude model runs in YOUR GCP project. Code never reaches Anthropic. | Maximum isolation. Full GCP compliance. |
| **Copilot via Azure** | Already runs through Azure. Microsoft's enterprise compliance applies. | SOC 2, ISO 27001, FedRAMP out of the box. |

> **For your organization's CAE code:** If the CISO requires that proprietary solver code never leaves the corporate cloud, deploying Claude via **AWS Bedrock** or **Vertex AI** eliminates the data sharing concern entirely. The model runs in your environment — Anthropic never sees the code.

---

## 10. GitHub Enterprise — Cloud vs Server

If your organization decides to adopt GitHub, you'll need to choose between **Enterprise Cloud** and **Enterprise Server**. This is a fundamental infrastructure decision.

### What's the Difference?

| | **Enterprise Cloud** | **Enterprise Server** |
|---|---|---|
| **Where it runs** | GitHub.com (hosted by GitHub/Microsoft) | **Your own servers** (on-prem or your private cloud) |
| **URL** | `github.com/your-org` | `github.yourcompany.com` |
| **Maintenance** | GitHub handles updates, backups, uptime | **Your team** manages updates, backups, infrastructure |
| **Price** | **$21/user/month** | **$21/user/month** (same license cost, but add your infra + ops cost) |
| **Copilot support** | ✅ Full — all features | ⚠️ Limited — Copilot still calls GitHub's cloud APIs |
| **GitHub Actions** | ✅ GitHub-hosted runners available | ⚠️ Self-hosted runners only (you provide compute) |
| **Uptime SLA** | 99.9% (GitHub-managed) | Depends on your infrastructure team |
| **Data residency** | GitHub's data centers (US, EU options available) | **Your data center** — full control over location |
| **Setup time** | Minutes (create org, add users) | Days to weeks (provision servers, configure, test) |
| **SAML/SSO** | ✅ Yes | ✅ Yes |
| **Audit logging** | ✅ Yes (API + UI) | ✅ Yes (local logs) |
| **Network isolation** | ⚠️ Shared infrastructure (logically isolated per org) | ✅ **Full network isolation** — runs behind your firewall |
| **Feature releases** | ✅ Latest features immediately | ⚠️ Features lag behind Cloud by 3-6 months |
| **Disaster recovery** | GitHub handles it | **Your responsibility** — backups, failover, etc. |

### When to Choose Cloud vs Server

```
Choose ENTERPRISE CLOUD if:
  ✅ You want zero infrastructure management
  ✅ Code on GitHub's servers is acceptable (encrypted at rest + in transit)
  ✅ You want the latest features and Copilot capabilities immediately
  ✅ You want GitHub-hosted Actions runners (no self-managed compute)
  ✅ Your team doesn't have dedicated DevOps for GitHub infra
  → 90% of organizations choose this option

Choose ENTERPRISE SERVER if:
  ✅ Regulatory requirement mandates code CANNOT leave your network
  ✅ Air-gapped environment (no internet access)
  ✅ CISO mandate: all source code must stay on-premise
  ✅ You have a dedicated infra/platform team to manage it
  ⚠️ You accept that features arrive 3-6 months later
  ⚠️ You accept the operational burden of managing GitHub infrastructure
```

### The Copilot Catch with Enterprise Server

> ⚠️ **Important:** Even with Enterprise Server (on-prem), **Copilot still sends code snippets to GitHub's cloud** for AI processing. There is no fully on-prem Copilot deployment. 

This means:

| Scenario | Enterprise Cloud | Enterprise Server |
|---|---|---|
| Code hosted where? | GitHub.com (cloud) | Your servers (on-prem) |
| Copilot completions processed where? | GitHub's cloud ✅ | **Still GitHub's cloud** ⚠️ |
| Code snippets leave your network? | Yes (by design) | **Yes (for Copilot only)** ⚠️ |

If your CISO's concern is specifically about code leaving the network, Enterprise Server **does not solve the Copilot problem**. For that scenario, you'd need:
- **Option A:** Use Enterprise Server WITHOUT Copilot (lose AI benefits)
- **Option B:** Use Enterprise Cloud WITH Copilot Business/Enterprise (accept cloud processing with enterprise data protections)
- **Option C:** Use Enterprise Server + Claude Code via AWS Bedrock/Vertex AI (code processed in YOUR cloud, not GitHub's)

### Cost Comparison — 50 Developers

| | Enterprise Cloud | Enterprise Server |
|---|---|---|
| GitHub license | $21 × 50 = **$1,050/mo** | $21 × 50 = **$1,050/mo** |
| Infrastructure | $0 (included) | ~$500-2,000/mo (servers, storage, backups) |
| Ops team time | $0 (GitHub-managed) | ~$2,000-5,000/mo (partial FTE for maintenance) |
| Copilot Business | $19 × 50 = $950/mo | $19 × 50 = $950/mo |
| **Total monthly** | **~$2,000** | **~$4,500-9,000** |
| **Total annual** | **~$24,000** | **~$54,000-108,000** |

> Enterprise Server costs **2-4x more** than Cloud when you factor in infrastructure and operations. The license is the same — the difference is everything you have to manage yourself.

### Recommendation

For an organization running workloads on Google Distributed Cloud (GDC) — meaning you're already a cloud-native shop — **Enterprise Cloud is the right choice**:

1. ✅ No infrastructure to manage
2. ✅ Full Copilot support with latest features
3. ✅ GitHub Actions with hosted runners
4. ✅ Lower total cost of ownership
5. ✅ Enterprise data protections (no training, audit logs, SSO)
6. ✅ Your code is already in cloud environments (GDC) — GitHub Cloud is consistent with that model

Enterprise Server only makes sense for **air-gapped or heavily regulated environments** where code physically cannot leave the corporate network — and even then, Copilot won't work fully on-prem.

---

> *This document is a companion to the [Copilot C++ Review & Cost Guide](Copilot-CPP-Review-Models-Cost-Guide.md). See also:*
> - *[CEO Briefing](GITHUB-Briefing-Migration-Proposal.md)*
> - *[Technical Details — Full Report](CVS-to-GitHub-Migration-Detailed-Report.md)*
> - *[Technical Q&A — 65+ Questions](Technical-QA-Team-Discussion.md)*
