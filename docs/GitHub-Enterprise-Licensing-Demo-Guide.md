# GitHub Enterprise — Step-by-Step Licensing, Demo & Code Exposure Guide

> **Critical Question Answered:** Should you use free tier or paid license before exposing your code?
>
> **Short Answer: DO NOT expose proprietary/production code to GitHub until you have a paid Enterprise license with signed legal agreements.** Use mock/sample code for the initial demo.

---

## ⚠️ The Golden Rule

```
FREE TIER = Demo with MOCK code only (never production code)
PAID ENTERPRISE = Production code (after legal + security controls)
```

> **CAUTION:** Even GitHub's **private repositories** on free/Team tier lack enterprise security controls (SAML SSO, audit logs, IP allow-lists, data residency). Your organization's legal and compliance teams will NOT approve production code on a non-enterprise plan.

---

## Decision Tree: Which Path Are You On?

```
Do you need to demo Copilot to management?
├── YES → Use GitHub Enterprise Cloud 30-day FREE TRIAL
│         with MOCK/SAMPLE code (not production)
│         ├── Demo successful? → Proceed to paid license
│         └── Demo rejected? → No cost, no risk
│
└── Already approved for purchase?
    → Skip trial, go straight to Enterprise license
    → Legal review → Configure security → Migrate real code
```

---

## Phase 1: Safe Demo (Week 1-2) — NO Production Code

### Step 1: Request GitHub Enterprise Cloud Trial (Day 1)

| Action | Details |
|--------|---------|
| **Go to** | https://github.com/enterprise |
| **Click** | "Start a free trial" |
| **Choose** | GitHub Enterprise Cloud (NOT Server) |
| **Trial duration** | 30 days, no credit card required |
| **Create org** | Use a name like `yourcompany-demo` |

> The trial gives you the FULL Enterprise Cloud experience — SAML SSO, audit logs, Copilot access, everything. This is identical to what you'd get with a paid license.

### Step 2: Create a Mock Repository for Demo (Day 1-2)

**DO NOT import your real CVS codebase yet.** Instead:

1. Create a sample C++ repository that mimics your project structure:
   ```
   yourcompany-demo/sample-cpp-project/
   ├── src/
   │   ├── main.cpp
   │   ├── solver/
   │   │   ├── solver.h
   │   │   └── solver.cpp
   │   └── utils/
   │       ├── math_utils.h
   │       └── math_utils.cpp
   ├── tests/
   ├── CMakeLists.txt
   └── README.md
   ```

2. Use **open-source C++ code** or write **dummy functions** that represent your domain (e.g., financial calculations, data processing)

3. This is enough to demonstrate:
   - Copilot code completion in C++
   - Copilot Chat understanding codebase context
   - PR reviews with Copilot
   - Code search across repos

### Step 3: Enable Copilot on Trial Org (Day 2)

1. Go to: `https://github.com/organizations/yourcompany-demo/settings/copilot`
2. Enable **GitHub Copilot Enterprise**
3. Set policy: "Enabled for all members" (or select specific users)
4. Configure Copilot settings:
   - ✅ Suggestions matching public code: **Block** (important for compliance)
   - ✅ Allow Copilot to use your org's code as context: **Enable**

### Step 4: Invite Demo Participants (Day 2-3)

1. Go to: `https://github.com/orgs/yourcompany-demo/people`
2. Invite 3-5 developers who will participate in the demo
3. Each developer installs the Copilot extension in their IDE (VS Code, JetBrains, etc.)

### Step 5: Run the Demo (Day 3-5)

Show stakeholders:
- **Copilot autocomplete** — Type function signatures, watch Copilot complete C++ code
- **Copilot Chat** — Ask questions about the codebase, generate tests, explain code
- **PR reviews** — Create a PR and let Copilot review it
- **Code search** — Natural language search across repositories

> **TIP:** Record the demo session. This is invaluable for getting executive buy-in from people who couldn't attend.

---

## Phase 2: Get Paid License (Week 2-3)

### Step 6: Contact GitHub Sales (Day 5-7)

| Action | Details |
|--------|---------|
| **Contact** | https://github.com/enterprise/contact or your assigned GitHub rep |
| **Request** | Enterprise Cloud quote for your org size |
| **Mention** | You're migrating from CVS, ~75 developers, ~5GB repo |
| **Ask for** | Volume discounts, multi-year pricing, migration assistance |

**Pricing Reference (as of 2026):**

| Plan | Per User/Month | Includes |
|------|---------------|----------|
| GitHub Enterprise Cloud | ~$21/user/month | SSO, audit logs, security features |
| Copilot Enterprise add-on | ~$39/user/month | Code completion, Chat, PR reviews |
| **Total** | **~$60/user/month** | **Full stack** |
| **75 developers × 12 months** | **~$54,000/year** | **Annual estimate** |

### Step 7: Legal Review — BEFORE Any Production Code (Day 7-14)

> **CAUTION:** This is the **most critical step**. DO NOT proceed to Phase 3 until legal signs off.

**Documents your legal team must review:**

| Document | Where to Find |
|----------|---------------|
| GitHub Enterprise Cloud Agreement | Provided by GitHub sales |
| Data Processing Agreement (DPA) | https://github.com/customer-terms |
| GitHub Copilot Product Terms | Included in Enterprise agreement |
| Subprocessor List | https://github.com/subprocessors |
| Security Whitepaper | https://github.com/security |
| SOC 2 Type II Report | Request from GitHub sales |
| Data Residency Documentation | Request if you need EU/specific region |

**Key legal questions your team should verify:**

1. ✅ **IP Ownership**: GitHub does NOT claim ownership of your code (confirmed in ToS)
2. ✅ **Copilot training**: Enterprise Copilot does NOT train on your code (confirmed in product terms)
3. ✅ **Data residency**: Where is your code stored? (US/EU data centers)
4. ✅ **Data retention**: What happens to your code if you cancel?
5. ✅ **Breach notification**: SLA for notifying you of security incidents
6. ✅ **Compliance**: SOC 2, ISO 27001, FedRAMP (if applicable)
7. ✅ **Indemnification**: IP indemnification for Copilot-generated code

### Step 8: Purchase and Activate Enterprise License (Day 14)

Once legal approves:
1. Sign the Enterprise agreement
2. GitHub provisions your Enterprise account
3. Upgrade your trial org (or create a new production org)
4. Set up billing (annual or monthly)

---

## Phase 3: Security Configuration — BEFORE Migrating Code (Week 3-4)

### Step 9: Configure Enterprise Security Controls (Day 14-18)

**These MUST be in place before any production code touches GitHub:**

| Control | How to Configure |
|---------|-----------------|
| **SAML SSO** | Connect to your corporate IdP (Okta, Azure AD, etc.) |
| **2FA enforcement** | Org settings → Security → Require 2FA |
| **IP allow-list** | Enterprise settings → IP allow list → Add your office/VPN ranges |
| **Audit log streaming** | Enterprise → Audit log → Stream to your SIEM (Splunk, etc.) |
| **Repository visibility** | Default to **Internal** or **Private** (NEVER public) |
| **Branch protection** | Require PR reviews, status checks, signed commits |
| **Secret scanning** | Enable to prevent accidental credential exposure |
| **Dependabot** | Enable for vulnerability alerts |
| **Code scanning (CodeQL)** | Enable for C++ static analysis |

### Step 10: Set Up Team Structure (Day 18-20)

```
Enterprise Account: yourcompany
└── Organization: yourcompany-engineering
    ├── Team: platform-team (read/write to platform repos)
    ├── Team: solver-team (read/write to solver repos)
    ├── Team: devops-team (admin on CI/CD repos)
    └── Team: release-managers (maintain permissions)
```

### Step 11: VPN / Network Configuration (Day 18-20)

| Requirement | Details |
|-------------|---------|
| **Firewall rules** | Allow outbound HTTPS to `github.com`, `*.github.com`, `*.githubusercontent.com` |
| **Proxy config** | If corporate proxy, configure `git` to use it: `git config --global http.proxy http://proxy:8080` |
| **IP allow-list** | Restrict GitHub API access to your corporate IP ranges |
| **SSH keys** | Decide on SSH vs HTTPS authentication for git operations |
| **For WFH employees** | They need VPN connected → VPN routes to corporate proxy → proxy connects to GitHub |

---

## Phase 4: Migrate Real Code (Week 4-6)

### Step 12: CVS → Git Migration (ONLY After Steps 7-11 Complete)

Now and ONLY now should you bring production code to GitHub:

1. **Test migration** with a small, non-sensitive module first
2. **Use `cvs2git`** to convert CVS history to Git
3. **Push to a private repository** inside your secured Enterprise org
4. **Verify**: Check that audit logs capture the push, SSO is enforced, IP allow-list works

```bash
# Example migration flow (simplified)
cvs2git --blobfile=blob.dat --dumpfile=dump.dat /path/to/cvs/module
git init my-project
cat blob.dat dump.dat | git fast-import
git remote add origin https://github.com/yourcompany-engineering/my-project.git
git push -u origin main
```

---

## Summary Checklist

```
Phase 1: Safe Demo (NO production code)
  □ Get Enterprise Cloud 30-day trial
  □ Create mock C++ repository
  □ Enable Copilot on trial org
  □ Invite 3-5 developers
  □ Run demo with stakeholders
  □ Record demo for executive review

Phase 2: Legal & Licensing  
  □ Contact GitHub sales for quote
  □ Legal reviews Enterprise agreement
  □ Legal reviews DPA (Data Processing Agreement)
  □ Legal reviews Copilot product terms
  □ Legal confirms: code NOT used for training
  □ Legal confirms: IP ownership retained
  □ Sign Enterprise agreement
  □ Purchase licenses

Phase 3: Security Hardening (BEFORE real code)
  □ Configure SAML SSO with corporate IdP
  □ Enforce 2FA for all members
  □ Set up IP allow-list
  □ Enable audit log streaming to SIEM
  □ Set default repo visibility to Private/Internal
  □ Configure branch protection rules
  □ Enable secret scanning
  □ Enable code scanning (CodeQL for C++)
  □ Configure VPN/proxy for WFH access

Phase 4: Code Migration (AFTER all above)
  □ Test migration with small non-sensitive module
  □ Verify security controls work with real data
  □ Full CVS → Git migration
  □ Decommission CVS (after validation period)
```

---

## Timeline at a Glance

```
Week 1   ████████  Demo with mock code (FREE trial)
Week 2   ████████  Sales call + Legal review starts  
Week 3   ████████  Legal signs off + Purchase license
Week 4   ████████  Security hardening (SSO, 2FA, IP allow-list)
Week 5   ████████  Test migration (small module)
Week 6   ████████  Full CVS → GitHub migration begins
```

> **WARNING:** The biggest mistake companies make is pushing production code to GitHub BEFORE legal review and security controls are in place. Even on a private repo, without SSO and IP restrictions, any employee with a personal GitHub account could accidentally fork the repo or access it from an unsecured network. Get the controls in place FIRST.
