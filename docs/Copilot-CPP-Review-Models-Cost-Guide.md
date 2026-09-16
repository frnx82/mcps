# GitHub Copilot for C++ CAE Development
## Code Review, IDE Integration, AI Models & Cost Guide

> **For:** the organization — Engineering & Management Teams  
> **Product:** the application (C++ Computer-Aided Engineering Desktop Application)  
> **Date:** July 2026  
> **Focus:** Copilot capabilities for complex C++ code, review rules, models, and costs

---

## Table of Contents

1. [What Types of Code Reviews Can Copilot Perform?](#1-what-types-of-code-reviews-can-copilot-perform)
2. [How Complex Can Copilot's C++ Reviews Get?](#2-how-complex-can-copilots-c-reviews-get)
3. [Copilot Review for CAE-Specific C++ Code](#3-copilot-review-for-cae-specific-c-code)
4. [VC++ Compiler vs Copilot — What's the Difference?](#4-vc-compiler-vs-copilot--whats-the-difference)
5. [Copilot Integration with Visual C++ IDE](#5-copilot-integration-with-visual-c-ide)
6. [Developer Productivity Benefits](#6-developer-productivity-benefits)
7. [Available AI Models & Their Capabilities](#7-available-ai-models--their-capabilities)
8. [Copilot Plans — Business vs Enterprise](#8-copilot-plans--business-vs-enterprise)
9. [Cost Analysis — 50 Developers, High Usage](#9-cost-analysis--50-developers-high-usage)
10. [Setting Up Copilot Review Rules for C++ Apps](#10-setting-up-copilot-review-rules-for-c-apps)
11. [Complete copilot-instructions.md for the application](#11-complete-copilot-instructionsmd-for-morpher)

---

## 1. What Types of Code Reviews Can Copilot Perform?

Copilot reviews pull requests automatically when a developer pushes code. It reads the code changes (the "diff") and posts review comments — exactly like a human reviewer would.

### Review Categories Copilot Handles Well

![Code Review Categories — What Copilot Handles](images/cpp_review_categories_1784556839793.png)

### Review Categories That Require Human Reviewers

![Review Categories That Require Human Reviewers](images/cpp_human_review_1784560004348.png)

---

## 2. How Complex Can Copilot's C++ Reviews Get?

### Complexity Levels — Honest Assessment

![Copilot Review Complexity — Honest Assessment](images/cpp_complexity_levels_1784556849472.png)

### Template Metaprogramming — Detailed Breakdown

Since the application likely uses significant TMP for performance:

![Template Metaprogramming — Copilot Capability](images/cpp_tmp_breakdown_1784560010517.png)

---

## 3. Copilot Review for CAE-Specific C++ Code

### What Copilot CAN Catch in CAE Code

Even though Copilot doesn't understand physics, it catches **software engineering issues** within CAE code:

![What Copilot Catches in CAE Code — By Module](images/cpp_cae_modules_1784560018608.png)

### Example: Copilot Reviewing a Stiffness Matrix Function

```cpp
// Developer submits this in a Pull Request:
void AssembleStiffnessMatrix(Element* pElem, double* K, int nDof) {
    double* Ke = new double[nDof * nDof];  // Local element stiffness
    
    for (int i = 0; i < nDof; i++) {
        for (int j = 0; j < nDof; j++) {
            Ke[i * nDof + j] = ComputeKe(pElem, i, j);
            K[pElem->GetDof(i) * nDof + pElem->GetDof(j)] += Ke[i * nDof + j];
        }
    }
    // Function ends without freeing Ke
}
```

**Copilot would flag:**

![Copilot Review Comments on Stiffness Matrix Code](images/cpp_copilot_comments_1784560048134.png)

**Copilot would NOT flag:**
- Whether the stiffness matrix formula `ComputeKe()` is mathematically correct
- Whether the DOF mapping `pElem->GetDof(i)` produces a valid global index
- Whether the element stiffness is symmetric (as it should be in structural analysis)

---

## 4. VC++ Compiler vs Copilot — What's the Difference?

This is the most common question: **"Our VC++ compiler already catches errors — why do we need Copilot?"**

The short answer: **The compiler catches code that won't run. Copilot catches code that runs but is wrong.**

### The Fundamental Difference

![VC++ Compiler vs Copilot — The Fundamental Difference](images/cpp_compiler_vs_copilot_1784556794925.png)

### Side-by-Side: Same Code, Different Catches

Here's a realistic C++ function. Let's see what each tool catches:

```cpp
void ProcessElements(std::vector<Element*>& elements, double* results)
{
    double* temp = new double[1000];

    for (int i = 0; i <= elements.size(); i++)  // Bug: off-by-one
    {
        Element* pElem = elements[i];
        double val = pElem->ComputeValue();
        results[i] = val;
        
        if (val > 100.0)
        {
            return;  // Bug: memory leak — temp never freed
        }
        
        if (pElem->GetType() == 3)
        {
            delete pElem;  // Bug: deleting from vector without removing
        }
        
        sprintf(temp, "Element %d: %f", i, val);  // Bug: type mismatch (temp is double*, not char*)
    }
    
    delete temp;  // Bug: should be delete[], not delete
}
```

### What Each Tool Catches — Side by Side

![Same Code — What Each Tool Catches](images/cpp_what_compiler_catches_1784556801958.png)

### The Complete Comparison Table

![Complete Comparison — Compiler vs Copilot vs Static Analysis](images/cpp_complete_comparison_1784560057415.png)

### Three Layers of Error Detection

![Three Layers of Error Detection](images/cpp_three_layers_1784556808825.png)

### Real-World Impact

![Real-World Impact — Compiler Only vs Compiler + Copilot](images/cpp_real_world_impact_1784556939487.png)

### What About VS Static Analysis?

Visual Studio has a built-in Static Analysis tool (`/analyze` flag). Here's how it fits:

![VS Static Analysis vs Copilot](images/cpp_static_analysis_1784560063166.png)

> **They are not competing tools — they are complementary layers.** The compiler catches won't-run code, static analysis catches some won't-work-right code, and Copilot catches won't-work-well code plus suggests improvements. Use all three together.

---

## 5. Copilot Integration with Visual C++ IDE

### Supported Visual Studio Versions

![Supported Visual Studio Versions](images/cpp_vs_versions_1784560090283.png)

### All Copilot Features Available in Visual Studio C++

![All Copilot Features in Visual Studio C++](images/cpp_vs_features_1784556980363.png)

### How Copilot Works Alongside Existing VS Features

![How Copilot Works Alongside Existing VS Features](images/cpp_vs_alongside_1784560098155.png)

---

## 6. Developer Productivity Benefits

### What Changes in a Developer's Daily Workflow

![Developer Productivity — Time Saved Per Task](images/cpp_productivity_gains_1784556971831.png)

### Productivity Impact — Research Data

![Productivity Impact — Research Data](images/cpp_research_data_1784560104723.png)

> **Important nuance for your organization:** The 19% slowdown finding applies to senior engineers verifying AI output on complex, mature codebases — exactly this scenario. This is temporary (2–4 weeks) and is offset by massive gains in boilerplate, testing, and documentation. The net effect over 3+ months is strongly positive.

---

## 7. Available AI Models & Their Capabilities

### Models Accessible in Copilot (Visual Studio 2022)

Developers can switch between models using the **model picker** dropdown in Copilot Chat:

![Available AI Models in Copilot for C++](images/cpp_ai_models_1784556857252.png)

### AI Credits Billing Model (Effective June 2026)

> **Key Change:** As of June 1, 2026, GitHub transitioned from flat "premium request" billing to **usage-based billing** via **GitHub AI Credits**. 1 AI Credit = $0.01 USD.

#### What Consumes Credits vs. What's Unlimited

| Feature | Consumes Credits? | Details |
|---|---|---|
| **Code completions** (inline autocomplete) | ❌ **No — Unlimited** | Free on all paid plans, no limits |
| **Next Edit Suggestions** | ❌ **No — Unlimited** | Free on all paid plans |
| **Copilot Chat** | ⚠️ **Yes** | Each chat message consumes tokens |
| **Agent Mode** (multi-step agentic coding) | ⚠️ **Yes — Heavy** | Can be 10-1,000× more tokens than chat |
| **Copilot Code Review** (PR reviews) | ⚠️ **Yes** | Each review consumes tokens |
| **Copilot Cloud Agent** | ⚠️ **Yes — Heavy** | Autonomous sessions are expensive |
| **Copilot CLI** | ⚠️ **Yes** | Command-line interactions |

### Token Pricing Per Model

Credits are consumed based on actual **tokens processed** (input + output + cached). Different models have different rates:

| Model Category | Example Models | Input ($/1M tokens) | Output ($/1M tokens) | Relative Cost |
|---|---|---|---|---|
| **Lightweight** | GPT-5 mini, Claude Haiku | ~$0.25 | ~$2.00 | 💚 Cheapest |
| **Versatile** | GPT-4o/5.4, Claude Sonnet | ~$2.50 | ~$15.00 | 🟡 Moderate |
| **Powerful** | GPT-5.3 Codex | ~$1.75 | ~$14.00 | 🟠 Moderate-High |
| **Ultra-Premium** | Claude Opus, o3 | Higher | Higher | 🔴 Most Expensive |

> **Note:** Cached input tokens are significantly discounted (e.g., GPT-5 mini cached: $0.025/1M vs $0.25/1M standard). Using "auto model selection" may qualify for a 10% discount.

![Token Pricing Per Model](images/cpp_token_pricing_1784560131745.png)

### Typical Credit Consumption Per Activity

| Activity | Typical Token Usage | Approx Credit Cost | Notes |
|---|---|---|---|
| Simple chat question | ~1K-3K tokens | ~$0.01-0.05 | "How do I use std::variant?" |
| Code explanation (1 file) | ~5K-15K tokens | ~$0.05-0.30 | "Explain this function" |
| PR code review | ~10K-50K tokens | ~$0.10-1.00 | Depends on PR size |
| Agent mode (simple) | ~50K-200K tokens | ~$0.50-3.00 | Fix a bug, write a test |
| Agent mode (complex) | ~500K-2M+ tokens | ~$1.00-10.00+ | Multi-file refactoring |
| Cloud agent (autonomous) | ~1M-5M+ tokens | ~$5.00-50.00+ | Repository-wide tasks |

### Which Model to Use for What (C++ Recommendation)

| Task | Recommended Model | Why |
|---|---|---|
| Routine chat, quick answers | **Lightweight** (GPT-5 mini) | Fastest, cheapest — preserves credits |
| Code review, standard C++ | **Versatile** (GPT-4o, Claude Sonnet) | Good balance of quality vs. cost |
| Complex TMP, solver logic | **Powerful/Ultra-Premium** (Claude Opus, o3) | Best reasoning for complex C++ |
| Boilerplate, getters/setters | **Lightweight** | Don't waste credits on simple tasks |
| Multi-file refactoring | **Versatile** | Good enough for structural changes |
| Understanding legacy code | **Ultra-Premium** | Large context + deep reasoning needed |

![Which Model to Use for What — C++ Recommendation](images/cpp_model_recommend_1784560138309.png)

---

## 8. Copilot Plans — Business vs Enterprise

### Feature Comparison

![Copilot Business vs Enterprise](images/cpp_business_vs_enterprise_1784556923931.png)

### Monthly AI Credit Allowances Per Plan

| Plan | Monthly Price | Included AI Credits/User | Credit $ Value | Key Additions Over Lower Plan |
|---|---|---|---|---|
| **Free** | $0 | Limited | Very limited | Basic completions only |
| **Pro** | $10 | 1,500 | $15.00 | Unlimited completions + chat |
| **Pro+** | $39 | 7,000 | $70.00 | Higher credit allowance |
| **Max** | $100 | 20,000 | $200.00 | Highest individual allowance |
| **Business** | $19/user | 1,900/user | $19.00/user | Org management, **pooled credits** |
| **Enterprise** | $39/user | 3,900/user | $39.00/user | + codebase indexing, policy controls, knowledge bases |

> **Pooled Credits (Business & Enterprise):** Individual seat credits are **pooled** at the organization level. A team of 50 developers shares the total monthly allowance, allowing power users to draw more credits while lighter users offset that consumption.

### Recommendation

![Cost Analysis — 50 Developers, All Scenarios](images/cpp_cost_scenarios_1784560145920.png)

> **Recommendation:** Start with **Copilot Business** ($19/user). Upgrade specific teams to Enterprise later if codebase indexing proves valuable. The core review and completion features are identical between plans.

> **Important Note:** GitHub Enterprise license ($21/user/month) is **separate** from Copilot subscription. Total Enterprise stack = $21 (GitHub Enterprise) + $39 (Copilot Enterprise) = **$60/user/month**.

---

## 9. Cost Analysis — 50 Developers, AI Credits & Overage

### Base Subscription Cost

| Plan | Per User/Mo | 50 Users/Mo | Annual | Included Credit Pool |
|---|---|---|---|---|
| **Copilot Business** | $19 | $950 | **$11,400** | 95,000 credits ($950 value) |
| **Copilot Enterprise** | $39 | $1,950 | **$23,400** | 195,000 credits ($1,950 value) |

> This is the **minimum guaranteed cost**. Code completions are unlimited and free beyond this. The credit pool covers Chat, Agent Mode, Code Review, and other metered features.

### What "High Usage Per Day" Looks Like

| Activity | Frequency | Daily Credits | Monthly Credits |
|---|---|---|---|
| Code completions | Continuous | **0** (unlimited) | **0** |
| Chat questions | 10-15/day | ~50-150 | ~1,000-3,000 |
| PR reviews | 1-2/day | ~20-200 | ~400-4,000 |
| Agent mode (simple) | 2-3/day | ~100-900 | ~2,000-18,000 |
| Agent mode (complex) | 1/day | ~100-1,000+ | ~2,000-20,000+ |

### Cost Scenarios for 50 Developers

Not all 50 developers will be heavy users. Realistic distribution:

| Usage Profile | % of Devs | Devs | Credits/User/Mo | Total Credits |
|---|---|---|---|---|
| **Light** (completions + occasional chat) | 40% | 20 | ~500 | 10,000 |
| **Moderate** (daily chat + weekly agent) | 40% | 20 | ~2,500 | 50,000 |
| **Heavy** (daily agent + PR reviews) | 15% | 7-8 | ~5,000 | 37,500 |
| **Power** (continuous agentic workflows) | 5% | 2-3 | ~10,000+ | 25,000+ |
| | | **Total** | | **~122,500** |

With Copilot Business pool of 95,000 credits → **~27,500 credits overage** (~$275/month).

### Annual Cost Summary — All Scenarios

| Scenario | Base Cost | Monthly Overage | Annual Overage | **Total Annual** | Per Dev/Year |
|---|---|---|---|---|---|
| **Conservative** (mostly completions) | $11,400 | $0 | $0 | **$11,400** | $228 |
| **Moderate** (regular chat + some agent) | $11,400 | ~$300 | ~$3,600 | **~$15,000** | ~$300 |
| **Heavy** (frequent agent mode) | $11,400 | ~$800 | ~$9,600 | **~$21,000** | ~$420 |
| **Aggressive agentic** (all devs daily agent) | $11,400 | ~$1,500+ | ~$18,000+ | **~$29,400+** | ~$588+ |
| **Hard cap ($0 overage)** | $11,400 | $0 | $0 | **$11,400** | $228 |

### With Spending Cap ($0 Overage)

```
With hard cap enabled:
  ✅ Code completions — STILL WORK (unlimited, always)
  ✅ Next Edit Suggestions — STILL WORK (unlimited, always)
  ❌ Copilot Chat — BLOCKED when credits exhausted
  ❌ Agent Mode — BLOCKED when credits exhausted
  ❌ PR Code Review — BLOCKED when credits exhausted
  ❌ Cloud Agent — BLOCKED when credits exhausted

Key insight: The features developers use MOST (completions)
             are never affected by credit limits.
```

### Overage Charges — How They Work

```
Scenario 1: NO spending cap set (⚠️ risky)
  Month starts → 95,000 pooled credits
  Day 15 → Credits exhausted
  Day 16-30 → Usage CONTINUES at per-token rates
  End of month → Overage billed to organization

Scenario 2: Hard spending cap ($0 overage)
  Month starts → 95,000 pooled credits
  Day 15 → Credits exhausted
  Day 16-30 → Chat/Agent/Review BLOCKED
  ✅ Completions still work (unlimited)
  End of month → No surprise bill

Scenario 3: Budget cap with limit (e.g., $500/month max overage)
  Month starts → 95,000 pooled credits
  Day 15 → Credits exhausted
  Day 16-25 → Overage accrues (up to $500)
  Day 26 → Cap hit → Chat/Agent/Review BLOCKED
  ✅ Completions still work (unlimited)
  End of month → Predictable $500 overage
```

### Admin Budget Controls — Preventing Surprise Bills

| Control | What It Does | Hard Stop? |
|---|---|---|
| **AI Credits Paid Usage Policy** | Master switch: disable to block ALL overage | **Yes (if disabled)** |
| **Enterprise/Org Budget** | Cap total org overage spend | **Only if "Stop usage" is enabled** |
| **Universal User-Level Budget (ULB)** | Cap per-individual consumption | **Yes (always)** |

**Configuration Steps:**

1. Go to: `Enterprise Settings → Billing → GitHub Copilot`
2. **AI Credits Paid Usage Policy** → DISABLE to block all overage (safest start)
3. If allowing overage, set an **Org Budget** with a dollar limit
   - ⚠️ **MUST enable "Stop usage when budget limit is reached"** — if disabled, it only notifies!
4. Set **Universal User-Level Budget** → default per-user cap (e.g., 3,000 credits/month)
   - Override individually for power users who need higher limits

### Recommended Strategy

```
Month 1-2: HARD CAP ($0 overage)
  → Measure actual usage patterns across the team
  → Identify who are the heavy vs. light users
  → Annual cost: $11,400 (fixed, predictable)

Month 3+: SET A REASONABLE OVERAGE BUDGET
  → Based on actual data, set $300-500/month overage limit
  → Set per-user budgets (ULBs) to prevent one user draining the pool
  → Review monthly usage reports by user, model, and repository

Ongoing: OPTIMIZE
  → Encourage lightweight models for routine tasks
  → Reserve frontier models (Opus, o3) for complex C++ reasoning
  → Use "auto model selection" for potential 10% discount
  → Estimated steady-state: $15,000-21,000/year for 50 devs
```

### The Bottom Line

![Annual Cost — 50 Developers, All Scenarios](images/cpp_cost_50_devs_1784556931600.png)

> **For management:** The $19/user subscription covers unlimited code completions — the feature developers use most. Chat and agentic features consume AI Credits from a monthly pool. With a hard spending cap, cost is fixed at **$11,400/year**. With moderate usage allowing overage, expect **$15,000-21,000/year**. Budget controls give you full visibility and hard stops.

---

## 10. Setting Up Copilot Review Rules for C++ Apps

### Repository Configuration Structure

Copilot reads review rules from files in the `.github/` directory of your repository:

```
the application/
├── .github/
│   ├── copilot-instructions.md          ← Global review rules (all files)
│   ├── instructions/
│   │   ├── cpp-standards.instructions.md ← C++ specific rules
│   │   ├── solver.instructions.md        ← Solver module rules
│   │   ├── mesh.instructions.md          ← Mesh module rules
│   │   └── io.instructions.md            ← I/O module rules
│   ├── CODEOWNERS                        ← Who must approve what
│   ├── pull_request_template.md          ← PR template with checklist
│   └── workflows/
│       └── pr-checks.yml                 ← CI pipeline
├── src/
│   ├── solver/
│   ├── mesh/
│   ├── ui/
│   └── io/
└── ...
```

### How Path-Specific Rules Work

You can apply **different review rules to different modules**:

```markdown
<!-- File: .github/instructions/solver.instructions.md -->
---
applyTo: "src/solver/**"
---

# Solver Module — Copilot Review Rules

When reviewing code in the solver module:
- Flag any use of `float` — all solver computations MUST use `double`
- Ensure all matrix operations check for singularity before inversion
- Verify that convergence criteria are explicitly defined
- Flag any hardcoded tolerance values — use named constants
- Ensure all solver iterations have a maximum iteration guard
```

```markdown
<!-- File: .github/instructions/mesh.instructions.md -->
---
applyTo: "src/mesh/**"
---

# Mesh Module — Copilot Review Rules

When reviewing code in the mesh module:
- Verify element connectivity arrays are properly bounds-checked
- Flag any direct memory allocation for nodes — use the NodePool allocator
- Ensure all mesh modification operations maintain mesh integrity
- Check that element quality metrics are validated after mesh operations
```

### How to Enable Review Rules

![How to Enable Copilot Review Rules](images/cpp_review_setup_1784560176835.png)

### Supported Configuration Files

Copilot also reads from these files if they exist:


---

## 11. Complete copilot-instructions.md for the application

Below is a **ready-to-use** `copilot-instructions.md` file tailored for a complex C++ CAE application like the application. Place this in `.github/copilot-instructions.md`:

```markdown
# Copilot Instructions — the application (the organization)

## Project Overview
the application is a C++ desktop application for Computer-Aided Engineering (CAE),
including finite element analysis, mesh generation, and optimization.
Built with Visual C++ (MSVC), targeting Windows x64.
Codebase is 20+ years old with a mix of legacy C++ and modern C++17 patterns.

## Language & Compiler
- Language: C++17 (targeting MSVC 2022 toolset v143)
- Build system: MSBuild (.sln / .vcxproj)
- Platform: Windows x64 only
- DO NOT suggest CMake, Makefile, or gcc/clang-specific syntax

## Memory Management Rules
- ALWAYS prefer `std::unique_ptr` over raw `new`
- ALWAYS prefer `std::shared_ptr` when ownership is shared
- NEVER use `malloc`/`free` in C++ code — use `new`/`delete` only as last resort
- Flag any raw `new` that is not immediately wrapped in a smart pointer
- Flag any `delete` in destructors — should use RAII instead
- Flag any missing virtual destructor in base classes

## Threading & Parallelism
- the application uses OpenMP for parallelization
- ALWAYS verify shared variables in `#pragma omp parallel` blocks
- Flag any shared mutable state accessed without `#pragma omp critical` or `omp_lock_t`
- Flag any non-thread-safe STL container access in parallel regions
- Prefer `#pragma omp parallel for reduction` over manual accumulation

## Naming Conventions
- Classes: PascalCase (e.g., `MeshGenerator`, `StiffnessMatrix`)
- Member functions: PascalCase (e.g., `ComputeStiffness()`)
- Member variables: `m_` prefix (e.g., `m_nodeCount`, `m_pElement`)
- Local variables: camelCase (e.g., `nodeIndex`, `totalForce`)
- Constants: ALL_CAPS_SNAKE (e.g., `MAX_ITERATIONS`, `DEFAULT_TOLERANCE`)
- Pointer members: `m_p` prefix (e.g., `m_pMesh`, `m_pSolver`)
- Boolean members: `m_b` prefix (e.g., `m_bConverged`, `m_bInitialized`)

## Code Style
- Braces: Allman style (opening brace on new line)
- Indentation: Tabs (not spaces)
- Max line length: 120 characters
- Always use `override` keyword on virtual function overrides
- Always use `const` correctness (const methods, const parameters)
- Prefer `enum class` over plain `enum`
- Prefer `nullptr` over `NULL` or `0`

## Error Handling
- NEVER use empty catch blocks — always log or rethrow
- Use structured exception handling for file I/O operations
- Validate all pointer arguments at function entry
- Check return values of Win32 API calls
- Use `assert()` for debug-mode invariant checks
- Use `static_assert` for compile-time checks where possible

## Performance Rules
- Flag unnecessary object copies (prefer move semantics or const reference)
- Flag `std::vector::push_back` in loops without prior `reserve()`
- Flag virtual function calls in tight computational loops
- Prefer `std::array` over C-style arrays for fixed-size data
- Prefer pre-increment (`++i`) over post-increment (`i++`) for iterators
- Flag `std::endl` — use `'\n'` instead (avoids unnecessary flush)

## Security Rules
- Flag any hardcoded file paths — use configuration or `std::filesystem`
- Flag any use of `sprintf` — use `snprintf` or `std::format`
- Flag any unchecked buffer operations
- Never commit credentials, API keys, or internal server paths

## Numerical Computing (CAE-Specific)
- All floating-point computations in solver code MUST use `double`, not `float`
- Flag any comparison of floating-point values using `==` — use tolerance-based comparison
- Flag any division without zero-check guard
- Note: DO NOT attempt to verify mathematical/physical correctness of FEA formulations
- Note: DO NOT suggest alternative algorithms for solver or mesh operations

## Documentation Requirements
- All public functions MUST have a documentation comment with:
  - `@brief` — one-line description
  - `@param` — for each parameter
  - `@return` — for non-void functions
  - `@throws` — if function can throw
- All classes MUST have a class-level documentation comment
- Complex algorithms SHOULD reference the relevant paper or textbook

## What NOT to Review
- Do not comment on mathematical formulations in solver code
- Do not suggest architectural changes to core modules
- Do not suggest replacing custom allocators with standard ones
- Do not suggest changing the build system from MSBuild
- Focus on code safety, maintainability, and C++ best practices
```

### Additional Path-Specific Rules Example

```markdown
<!-- File: .github/instructions/solver.instructions.md -->
---
applyTo: "src/solver/**"
---

# Solver Module Rules

Additional rules for the FEA solver module:

## Strict Requirements
- All matrix operations MUST check for dimension compatibility
- Symmetric matrices MUST only store upper/lower triangle
- Iterative solvers MUST have a maximum iteration count
- Convergence tolerance MUST be a named constant, not a magic number
- All solver entry points MUST validate input data before computation

## Performance Critical
- Inner loops MUST NOT allocate memory — pre-allocate all working arrays
- Sparse matrix operations MUST use CSR/CSC format, not dense
- Flag any `std::map` usage — use `std::unordered_map` or sorted vectors
```

```markdown
<!-- File: .github/instructions/io.instructions.md -->
---
applyTo: "src/io/**"
---

# I/O Module Rules

Additional rules for file import/export:

## File Safety
- ALL file operations MUST use RAII file handles
- Check file existence before opening for read
- Validate file headers/magic numbers before parsing
- Handle partial reads gracefully (don't crash on truncated files)
- ALL file paths MUST use `std::filesystem::path`, not raw strings

## Format Validation
- Validate ALL user-supplied data dimensions against file header claims
- Flag any `fscanf` or `fread` without error checking
- Binary file I/O MUST handle endianness
```

---

## Summary — Quick Reference

### What Copilot Does Best for C++ CAE

![Quick Reference — Copilot for C++ CAE](images/cpp_quick_ref_1784560183171.png)

### Cost at a Glance (50 Developers)

| Scenario | Annual Cost | Per Dev/Year | Notes |
|---|---|---|---|
| Copilot Business, hard cap | **$11,400** | $228 | Completions unlimited; chat/agent blocked when credits out |
| Copilot Business, moderate use | **~$15,000-21,000** | ~$300-420 | Recommended: set $300-500/mo overage budget |
| Copilot Enterprise, hard cap | **$23,400** | $468 | 2× credits + codebase indexing |
| Full stack (GitHub $21 + Copilot Ent $39) | **$36,000** | $720 | GitHub Enterprise + Copilot Enterprise |

### Models — Which to Use When

| Task | Model Tier | Credit Impact |
|---|---|---|
| Quick chat questions, boilerplate | **Lightweight** (GPT-5 mini) | 💚 Minimal |
| Code review, standard C++ | **Versatile** (Claude Sonnet, GPT-4o) | 🟡 Moderate |
| Complex TMP, solver debugging | **Ultra-Premium** (Claude Opus, o3) | 🔴 Heavy |
| Agent mode refactoring | **Versatile** | 🟡 Moderate per step, but many steps |


---

> *This document is part of the the migration documentation suite. See also:*
> - *[CEO Briefing](GITHUB-Briefing-Migration-Proposal.md)*
> - *[Technical Details — Full Report](CVS-to-GitHub-Migration-Detailed-Report.md)*
> - *[Technical Q&A — 65+ Questions](Technical-QA-Team-Discussion.md)*
> - *[Executive Summary](Executive-Summary-Team-Presentation.md)*
