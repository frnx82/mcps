# Modernizing Morpher's Development Infrastructure
## A Proposal for Detroit Engineered Products

> **Prepared for:** CEO, Detroit Engineered Products  
> **Date:** July 2026  
> **Read time:** 10 minutes  
> **Classification:** Internal — Confidential

---

## Why This Document Exists

DEP's flagship product **Morpher** — a Computer-Aided Engineering application with **20+ years of development history** — currently runs on a source code management system called **CVS** (Concurrent Versions System).

CVS was created in **1986** and has had **no active development since 2008**. It is now considered obsolete by the software industry.

This document proposes migrating to **GitHub**, the industry standard used by 100+ million developers worldwide, and adopting **GitHub Copilot**, an AI assistant that helps developers write, review, and test code faster.

---

## The Problem — In Plain Terms

Think of CVS like keeping all your engineering blueprints in a single filing cabinet in one office. If that cabinet is lost, everything is gone. Only one person can edit a blueprint at a time. There's no way to review changes before they're filed. And no new hires know how the filing system works.

![The Problem — Current State](images/table_problem_state_1784555435271.png)

---

## The Solution — What We're Proposing

We propose moving from an obsolete, fragile, single-server system to the industry standard — with AI-powered code assistance built in:

![The Solution — From CVS to GitHub](images/brief_solution_from_to_1784559375193.png)

---

## What Is GitHub Copilot?

Copilot is an AI assistant that sits inside the developer's editor (Visual Studio) and helps them:

![What Is GitHub Copilot?](images/brief_copilot_what_1784559383859.png)

> Copilot does **not** replace engineers. It makes them faster and catches mistakes they might miss. Think of it as spell-check for code — useful, but a human still writes the document.

---

## The Investment

![Annual Investment Breakdown](images/table_annual_cost_1784555443076.png)

### Annual Subscription Cost

![Annual Investment](images/brief_year1_cost_v2_1784593637253.png)

---

## The Return — What We Get Back

### Speed of Delivery

Research from Microsoft (studying 16,223 engineers) and multiple enterprise deployments shows:

![Speed of Delivery — Research-Backed Results](images/brief_speed_metrics_1784559416604.png)

### What This Looks Like For a Real Project

**Example: 5 developers building a new feature**

![Development Speed: Before vs After](images/table_speed_comparison_1784555449910.png)

### Projected Annual Value

![Projected Annual Return on Investment](images/table_roi_value_1784555475968.png)

---

## Cost Controls — No Surprise Bills

A common concern with AI tools is unpredictable costs. GitHub provides **hard spending limits** that guarantee costs stay within budget:

![Cost Controls — No Surprise Bills](images/brief_cost_controls_1784559423695.png)

It is **impossible** for costs to exceed these amounts with the cap enabled.

---

## Why Not Cursor AI? (The Other Option Being Discussed)

The team has also evaluated **Cursor AI** as an alternative. Here's the key issue:

![Copilot vs Cursor AI Comparison](images/table_copilot_vs_cursor_1784555483881.png)

**Cursor is a separate code editor.** It cannot run inside Visual Studio, which is the tool our entire engineering team uses every day. Adopting Cursor would require changing our development environment — a significantly more disruptive change.

**Copilot runs inside Visual Studio natively.** Developers don't change tools, don't learn a new editor, and don't disrupt their workflow.

---

## Risk Assessment

### What Could Go Wrong

![Risk Assessment — What Could Go Wrong](images/brief_risk_assessment_1784559430598.png)

### What Happens If We Do Nothing

![Risk of Doing Nothing](images/table_risk_inaction_1784555523425.png)

---

## The Migration Plan

The migration takes **10 weeks** and is designed to be **zero-risk**:

![10-Week Migration Plan](images/table_migration_plan_1784555489578.png)

---

## What Changes For the Engineering Team

![What Changes For the Engineering Team](images/brief_team_changes_1784559457696.png)

> **Visual Studio remains the IDE.** Developers keep their existing workflow, project files, and debugging tools. The change is in **how code is stored and reviewed**, not in how it's written.

---

## Decision Summary

![Decision Summary](images/table_decision_summary_1784555517960.png)

---

## Recommended Next Steps

![Recommended Next Steps](images/brief_next_steps_1784559463334.png)

---

> *Supporting documentation available:*
> - *[Technical Details — Full Report](DEP-CVS-to-GitHub-Migration-Detailed-Report.md) (94 KB, 17 sections)*
> - *[Technical Q&A — 65+ Questions Answered](DEP-Technical-QA-Team-Discussion.md)*
> - *[Interactive Diagrams](diagrams/) (Excalidraw)*
