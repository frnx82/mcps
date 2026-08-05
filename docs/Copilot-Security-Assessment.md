# AI Coding Security Assessment — Copilot vs Claude Code
## Does the AI Read, Store, or Learn From Your Proprietary Code?

> **For:** Engineering & Management Teams  
> **Date:** August 2026  
> **Decision:** Layer 1 (GitHub Copilot Enterprise) — Security Validation

---

## 1. The Core Concern

> *"We need AI-assisted development, but our C++ CAE source code contains proprietary algorithms, solver logic, and trade secrets. We need absolute clarity: does the AI read our code? Does it store it? Does it learn from it?"*

**Short answer:** All AI coding tools MUST read your code to function — that's how they work. The critical questions are: **where is it sent, how long is it kept, and is it used for training?**

---

## 2. How GitHub Copilot Actually Works

### What Happens When You Type Code

```
STEP 1: You type code in Visual Studio
           ↓
STEP 2: Copilot reads the current file + nearby open files
        (typically 1,500-8,000 tokens of surrounding context)
           ↓
STEP 3: This context is sent to GitHub's cloud (Azure)
        via encrypted HTTPS (TLS 1.2+)
           ↓
STEP 4: AI model processes the context and generates a suggestion
           ↓
STEP 5: Suggestion is returned to your IDE
           ↓
STEP 6: The context is DISCARDED — not stored, not logged, not saved
```

### What Copilot Reads (and Doesn't)

| What Copilot Reads | Scope |
|---|---|
| Current file you're editing | ✅ Full file content |
| Open tabs in your IDE | ✅ Used for context |
| Files in the same project | ⚠️ Only if Enterprise codebase indexing is enabled |
| Files NOT open in your IDE | ❌ Not read |
| Your build artifacts / binaries | ❌ Not read |
| Your databases or config files with secrets | ❌ Not read (unless open in editor) |

> **Key point:** Copilot only reads what's visible in your editor session. It does NOT scan your entire repository or hard drive.

### What Happens to Your Code on GitHub's Servers

| Question | Copilot Enterprise Answer |
|---|---|
| Is my code sent to the cloud? | **Yes** — code snippets are sent for AI processing |
| How much code is sent? | ~1,500-8,000 tokens per request (~50-250 lines of context) |
| Is my code stored after the response? | **No** — discarded immediately after generating a suggestion |
| Is my code used to train AI models? | **No** — contractually guaranteed for Business/Enterprise |
| Is my code visible to GitHub employees? | **No** — not logged, not accessible |
| Is my code shared with other customers? | **No** — completely isolated |
| Is my code encrypted in transit? | **Yes** — TLS 1.2+ encryption |
| Can I exclude sensitive files? | **Yes** — content exclusion policies let you block specific paths |

### Content Exclusion — Protecting Your Most Sensitive Code

Copilot Enterprise lets admins **exclude specific files and directories** from AI context:

```
Example: Exclude proprietary solver code from Copilot entirely

Organization Settings → Copilot → Content Exclusion:
  - "src/solver/core/**"        → Solver algorithms never sent to AI
  - "src/proprietary/**"        → Trade secret code excluded
  - "*.key, *.pem, *.env"      → Credentials never sent

Result: When a developer edits files in excluded paths,
        Copilot is DISABLED for those files. Zero data leaves.
```

---

## 3. How Claude Code Actually Works

### What Happens When You Use Claude Code

```
STEP 1: You run Claude Code in your terminal
           ↓
STEP 2: Claude Code has FULL ACCESS to your entire project directory
        (reads ANY file in the repo — not just open files)
           ↓
STEP 3: Claude Code decides what files to read based on the task
        (could be 10 files or 100+ files — you see but don't control)
           ↓
STEP 4: Selected file contents are sent to Anthropic's servers
        (could be thousands of lines of code per request)
           ↓
STEP 5: AI processes and returns suggestions / edits
           ↓
STEP 6: Code is retained on Anthropic's servers for up to 30 DAYS
        (for abuse prevention — can be reduced with ZDR option)
```

### Critical Differences from Copilot

| Aspect | Copilot Enterprise | Claude Code |
|---|---|---|
| **What it reads** | Only current file + open tabs | **Entire project directory** — any file |
| **How much code is sent** | ~50-250 lines per request | **Potentially thousands of lines** per session |
| **Who controls what's read** | IDE limits context automatically | **Claude Code decides** what files to read |
| **Data retention** | **Zero** — discarded immediately | **Up to 30 days** (ZDR option available) |
| **Training on your code** | ❌ No (Enterprise) | ❌ No (Enterprise/API) |
| **Filesystem access** | ❌ None — IDE only | ✅ **Full read/write/execute** |
| **Can run commands** | ❌ No | ✅ **Yes — builds, scripts, git, anything** |
| **Content exclusion** | ✅ Admin-controlled | ⚠️ Developer-managed (.claudeignore) |
| **Admin audit trail** | ✅ Full organizational logs | ⚠️ Requires AI gateway middleware |

---

## 4. Security Risk Comparison

### Risk Matrix

| Security Risk | Copilot Enterprise | Claude Code Enterprise | Claude Code Pro (Individual) |
|---|---|---|---|
| Code used for AI training | ✅ **Safe** — contractual guarantee | ✅ **Safe** — contractual guarantee | ⚠️ **Risk** — opt-out required |
| Code stored on vendor servers | ✅ **Safe** — zero retention | ⚠️ **30-day retention** | ⚠️ **30-day retention** |
| Entire codebase readable by AI | ⚠️ **Partial** — only editor context | ❌ **Full access** — reads anything | ❌ **Full access** |
| Unauthorized code modifications | ✅ **Low** — suggestions only | ⚠️ **Medium** — autonomous edits | ⚠️ **Medium** |
| Shadow AI (personal accounts) | ✅ **Manageable** — org policies | ⚠️ **Harder to control** — terminal tool | ❌ **High risk** |
| Compliance audit trail | ✅ **Full** — built-in | ⚠️ **Requires gateway** | ❌ **None** |
| IP indemnification | ✅ **Yes** — Microsoft backs it | ⚠️ **Commercial terms only** | ❌ **No** |
| SOC 2 Type 2 | ✅ **Yes** | ✅ **Yes** | ✅ **Yes** |

### Verdict

```
FOR MAXIMUM CODE SECURITY:

  ✅ GitHub Copilot Enterprise — RECOMMENDED
     • Code snippets sent only from editor context (not full repo)
     • Zero retention — discarded immediately after response
     • Content exclusion — admin blocks sensitive directories
     • Full audit trail — CISO can monitor all usage
     • IP indemnification — legal protection included
     • No filesystem access — can't read beyond editor

  ⚠️ Claude Code — NOT RECOMMENDED for security-sensitive code
     • Reads entire project directory (not just editor files)
     • 30-day data retention (even on Enterprise)
     • Filesystem + shell access = larger blast radius
     • No admin-controlled content exclusion
     • Requires additional AI gateway for audit compliance
```

---

## 5. Even More Secure Options (Beyond Standard Copilot)

If the organization requires additional security beyond Copilot Enterprise's default protections:

### Option 1: Copilot Enterprise + Content Exclusion (Recommended)

```
Security Level: ████████░░ (8/10)
Cost: $39/user/month
Setup: Configure content exclusion for sensitive solver/algorithm code

What's protected:
  ✅ Excluded files NEVER sent to AI — Copilot disabled for those paths
  ✅ All other code uses Copilot normally
  ✅ Developers in excluded paths can still use Copilot Chat (Q&A)
  ✅ Zero data retention on all requests
```

### Option 2: Copilot Enterprise + GitHub Enterprise Managed Users (EMU)

```
Security Level: █████████░ (9/10)
Cost: $39/user/month + GitHub Enterprise Cloud
Setup: All developer accounts managed by your org's identity provider

Additional protections:
  ✅ Developers can ONLY access org repos (no personal repos)
  ✅ Cannot fork to personal accounts
  ✅ Cannot copy code to external destinations
  ✅ Full identity governance via SAML/SSO
  ✅ All Copilot usage tied to managed enterprise identity
```

### Option 3: Self-Hosted AI (Maximum Security — No Data Leaves)

```
Security Level: ██████████ (10/10)
Cost: Significantly higher (infrastructure + model hosting)
Setup: Run open-source AI models on your own infrastructure

How it works:
  - Host models like CodeLlama, StarCoder, or DeepSeek on your servers
  - Use VS Code extension (Continue.dev) to connect to self-hosted model
  - Code NEVER leaves your network
  - Trade-off: AI quality is lower than Copilot/Claude

Not recommended unless:
  - Air-gapped environment (no internet)
  - Regulatory mandate: zero external data transmission
  - Government/defense classification requirements
```

---

## 6. Recommendation

### For Your Organization

Given that:
- Code security is the top priority
- You have proprietary C++ CAE algorithms to protect
- You need enterprise compliance and audit trails
- You want AI productivity benefits without security compromise

**Go with: GitHub Copilot Enterprise ($39/user/month)**

With these security configurations:
1. ✅ Content exclusion on `src/solver/core/**` and proprietary algorithm directories
2. ✅ SAML/SSO via your identity provider
3. ✅ Audit logging enabled
4. ✅ Organization-wide Copilot policies (no individual overrides)
5. ✅ Enterprise Managed Users (EMU) if maximum control needed
6. ❌ Skip Claude Code for now — security profile doesn't meet your requirements

---

> **Bottom line:** Copilot Enterprise sends small code snippets, retains nothing, trains on nothing, and lets you exclude sensitive directories. Claude Code reads your entire repo, retains data for 30 days, and has filesystem access. For security-first organizations, Copilot Enterprise is the clear choice.
