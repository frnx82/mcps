# GitHub Copilot for C++ CAE Development
## Code Review, IDE Integration, AI Models & Cost Guide

> **For:** Detroit Engineered Products — Engineering & Management Teams  
> **Product:** Morpher (C++ Computer-Aided Engineering Desktop Application)  
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
11. [Complete copilot-instructions.md for Morpher](#11-complete-copilot-instructionsmd-for-morpher)

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

Since Morpher likely uses significant TMP for performance:

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

> **Important nuance for DEP:** The 19% slowdown finding applies to senior engineers verifying AI output on complex, mature codebases — exactly the Morpher scenario. This is temporary (2–4 weeks) and is offset by massive gains in boilerplate, testing, and documentation. The net effect over 3+ months is strongly positive.

---

## 7. Available AI Models & Their Capabilities

### Models Accessible in Copilot (Visual Studio 2022)

Developers can switch between models using the **model picker** dropdown in Copilot Chat:

![Available AI Models in Copilot for C++](images/cpp_ai_models_1784556857252.png)

### Token Pricing Per Model

![Token Pricing Per Model](images/cpp_token_pricing_1784560131745.png)

### Which Model to Use for What (C++ Recommendation)

![Which Model to Use for What — C++ Recommendation](images/cpp_model_recommend_1784560138309.png)

---

## 8. Copilot Plans — Business vs Enterprise

### Feature Comparison

![Copilot Business vs Enterprise](images/cpp_business_vs_enterprise_1784556923931.png)

### Recommendation for DEP

![Cost Analysis — 50 Developers, All Scenarios](images/cpp_cost_scenarios_1784560145920.png)

> **Recommendation:** Start with **Copilot Business** ($19/user). Upgrade specific teams to Enterprise later if codebase indexing proves valuable. The core review and completion features are identical between plans.

---

## 9. Cost Analysis — 50 Developers, High Usage

### Base Subscription Cost


> This is the **minimum guaranteed cost**. Code completions are unlimited and free beyond this.

### What "High Usage Per Day" Looks Like


### Cost Scenarios for 50 Developers

Not all 50 developers will be heavy users. Realistic distribution:


### Annual Cost Summary — High Usage


### With Spending Cap ($0 Overage)


### Daily Cost Per Developer


### The $50K Question

![Annual Cost — 50 Developers, All Scenarios](images/cpp_cost_50_devs_1784556931600.png)

---

## 10. Setting Up Copilot Review Rules for C++ Apps

### Repository Configuration Structure

Copilot reads review rules from files in the `.github/` directory of your repository:

```
Morpher/
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

## 11. Complete copilot-instructions.md for Morpher

Below is a **ready-to-use** `copilot-instructions.md` file tailored for a complex C++ CAE application like Morpher. Place this in `.github/copilot-instructions.md`:

```markdown
# Copilot Instructions — Morpher (DEP)

## Project Overview
Morpher is a C++ desktop application for Computer-Aided Engineering (CAE),
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
- Morpher uses OpenMP for parallelization
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


### Models — Which to Use When


---

> *This document is part of the DEP migration documentation suite. See also:*
> - *[CEO Briefing](GITHUB-Briefing-Migration-Proposal.md)*
> - *[Technical Details — Full Report](DEP-CVS-to-GitHub-Migration-Detailed-Report.md)*
> - *[Technical Q&A — 65+ Questions](DEP-Technical-QA-Team-Discussion.md)*
> - *[Executive Summary](DEP-Executive-Summary-Team-Presentation.md)*
