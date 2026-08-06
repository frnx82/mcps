# Zero Data Retention (ZDR) — Can Claude Code Match Copilot's Security?
## Evaluating Claude Code with ZDR as an Alternative or Complement to Copilot Enterprise

> **For:** Engineering & Management Teams  
> **Date:** August 2026  
> **Context:** Follows the Copilot Security Assessment — explores whether enabling ZDR on Claude Code closes the security gap

---

## 1. What Is ZDR (Zero Data Retention)?

**ZDR = Zero Data Retention** — a policy where the AI vendor deletes your code immediately after processing, keeping nothing on their servers.

### Standard vs ZDR — How Your Code Is Handled

| | Standard (Default) | ZDR (Zero Data Retention) |
|---|---|---|
| **What happens to your code** | Code is sent → AI processes → response returned → **code kept for up to 30 days** | Code is sent → AI processes → response returned → **code deleted immediately** |
| **Why vendors retain data** | Abuse prevention, safety monitoring, service improvement | N/A — nothing to retain |
| **Who can see retained data** | No one (except if safety-flagged) | No one — it's gone |
| **Risk of data breach** | Low but non-zero (data exists on servers) | Near zero (data doesn't persist) |

### ZDR Availability by Vendor

| Vendor / Product | ZDR Available? | How to Enable | Default Behavior |
|---|---|---|---|
| **GitHub Copilot Enterprise** | ✅ **Already zero retention by default** | No action needed — built-in | Code discarded after response |
| **GitHub Copilot Business** | ✅ **Already zero retention by default** | No action needed — built-in | Code discarded after response |
| **Anthropic Claude (API)** | ✅ Available | Contact Anthropic sales or set in API config | 30-day retention without ZDR |
| **Anthropic Claude Code (Enterprise)** | ✅ Available | Enterprise agreement with ZDR clause | 30-day retention without ZDR |
| **Anthropic Claude Pro/Max (Consumer)** | ❌ **NOT available** | Cannot enable ZDR on consumer plans | 30-day retention, may be used for training |
| **Cursor Teams** | ❌ Not available | Depends on underlying model provider | Transient (claimed) |
| **Windsurf Teams** | ❌ Not available | Depends on underlying model provider | Transient (claimed) |

### Visual: How ZDR Changes the Data Flow

```
COPILOT ENTERPRISE (Zero retention by default):
  Your code snippet → GitHub/Azure cloud → AI processes → suggestion returned
  └→ Code DELETED immediately ✅
  └→ Nothing stored on any server ✅
  └→ No action required ✅

CLAUDE CODE WITHOUT ZDR (Default):
  Your code → Anthropic servers → AI processes → response returned
  └→ Code KEPT for 30 DAYS ⚠️
  └→ Sits on Anthropic's servers for abuse review ⚠️
  └→ Proprietary C++ algorithms stored externally ⚠️

CLAUDE CODE WITH ZDR (Must be enabled):
  Your code → Anthropic servers → AI processes → response returned
  └→ Code DELETED immediately ✅
  └→ Same behavior as Copilot ✅
  └→ BUT: requires API/Enterprise plan + explicit configuration ⚠️
```

---

## 2. With ZDR Enabled, Can Claude Code Replace Copilot?

### What ZDR Fixes

ZDR eliminates the **data retention concern** — the #1 objection to Claude Code in the security assessment. With ZDR enabled:

- ✅ Code is not stored for 30 days
- ✅ Code is not retained on Anthropic's servers
- ✅ Data handling matches Copilot's zero-retention behavior
- ✅ Code is not used for model training (Enterprise/API plans)

### What ZDR Does NOT Fix

**Data retention was only ONE of several security differences.** Even with ZDR enabled, significant gaps remain:

| Security Concern | Copilot Enterprise | Claude Code + ZDR | Gap Closed? |
|---|---|---|---|
| Code used for training? | ❌ No | ❌ No | ✅ **Same** |
| Data retention? | Zero (immediate delete) | **Zero (with ZDR)** | ✅ **Same now** |
| How much code is sent per request? | ~50-250 lines (editor context) | **Thousands of lines** (reads full files) | ⚠️ **Gap remains** |
| Who decides what code is sent? | IDE limits context automatically | **Claude Code decides** — reads any file it wants | ⚠️ **Gap remains** |
| Admin content exclusion? | ✅ Admin blocks sensitive directories | ❌ Developer-managed only (.claudeignore) | ⚠️ **Gap remains** |
| Filesystem access? | ❌ None — IDE suggestion only | ✅ **Full read/write/execute access** | ⚠️ **Gap remains** |
| Can run shell commands? | ❌ No | ✅ **Yes — build, git, any command** | ⚠️ **Gap remains** |
| [IP indemnification](#appendix-a-what-is-ip-indemnification)? | ✅ Microsoft provides legal protection | ⚠️ Commercial terms only | ⚠️ **Gap remains** |
| Centralized audit logs? | ✅ Built-in org-level logging | ❌ Requires third-party AI gateway | ⚠️ **Gap remains** |
| Org-wide policy enforcement? | ✅ Admin controls all settings | ❌ Per-developer configuration | ⚠️ **Gap remains** |
| IP allow list (network restriction)? | ✅ Built-in — restrict to company network | ❌ Not available | ⚠️ **Gap remains** |
| Account management? | ✅ Enterprise Managed Users | ❌ Individual accounts | ⚠️ **Gap remains** |

> **Score: ZDR closes 2 out of 12 security concerns.** The remaining 10 are structural differences between an IDE assistant (Copilot) and an autonomous agent (Claude Code).

---

## 3. The Remaining Risks — Even With ZDR

### Risk 1: Blast Radius — How Much Code Is Exposed

```
COPILOT per request:
  → Reads: current file + open tabs
  → Sends: ~50-250 lines of code to AI
  → Developer SEES what Copilot is using (editor context)

CLAUDE CODE per session:
  → Reads: ANY file in the project directory
  → Sends: potentially 5,000-50,000+ lines per session
  → Claude Code DECIDES what files to read (developer sees but doesn't control)
  
  Example Claude Code session:
    "Refactor the solver module to use smart pointers"
    → Claude reads: solver/*.cpp, solver/*.h, common/*.h, tests/*.cpp
    → 50+ files, 20,000+ lines sent to Anthropic
    → Even with ZDR: 20,000 lines transit through Anthropic's servers
    → vs Copilot: 200 lines per suggestion, never reads beyond editor
```

### Risk 2: No Admin-Controlled Content Exclusion

```
COPILOT:
  Admin configures (developers CANNOT override):
    Content exclusion: "src/solver/core/**" → BLOCKED from AI
    
  Result: Even if a developer opens StiffnessMatrix.cpp,
          Copilot is DISABLED. Zero code leaves the machine.

CLAUDE CODE:
  Developer configures (admin has NO central control):
    .claudeignore file in project root
    
  Risks:
    → Developer forgets to add .claudeignore
    → Developer removes exclusions for convenience
    → New hires don't know about the policy
    → No admin enforcement mechanism
```

### Risk 3: Autonomous Actions

```
COPILOT:
  → Suggests code → Developer accepts or rejects
  → Cannot modify files without developer clicking "Accept"
  → Cannot run any commands
  → READ-ONLY assistance

CLAUDE CODE:
  → Can READ any file in the project
  → Can WRITE/MODIFY files directly
  → Can RUN shell commands (msbuild, git commit, scripts)
  → Can CREATE new files
  → Operates AUTONOMOUSLY with developer approval per action
  
  Risk scenario:
    Claude Code runs "git add . && git commit -m 'fix' && git push"
    → Could push sensitive code changes without thorough review
    → Mitigated by developer awareness, but risk exists
```

### Risk 4: Shadow AI — Personal Accounts

```
COPILOT:
  → Tied to org-managed GitHub account
  → Admin sees all Copilot usage in audit logs
  → Cannot use without org license assignment
  → Enterprise Managed Users prevents personal usage

CLAUDE CODE:
  → Developer can install with personal Pro ($20/mo) account
  → No way for admin to know it's installed
  → Personal account → code MAY be used for training
  → Even with org API key: developer could use personal key instead
```

---

## 4. Security Score Comparison

| Category | Weight | Copilot Enterprise | Claude Code + ZDR |
|---|---|---|---|
| Data retention | 15% | 10/10 | **10/10** (with ZDR) |
| Training exclusion | 15% | 10/10 | 10/10 |
| Blast radius (code exposure) | 20% | 9/10 (small context) | 4/10 (full repo access) |
| Admin control | 15% | 10/10 | 3/10 |
| Audit trail | 10% | 10/10 | 3/10 |
| [IP indemnification](#appendix-a-what-is-ip-indemnification) | 5% | 10/10 | 5/10 |
| Network restriction | 5% | 10/10 | 2/10 |
| Shadow AI prevention | 5% | 9/10 | 3/10 |
| Autonomous action risk | 5% | 10/10 (suggestions only) | 5/10 |
| Compliance readiness | 5% | 10/10 | 5/10 |
| **Weighted Security Score** | **100%** | **~95/100** | **~55/100** |

> **Even with ZDR, Claude Code scores ~55/100 on security vs Copilot's ~95/100.** ZDR closes the data retention gap but the structural differences remain significant.

---

## 5. When Claude Code + ZDR Makes Sense

Despite the security gaps, Claude Code's **coding effectiveness is 15-20% higher** than Copilot for complex tasks. Here's when the trade-off is worth it:

### ✅ Use Claude Code + ZDR For:

| Scenario | Why It's Okay |
|---|---|
| 5-10 **senior engineers** only | Skilled users who understand security boundaries |
| **Non-sensitive code** only (UI, tests, scripts) | Low-value code — blast radius doesn't matter |
| Complex **multi-file refactoring** | Where Copilot's 60-65% effectiveness is insufficient |
| **Build pipeline debugging** | Claude can run msbuild, read errors, iterate |
| **Legacy code understanding** | Claude reads entire modules — essential for 20+ yr codebase |

### ❌ Do NOT Use Claude Code For:

| Scenario | Why Not |
|---|---|
| **Proprietary solver algorithms** | Blast radius too large — reads entire solver module |
| **Patent-pending code** | IP risk — no indemnification |
| **All 50 developers** | Impossible to manage without admin controls |
| **Without signed developer policy** | Shadow AI risk too high |
| **On consumer Pro accounts** | ZDR not available — 30-day retention applies |

---

## 6. Recommended Strategy — Revised With ZDR Option

```
LAYER 1: GitHub Copilot Enterprise ($39/user) — ALL 50 DEVELOPERS
  ├── Daily coding, inline completions, Copilot Chat
  ├── Automated PR code reviews on GitHub
  ├── Content exclusion protects proprietary solver code
  ├── Full admin control, audit logs, IP allow list
  └── Security score: 95/100

LAYER 2 (OPTIONAL): Claude Code + ZDR ($100/user) — 5 SENIOR LEADS ONLY
  ├── Complex refactoring on NON-SENSITIVE modules only
  ├── Used for: UI code, tests, build scripts, documentation
  ├── NEVER used on: solver code, proprietary algorithms, patents
  ├── Security score: 55/100 (acceptable for non-sensitive code)
  │
  ├── Required safeguards:
  │   ✅ API access only (NOT consumer Pro/Max accounts)
  │   ✅ ZDR enabled on all API calls
  │   ✅ .claudeignore excluding all sensitive directories
  │   ✅ Signed developer policy agreement
  │   ✅ Quarterly review of Claude Code usage
  │   ✅ Training: what can/cannot be AI-processed
  │
  └── Cost: 5 users × $100/mo = $500/mo ($6,000/year)

TOTAL ANNUAL COST:
  Copilot Enterprise (50 users):     $23,400/year
  Claude Code + ZDR (5 users):       $6,000/year
  GitHub Enterprise Cloud (50 users): $12,600/year
  ──────────────────────────────────────────────────
  Total:                             $42,000/year
```

---

## 7. Decision Matrix

| If Your Priority Is... | Recommendation |
|---|---|
| **Maximum security, no exceptions** | Copilot Enterprise only. Skip Claude Code entirely. |
| **Security + best coding effectiveness** | Copilot for all + Claude Code with ZDR for 5 senior leads on non-sensitive code |
| **Maximum AI capability** | Both tools — but accept the 55/100 security score for Claude Code |
| **Budget-conscious** | Copilot Business ($19/user) for all. No Claude Code. |
| **CISO requires full audit trail** | Copilot Enterprise only — Claude Code has no centralized logging |
| **Code NEVER leaves company network** | Neither tool — use self-hosted open-source models (CodeLlama, StarCoder) |

---

> **Final verdict:** ZDR closes the data retention gap, making Claude Code's security profile significantly better. However, the **blast radius** (reads entire repo), **lack of admin controls**, and **autonomous agent risks** remain. Claude Code + ZDR is a viable **Layer 2 for 5-10 senior engineers on non-sensitive code**, but it should NOT replace Copilot Enterprise as the primary tool for the full team.

---

## Appendix A: What Is IP Indemnification?

> **In plain language:** IP Indemnification means the AI vendor (Microsoft, in the case of Copilot) takes on the legal and financial responsibility if their AI tool generates code that infringes on someone else's intellectual property.

### Why Does This Matter?

- AI coding tools like Copilot are **trained on billions of lines of publicly available code** — including open-source code with licenses (GPL, MIT, Apache, etc.)
- There is a risk that the AI **suggests code that closely matches or copies someone else's copyrighted work**
- If you use that code in your commercial product and the original author or company discovers it, they could **file a copyright infringement lawsuit**
- Without indemnification, **your company bears all legal costs and damages**
- With indemnification, **the AI vendor bears the legal costs and damages**

### A Simple Example

```
Step 1: A developer asks Copilot to generate a matrix solver function
Step 2: Copilot generates 30 lines of C++ code
Step 3: Those 30 lines happen to closely match code from an open-source
        library licensed under GPL (which requires derivative works
        to also be open-sourced)
Step 4: You include that code in your proprietary, commercial product
Step 5: The original author discovers the match and sues your company
        for copyright infringement

WITHOUT IP Indemnification:
  → Your company hires lawyers                    💰 $200K-500K+
  → Your company pays the settlement/damages       💰 $500K-2M+
  → Your company may be forced to open-source      ⚠️ Catastrophic
     parts of your proprietary product
  → Total risk: $1M+ and potential IP loss

WITH IP Indemnification (Copilot Enterprise):
  → Microsoft's legal team defends your company    ✅ $0 to you
  → Microsoft pays any settlement or damages       ✅ $0 to you
  → Microsoft takes full financial responsibility  ✅ $0 to you
  → Your company is protected                     ✅ No IP risk
```

### What Microsoft's Copilot Copyright Commitment Covers

- ✅ **Legal defense** — Microsoft will defend your company in court if Copilot-generated code leads to a copyright claim
- ✅ **Financial damages** — Microsoft will pay any court-ordered damages or agreed settlements
- ✅ **Applies worldwide** — Not limited to US courts; covers international IP disputes
- ✅ **No cap mentioned** — Microsoft has not published a maximum liability cap for Copilot indemnification
- ✅ **Backed by Microsoft** — A $3 trillion company with one of the largest legal teams in tech

### Conditions to Qualify

Indemnification is **not automatic for all users**. You must meet these conditions:

- ✅ **Plan requirement:** Must be on **Copilot Business ($19/user)** or **Copilot Enterprise ($39/user)** — NOT available on Individual/Free plans
- ✅ **Code referencing filter:** Must have the "suggestions matching public code" filter **enabled** (set to "Block") — this is the feature that detects when a Copilot suggestion matches known public code
- ✅ **Good faith usage:** You must not have intentionally prompted Copilot to reproduce specific copyrighted code (e.g., "copy the exact implementation of XYZ library")
- ✅ **Use the tool as designed:** Standard use of Copilot within the IDE for code generation

### Comparison: Who Offers IP Indemnification?

| Vendor / Product | IP Indemnification | Details |
|---|---|---|
| **GitHub Copilot Enterprise** | ✅ **Yes — full coverage** | Microsoft's Copilot Copyright Commitment |
| **GitHub Copilot Business** | ✅ **Yes — full coverage** | Same commitment as Enterprise |
| **GitHub Copilot Individual/Free** | ❌ **No** | Not covered |
| **Claude Code (Enterprise contract)** | ⚠️ **Negotiable** | Must be explicitly included in your enterprise agreement with Anthropic |
| **Claude Code (Pro/Max consumer)** | ❌ **No** | No protection |
| **Cursor Teams** | ⚠️ **Unclear** | No published indemnification policy |
| **Windsurf** | ❌ **No** | No published indemnification policy |
| **Google Gemini Code Assist** | ✅ **Yes** | Google's indemnification for Enterprise users |

### Why This Is Important for Your Organization

- Your company builds a **commercial C++ CAE product** that is sold to customers
- If AI-generated code in your product matches copyrighted code, your **entire product could be at legal risk**
- GPL-licensed code is particularly dangerous — using GPL code in a proprietary product can require you to **open-source your entire product**
- IP indemnification from Microsoft is essentially a **free insurance policy** that eliminates this risk
- This is one of the **strongest reasons to choose Copilot Enterprise** over alternatives that don't offer this protection

### Key Takeaway for Management

```
IP Indemnification = FREE LEGAL INSURANCE from Microsoft

  What it costs you:     $0 (included in Copilot Enterprise license)
  What it protects:      Your company from copyright lawsuits
  Who pays if sued:      Microsoft (not your company)
  Who defends you:       Microsoft's legal team
  Required action:       Enable "Block" on code referencing filter
  
  Bottom line: If Copilot writes code that gets you sued,
              Microsoft pays. This protection is NOT available
              from Claude Code, Cursor, or Windsurf.
```

