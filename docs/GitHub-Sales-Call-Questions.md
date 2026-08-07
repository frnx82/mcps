# GitHub Sales Call — Questions & Preparation Guide
## Enterprise Cloud + Copilot Enterprise Evaluation

> **Date:** August 2026  
> **Call Purpose:** Evaluate GitHub Enterprise Cloud + Copilot Enterprise for 75 C++ developers  
> **Context:** CVS-to-GitHub migration, AI-assisted development, security-first organization

---

## ⭐ Priority 1: Pricing & Licensing

| # | Question | Why It Matters |
|---|---|---|
| 1 | **What's the best pricing you can offer for 75 seats of GitHub Enterprise Cloud + Copilot Enterprise?** | Published rate is $60/user/mo ($21 + $39). Push for volume discount. |
| 2 | **Is there a bundle discount for Enterprise Cloud + Copilot Enterprise together?** | Some vendors offer 10-20% bundle discount vs buying separately. |
| 3 | **Do you offer annual vs monthly billing? Is there a discount for annual commitment?** | Annual prepay often saves 10-15%. |
| 4 | **Can we start with 10 seats for a pilot and expand to 75 later at the same rate?** | Locks in pricing while reducing initial risk. |
| 5 | **Is there a free trial available for Enterprise Cloud + Copilot Enterprise?** | GitHub sometimes offers 30-60 day Enterprise trials. |
| 6 | **Are there any startup/growth discounts or non-profit pricing if applicable?** | Worth asking — can save 20-50%. |
| 7 | **What happens if we need to reduce seats mid-year?** | Understand flexibility on scaling down if needed. |

**Notes from call:**
> _(fill in during/after call)_

---

## ⭐ Priority 2: Security & Data Privacy

| # | Question | Why It Matters |
|---|---|---|
| 8 | **Can you confirm in writing that Copilot Enterprise does NOT use our code for model training?** | #1 concern for proprietary C++ CAE code. Need written confirmation. |
| 9 | **How does zero data retention work? Is our code ever stored on your servers, even temporarily?** | Clarify: is code discarded immediately after response, or is there any buffer? |
| 10 | **What exactly does the IP indemnification cover? Is there a liability cap?** | If Copilot generates code that infringes copyright, Microsoft pays — confirm scope. |
| 11 | **Can we get a copy of your Data Processing Agreement (DPA) before signing?** | Legal team must review before committing. |
| 12 | **Can you share your SOC 2 Type 2 report and ISO 27001 certification?** | CISO needs these for compliance approval. |
| 13 | **How does content exclusion work technically — are excluded files still sent to the server and discarded, or never sent at all?** | Critical: "never sent" is much safer than "sent and discarded." |
| 14 | **If we enable the IP allow list, does it also restrict Copilot API calls, or just web/git access?** | Ensure Copilot can't be used from outside the company network. |
| 15 | **What happens to code context during a Copilot request — which servers process it, where are they located (US, EU)?** | Data residency requirements. |

**Notes from call:**
> _(fill in during/after call)_

---

## Priority 3: CVS Migration Support

| # | Question | Why It Matters |
|---|---|---|
| 16 | **Do you have a professional services team that helps with CVS-to-Git migration?** | May save significant consulting time if GitHub offers migration support. |
| 17 | **Have you worked with other customers migrating from CVS specifically? Can you share case studies?** | CVS is legacy — want proof they've handled it before. |
| 18 | **Do you offer any migration tools or scripts for CVS-to-GitHub?** | GitHub may have internal tools beyond public cvs2git. |
| 19 | **What's the recommended approach for a ~5 GB repository with DLLs and binary assets?** | Get their Git LFS recommendation for large C++ repos. |

**Notes from call:**
> _(fill in during/after call)_

---

## Priority 4: Copilot Enterprise Features

| # | Question | Why It Matters |
|---|---|---|
| 20 | **What's the difference between Copilot Business ($19) and Copilot Enterprise ($39)? What do we get for the extra $20?** | Justify the $20/user premium — is codebase indexing + PR reviews worth it? |
| 21 | **How does codebase indexing work in Enterprise? Does it index the entire repo or just what's open?** | Understand how much codebase context Copilot Enterprise actually uses. |
| 22 | **Can Copilot review PRs automatically, or does someone have to request it?** | Automated = less friction for developers. |
| 23 | **How well does Copilot work with C++ specifically in Visual Studio 2022? Any C++ customer references?** | C++ is our primary language — need confidence it works well. |
| 24 | **Does Copilot Enterprise support custom instructions (copilot-instructions.md)? Are there limits?** | We've prepared C++ CAE-specific review rules. |
| 25 | **What AI models power Copilot Enterprise today? Can we choose between models?** | Want to know if it's GPT-4, GPT-5, Claude, etc. and if we have model choice. |

**Notes from call:**
> _(fill in during/after call)_

---

## Priority 5: GitHub Actions & CI/CD

| # | Question | Why It Matters |
|---|---|---|
| 26 | **How many GitHub Actions minutes are included with Enterprise Cloud?** | C++ builds are long — need to know if we'll exceed included minutes. |
| 27 | **What are the specs of your hosted Windows runners? Are they sufficient for large C++ builds?** | 4 vCPU may be too slow for C++ — need to understand options. |
| 28 | **Can we use self-hosted runners? Are there any restrictions?** | Plan to use existing build machines as runners. |
| 29 | **Is there additional cost for larger runners (8-core, 16-core)?** | May need bigger runners if cloud builds are too slow. |

**Notes from call:**
> _(fill in during/after call)_

---

## Priority 6: Git LFS (Large File Storage)

| # | Question | Why It Matters |
|---|---|---|
| 30 | **How much LFS storage and bandwidth is included with Enterprise?** | Our DLLs/libraries need LFS — need to budget for overages. |
| 31 | **What's the pricing for additional LFS packs beyond the free tier?** | Published rate is $5/50 GB — confirm for Enterprise. |
| 32 | **For a ~5 GB repo with binary assets, what LFS configuration do you recommend?** | Get their expert recommendation for our specific repo size. |

**Notes from call:**
> _(fill in during/after call)_

---

## Priority 7: Support & Onboarding

| # | Question | Why It Matters |
|---|---|---|
| 33 | **What level of support is included? Is there a dedicated account manager?** | Enterprise should include premium support — confirm. |
| 34 | **Do you offer onboarding or setup assistance for Enterprise customers?** | May get free onboarding help — worth asking. |
| 35 | **What's the typical response time for Enterprise support tickets?** | Need SLA for critical issues. |
| 36 | **Do you have training resources for developers transitioning from CVS to Git?** | 75 developers need Git training — any resources help. |

**Notes from call:**
> _(fill in during/after call)_

---

## Priority 8: Enterprise Managed Users (EMU)

| # | Question | Why It Matters |
|---|---|---|
| 37 | **Should we use Enterprise Managed Users or standard accounts with SAML? What do you recommend?** | EMU = maximum control but limits open-source access. Need their recommendation. |
| 38 | **With EMU, can our developers still access public repos or open-source projects?** | If not, EMU may be too restrictive. |
| 39 | **What IdPs do you support? We're evaluating Azure AD / Okta / Google Workspace.** | Confirm compatibility with whatever IdP we choose. |

**Notes from call:**
> _(fill in during/after call)_

---

## Priority 9: Contract & Legal

| # | Question | Why It Matters |
|---|---|---|
| 40 | **What's the minimum contract term? Can we do month-to-month?** | Flexibility to exit if needed. |
| 41 | **Is there an exit clause if Copilot doesn't meet our expectations?** | Risk mitigation — want an out if AI doesn't work for C++. |
| 42 | **Who owns the code that Copilot generates? Is there any IP assignment to GitHub/Microsoft?** | Must confirm: generated code belongs to US, not GitHub. |

**Notes from call:**
> _(fill in during/after call)_

---

## 🎯 Call Strategy

### Do's

- ✅ **Mention 75 seats** — shows serious intent, gets you to the right pricing tier
- ✅ **Ask about pilot/trial** — lowers initial commitment and risk
- ✅ **Ask for C++ / engineering / CAE customer references** — validate they work for your use case
- ✅ **Request the DPA and security docs BEFORE committing** — legal must review
- ✅ **Ask about bundle pricing** (Enterprise + Copilot together) — unlocks potential discounts
- ✅ **Take notes on exact pricing they quote** — prices are often negotiable
- ✅ **Ask about Professional Services** — free migration help saves you money

### Don'ts

- ❌ **Don't commit to a number of seats on the call** — say "we'll discuss internally"
- ❌ **Don't agree to annual billing without seeing the discount** — compare annual vs monthly
- ❌ **Don't share your budget number** — let them offer first, then negotiate
- ❌ **Don't skip the security questions** — these are your strongest leverage points
- ❌ **Don't sign anything on the call** — take the proposal back for review

---

## After the Call — Checklist

### Documents to Request

| Document | Status |
|---|---|
| Quoted pricing (per seat, total, annual vs monthly) | ☐ Requested |
| Trial/pilot offer details | ☐ Requested |
| Data Processing Agreement (DPA) | ☐ Requested |
| SOC 2 Type 2 audit report | ☐ Requested |
| ISO 27001 certification | ☐ Requested |
| IP indemnification terms (Copilot Copyright Commitment) | ☐ Requested |
| Written no-training confirmation | ☐ Requested |
| C++ / engineering customer case studies | ☐ Requested |
| Enterprise vs Business feature comparison | ☐ Requested |

### Key Answers to Capture

| Question | Their Answer |
|---|---|
| Best price per seat (Enterprise Cloud) | $ _____ /user/mo |
| Best price per seat (Copilot Enterprise) | $ _____ /user/mo |
| Bundle discount available? | Yes / No — details: |
| Annual discount? | _____ % off |
| Trial available? | Yes / No — duration: |
| Minimum contract term | _____ months |
| LFS included storage | _____ GB |
| Actions minutes included | _____ min/mo |
| Larger runners available? | Yes / No — cost: |
| Professional Services for migration? | Yes / No — cost: |
| EMU vs SAML recommendation | _____ |
| Content exclusion: sent-and-discarded or never-sent? | _____ |
| Data processing location (US/EU) | _____ |

---

> **Bring this document to the call. Fill in the "Notes" and "Key Answers" sections during the conversation. Share the completed version with your team and legal after the call.**
