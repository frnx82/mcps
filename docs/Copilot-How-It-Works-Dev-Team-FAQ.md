# GitHub Copilot — How It Works with Your Codebase
## FAQ for Development Team

> **Context:** These are answers to the development team's questions about how
> GitHub Copilot understands and uses existing code when generating suggestions.

---

## The Core Question

**"Does Copilot use our existing data structures, or does it write its own?"**

### Short answer:
**It does BOTH — and knowing WHEN it does each is critical to using it effectively.**

---

## How Copilot Builds Context

Copilot reads code in **layers of context**, from most to least aware:

```
Layer 1: Current File (STRONGEST context)
  ├── The file you're editing right now
  ├── All #includes, function signatures, variable names
  └── Copilot sees ALL of this → uses YOUR data structures ✅

Layer 2: Open Tabs (GOOD context)  
  ├── Other files open in your IDE
  ├── If you have MeshGenerator.h open, Copilot sees Point3D, Element, Mesh
  └── It will use these types in suggestions ✅

Layer 3: @workspace Index (Enterprise only — MODERATE context)
  ├── GitHub indexes your entire repository
  ├── Copilot Chat can search across all files
  └── But code completion only uses Layers 1-2

Layer 4: Training Data (WEAKEST — fallback)
  ├── General C++ patterns from public open-source code
  ├── Standard FEA/mesh algorithms from textbooks/papers
  └── This is what Copilot falls back to when it has no project context ⚠️
```

---

## The TODO Example — Explained

Let's analyze what happens when you prompt the TODO in `MeshRefinement.cpp`:

```cpp
// TODO: Create proper 8 sub-hex connectivity
```

**What Copilot sees (Layer 1 — current file):**
- `splitHex8()` function above the TODO
- `Point3D nodes[8]` — it knows there are 8 corner nodes
- `int center_id` — it knows there's a center node
- `int mid[12]` — it knows there are 12 edge midpoint nodes
- `refined_mesh->addElement(ElementType::HEX8, ...)` — it knows the API

**What Copilot sees (Layer 2 — open tabs):**
- If `MeshGenerator.h` is open → it sees `ElementType::HEX8`, `addElement()` signature
- If `MeshGenerator.cpp` is open → it sees `createBeam()` connectivity pattern

**What Copilot uses (Layer 4 — training data):**
- Standard hex8 subdivision algorithm from FEA textbooks
- The connectivity pattern `{n0, n1, n2, n3, n4, n5, n6, n7}` for hex8 is well-known

### Result:
```
Copilot generates hex8 connectivity using:
  ✅ YOUR variables: center_id, mid[], elem.node_ids[]
  ✅ YOUR API: refined_mesh->addElement(ElementType::HEX8, {...})
  ⚠️ GENERAL KNOWLEDGE: The actual connectivity pattern comes from
     standard FEA algorithms, not from your codebase
```

**This is the key insight:** Copilot uses YOUR data structures but may apply
GENERAL algorithms. For standard patterns (like hex subdivision), this is fine.
For YOUR COMPANY'S custom algorithms, it won't know the right approach.

---

## What This Means for a 20+ Year C++ Codebase

### Where Copilot is VERY effective (85% of code):

| Task | Why It Works |
|------|-------------|
| Boilerplate code | Getters, setters, constructors, operator overloads |
| File I/O | Reading CSV, XML, INP files — common patterns |
| Unit tests | It reads the function signature and generates test cases |
| Error handling | Try/catch blocks, validation logic |
| STL usage | Vectors, maps, algorithms — well-known patterns |
| Logging/debugging | Adding log statements, print functions |
| Refactoring | Converting raw pointers to smart pointers, range-based for loops |
| Documentation | Doxygen comments from function signatures |
| OpenMP/threading | Parallel patterns it's seen thousands of times |

### Where Copilot is LIMITED (15% of code):

| Task | Why It Struggles |
|------|-----------------|
| **Custom domain algorithms** | Your proprietary solver math, custom convergence criteria |
| **Cross-module dependencies** | Module A's data structures used deep inside Module B |
| **20-year legacy patterns** | Custom macros, company-specific coding conventions |
| **Business logic** | Why a specific tolerance is 1e-7 and not 1e-8 |
| **Architectural decisions** | Which module owns which data, lifecycle management |

---

## How to Maximize Effectiveness with a Large Codebase

### Strategy 1: Open relevant files in tabs

```
Before coding in solver/FEASolver.cpp, open:
  Tab 1: solver/FEASolver.h        ← Copilot sees your struct definitions
  Tab 2: mesh/MeshGenerator.h      ← Copilot sees Mesh, Element, Point3D
  Tab 3: utils/MathUtils.h         ← Copilot sees math function signatures

Now Copilot knows YOUR data structures and will use them.
```

### Strategy 2: Add context comments

```cpp
// Uses the existing SparseMatrix class (CSR format) from solver/SparseMatrix.h
// Must call addValue() for each entry, then finalize() before multiply()
void assembleLocalMatrix(int elem_id) {
    // ← Copilot now knows to use SparseMatrix::addValue(), not create its own
}
```

### Strategy 3: Use Copilot Chat with @workspace (Enterprise)

```
@workspace How does the MeshGenerator store element connectivity?
→ Copilot searches ALL files and shows you Element::node_ids, addElement(), etc.

@workspace What classes use SparseMatrix?
→ Copilot finds FEASolver, shows how it's assembled and solved
```

### Strategy 4: Create a .github/copilot-instructions.md file

This file tells Copilot about your project conventions:

```markdown
# Copilot Instructions for Our CAE Solver

## Data Structures
- Use `Point3D` for all 3D coordinates (not std::array or raw doubles)
- Use `SparseMatrix` (CSR format) for all sparse matrices
- Elements are stored as `Element` structs with `node_ids` connectivity

## Coding Conventions
- All classes use PascalCase (e.g., MeshRefinement)
- All member variables use m_ prefix (e.g., m_nodes)
- Use OpenMP for parallel loops in solver code
- Never use raw `new/delete` — use smart pointers

## Domain Rules
- Poisson's ratio must be in (0, 0.5) — reject 0.5 (incompressible)
- Always check Jacobian determinant > 0 in element computations
- Von Mises stress is used for yield checks, not Tresca
```

Copilot reads this file and follows these rules in its suggestions.

---

## Honest Assessment for Your Team

### What to tell developers:

> "Copilot is like a very fast junior developer who knows C++ extremely well
> but has never seen our codebase before.
>
> - Give it context (open tabs, comments) → it writes code using OUR structs
> - Don't give it context → it writes generic code that MAY not fit
>
> It will save significant time on the 85% of code that is standard C++.
> For the 15% that is our proprietary algorithms, it helps with syntax
> and boilerplate but the LOGIC still needs to come from our engineers."

### What to tell management:

> "Copilot accelerates development by handling routine coding tasks.
> It does NOT replace domain expertise. Our engineers still design
> the algorithms — Copilot helps implement them faster."

---

## Cross-Module Dependencies — The Real Challenge

For a 20-year codebase with modules like:

```
Module A: Solver Engine (uses custom matrix types)
Module B: Mesh Generator (uses custom element types)
Module C: GUI (uses both Module A and B types)
Module D: File I/O (reads/writes all data types)
```

**The challenge:** When editing Module D, Copilot may not know about
Module A's `SparseMatrix` or Module B's `MeshRefinement` unless those
headers are open in tabs or referenced in the current file's #includes.

**Solutions:**
1. **Open the relevant headers in tabs** before coding
2. **Use @workspace queries** to understand cross-module APIs
3. **Create the `.github/copilot-instructions.md`** with key type mappings
4. **Accept that Copilot suggestions need review** — just like code from
   any team member, Copilot's output must be reviewed by someone who
   understands the architecture

---

## Summary

| Question | Answer |
|----------|--------|
| Does Copilot use our data structures? | **Yes, if they're visible** (current file or open tabs) |
| Does it invent its own? | **Yes, if it has no context** — it falls back to general patterns |
| How to make it use ours? | Open relevant headers, add context comments, use @workspace |
| Is it effective for a large codebase? | **85% yes** (boilerplate, tests, standard C++), **15% limited** (custom algorithms) |
| Does it understand cross-module deps? | Only what it can see — open tabs + @workspace help significantly |
| Should we trust it blindly? | **Never** — always review, especially for solver/domain logic |

---

## Deep Dive: Layer 3 — Where is the Index Stored?

### The index is NOT the same as your Git repository

When GitHub indexes your code for @workspace, it creates **two separate things**:

```
┌──────────────────────────────────────────────────────────────────┐
│                    GitHub's Infrastructure                        │
│                                                                  │
│  ┌──────────────────────┐    ┌──────────────────────────────┐   │
│  │  Git Storage          │    │  Search Index (Embeddings)    │   │
│  │  (Your actual repo)   │    │  (Separate system)            │   │
│  │                       │    │                               │   │
│  │  • Source code files  │───▶│  • Vector embeddings of code  │   │
│  │  • Commit history     │    │  • Semantic search database   │   │
│  │  • Branches/tags      │    │  • Function/class mappings    │   │
│  │  • .git metadata      │    │  • NOT raw source code        │   │
│  │                       │    │  • Mathematical              │   │
│  │  Stored in: GitHub's  │    │    representations only       │   │
│  │  Git infrastructure   │    │                               │   │
│  │  (Azure data centers) │    │  Stored in: GitHub's search   │   │
│  └──────────────────────┘    │  infrastructure (separate      │   │
│                               │  from Git storage)             │   │
│                               └──────────────────────────────┘   │
│                                          │                        │
│                                          ▼                        │
│                           ┌──────────────────────────┐           │
│                           │  When you ask @workspace  │           │
│                           │  a question:              │           │
│                           │                           │           │
│                           │  1. Search index finds    │           │
│                           │     relevant files        │           │
│                           │  2. Raw code snippets     │           │
│                           │     from those files are  │           │
│                           │     sent to the LLM       │           │
│                           │  3. LLM generates answer  │           │
│                           │  4. Code snippets are     │           │
│                           │     DISCARDED (not stored) │           │
│                           └──────────────────────────┘           │
└──────────────────────────────────────────────────────────────────┘
```

### What exactly is stored where:

| What | Where | Retention |
|------|-------|-----------|
| **Your source code** (git repo) | GitHub Git storage (Azure) | Until you delete the repo |
| **Search index** (embeddings) | GitHub's search infrastructure (separate system) | Updated continuously, deleted if repo is deleted |
| **Code snippets sent to LLM** | Temporarily in memory during request | **Discarded immediately after response** — NOT stored |
| **Your prompts/questions** | Temporarily in memory during request | **NOT retained** (Enterprise guarantee) |
| **Copilot's responses** | Temporarily in memory | **NOT retained** after delivery |

### What are "embeddings"?

The search index doesn't store your raw source code. It stores **mathematical vectors** (embeddings):

```
Your code:
  void FEASolver::assemble() {
      for (int e = 0; e < num_elements; ++e) {
          computeElementStiffness(e, ke);
      }
  }

Becomes an embedding like:
  [0.234, -0.891, 0.456, 0.123, -0.567, ...]  (1536 floating point numbers)

This vector captures the MEANING of the code ("FEA assembly loop")
but you CANNOT reconstruct the original source code from the vector.
```

Think of it like a fingerprint — it identifies the content but you can't reconstruct
a person from their fingerprint.

**However:** When you actually ask a @workspace question, GitHub retrieves the
**original code** from the Git repo and sends relevant snippets to the LLM.
The embedding just helps FIND the right code — the LLM sees real code.

---

## Copilot Enterprise vs Claude Code — Data Handling Comparison

> **This is the most important section for your security team.**

### How each tool handles your code:

```
┌─────────────────────────────────────────────────────────────────┐
│                  GitHub Copilot Enterprise                        │
│                                                                  │
│  Developer types code                                            │
│       │                                                          │
│       ▼                                                          │
│  IDE sends current file + open tabs to GitHub/OpenAI LLM         │
│       │                                                          │
│       ▼                                                          │
│  LLM generates suggestion                                       │
│       │                                                          │
│       ▼                                                          │
│  Suggestion returned to developer                                │
│       │                                                          │
│       ▼                                                          │
│  ❌ Code snippets DISCARDED — not stored, not logged             │
│  ❌ NOT used for model training                                  │
│  ❌ NOT retained for any period                                  │
│                                                                  │
│  Retention: ZERO (Enterprise contractual guarantee)              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  Claude Code (Anthropic)                          │
│                                                                  │
│  Developer opens project in Claude Code                          │
│       │                                                          │
│       ▼                                                          │
│  Claude reads files from your local machine                      │
│       │                                                          │
│       ▼                                                          │
│  Code sent to Anthropic's API servers                            │
│       │                                                          │
│       ▼                                                          │
│  Claude generates response                                       │
│       │                                                          │
│       ▼                                                          │
│  ⚠️ DEFAULT: Prompts + code retained for UP TO 30 DAYS          │
│  ⚠️ Used for safety monitoring and abuse prevention              │
│  ⚠️ MAY be used for model improvement (unless opted out)         │
│                                                                  │
│  Retention: UP TO 30 DAYS (default)                              │
│  With Enterprise plan + ZDR: ZERO (must be negotiated)           │
└─────────────────────────────────────────────────────────────────┘
```

### Side-by-side comparison:

| Aspect | GitHub Copilot Enterprise | Claude Code (Default) | Claude Code (Enterprise + ZDR) |
|--------|--------------------------|----------------------|-------------------------------|
| **Where code is sent** | GitHub/OpenAI servers | Anthropic servers | Anthropic servers |
| **Code retention** | ❌ None (0 days) | ⚠️ Up to 30 days | ❌ None (0 days) |
| **Used for training?** | ❌ Never (contractual) | ⚠️ May be (default) | ❌ Never (contractual) |
| **Who sees your code?** | LLM only (no human review) | May be reviewed for safety | LLM only (no human review) |
| **Code lives on your machine?** | Code on GitHub servers (repo) | Code on your local machine | Code on your local machine |
| **Requires code on vendor servers?** | Yes (GitHub hosts the repo) | No (reads local files) | No (reads local files) |
| **Enterprise agreement needed?** | Yes (GitHub Enterprise) | Yes (Anthropic Enterprise) | Yes + Zero Data Retention add-on |
| **SOC 2 certified?** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Data Processing Agreement?** | ✅ Included | ✅ Available | ✅ Available |

### Key differences explained:

**1. Where your code physically lives:**

```
Copilot:  Your code is already ON GitHub's servers (it's a Git repo).
          Copilot reads from what's already there.
          
Claude:   Your code stays on YOUR machine/laptop.
          Claude reads local files and sends snippets to Anthropic's API.
```

**2. The 30-day retention issue with Claude:**

By default (without Enterprise plan), when Claude Code reads your file:
```
Your file: src/solver/FEASolver.cpp (500 lines)
          │
          ▼
Claude reads it → sends to Anthropic API
          │
          ▼
Anthropic stores the prompt (including your code) for up to 30 days
          │
          ▼
During those 30 days:
  - Anthropic MAY review it for safety/abuse
  - It MAY be used to improve models (unless opted out)
  - It is stored on Anthropic's servers
          │
          ▼
After 30 days: automatically deleted
```

**With Anthropic Enterprise + Zero Data Retention (ZDR):**
```
Your file → Claude reads → Anthropic API → Response generated → DISCARDED
                                              (zero retention, zero training)
```

**3. Which is safer for your company?**

| Scenario | Safer Option | Why |
|----------|-------------|-----|
| Code already on GitHub | **Copilot** | Code is already there, no additional exposure |
| Code only on local machines (not migrated yet) | **Claude + ZDR** | Code never leaves to a second vendor |
| Maximum contractual protection | **Both require Enterprise agreements** | Similar guarantees when properly configured |
| During the demo (mock code) | **Doesn't matter** | Mock code has no IP to protect |

### What to tell your security team:

> **For the demo:** We're using mock code — no security risk with either tool.
>
> **For production with Copilot Enterprise:**
> - Our code is already on GitHub (we chose to host it there)
> - Copilot reads from what's already there — no additional exposure
> - Enterprise agreement guarantees: zero retention, zero training
> - This is contractually binding and auditable (SOC 2)
>
> **If we also want Claude Code for production:**
> - Must get Anthropic Enterprise plan with Zero Data Retention (ZDR)
> - Without ZDR, code snippets are retained for 30 days — NOT acceptable
> - With ZDR, same guarantees as Copilot Enterprise

---

## Model vs Product: Does Claude "See" Our Code Through Copilot?

> **Developer question:** "If Copilot uses Claude models to write code on our data
> structures, does that mean Claude/Anthropic gets access to read our code?"

### Short answer:
**Yes, Anthropic's servers process your code when Copilot routes to a Claude model.
BUT — GitHub's Enterprise contract governs the data handling, NOT Anthropic's
default terms. Zero retention, zero training.**

### The data flow when Copilot uses Claude:

```
Your code in VS Code
     │
     ▼
GitHub Copilot Extension (IDE plugin)
     │
     ▼
GitHub's API Gateway (GitHub controls this)
     │
     ├──▶ Route to OpenAI GPT-4o     ← GitHub's default model
     ├──▶ Route to Anthropic Claude   ← If you selected Claude in Copilot settings
     └──▶ Route to Google Gemini      ← If you selected Gemini
     │
     ▼
Selected model processes your code → returns suggestion
     │
     ▼
GitHub's API Gateway receives response
     │
     ▼
Suggestion appears in your IDE
```

### What is a "Model" vs a "Product"?

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  "Claude" the MODEL (the brain/engine)                           │
│  ──────────────────────────────────────                          │
│  • An AI engine that processes text and code                     │
│  • Can be embedded INSIDE other products (like Copilot)          │
│  • Like an Intel chip inside a Dell laptop — Intel makes         │
│    the chip, Dell makes the laptop, you buy from Dell            │
│  • When used inside Copilot: Anthropic is a SUBPROCESSOR         │
│    under GitHub's contract                                       │
│                                                                  │
│                         vs                                       │
│                                                                  │
│  "Claude Code" the PRODUCT (the tool)                            │
│  ────────────────────────────────────                            │
│  • Anthropic's own standalone coding tool                        │
│  • You interact with Anthropic DIRECTLY                          │
│  • Like buying a computer directly from Intel                    │
│  • Anthropic's own terms of service apply                        │
│  • Default: 30-day data retention                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### The "Engine in a Car" Analogy

```
GitHub Copilot = The car you bought
Claude Sonnet  = One of several engines available in that car

When you drive the car (use Copilot):
  • You have a contract with GitHub (the car manufacturer)
  • GitHub installed the Claude engine and has its OWN contract
    with Anthropic (the engine maker)
  • GitHub's contract says: "Don't record where the driver goes,
    don't use their driving data for anything"
  • The engine DOES process your driving (code), but:
    ❌ Does NOT store it
    ❌ Does NOT use it for training
    ❌ Does NOT share it with anyone
  • If Anthropic violates this → GitHub is liable to YOU

Claude Code = Buying the engine directly from Anthropic
  • You have a contract with Anthropic directly
  • Anthropic's default terms: "We record your trips for 30 days"
  • You CAN negotiate zero recording (Enterprise + ZDR)
  • But YOU must negotiate it yourself
```

### The contractual chain:

```
┌──────────────────────────────────────────────────────────┐
│ Using Claude model THROUGH Copilot:                      │
│                                                          │
│  You ←──contract──▶ GitHub ←──subprocessor──▶ Anthropic  │
│       (Enterprise        (GitHub's contract              │
│        Agreement)         prohibits retention)            │
│                                                          │
│  • GitHub is the DATA PROCESSOR                          │
│  • Anthropic is a SUB-PROCESSOR                          │
│  • GitHub is accountable for Anthropic's compliance      │
│  • Your code: ZERO retention, ZERO training              │
│  • Anthropic is listed on GitHub's subprocessor list:    │
│    https://github.com/subprocessors                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ Using Claude Code DIRECTLY:                              │
│                                                          │
│  You ←──contract──▶ Anthropic                            │
│       (Anthropic's                                       │
│        Terms of Service)                                 │
│                                                          │
│  • Anthropic is the DATA PROCESSOR (directly)            │
│  • Default: UP TO 30 DAYS retention                      │
│  • Default: MAY use for model improvement                │
│  • Enterprise + ZDR: zero retention (must be negotiated) │
└──────────────────────────────────────────────────────────┘
```

### Side-by-side: Three scenarios compared

| Aspect | Copilot + OpenAI model | Copilot + Claude model | Claude Code (standalone) |
|--------|----------------------|----------------------|------------------------|
| **Code sent to** | OpenAI servers | Anthropic servers | Anthropic servers |
| **Contract governs** | GitHub Enterprise | GitHub Enterprise | Anthropic ToS |
| **Who is accountable** | GitHub | GitHub | Anthropic |
| **Retention** | Zero | Zero | 30 days (default) |
| **Training** | Never | Never | May be (default) |
| **Can admin control?** | ✅ Can block this model | ✅ Can block this model | N/A (separate product) |
| **Subprocessor relationship** | OpenAI is GitHub's subprocessor | Anthropic is GitHub's subprocessor | Anthropic is primary |

### Admin Controls: Restricting Which Models Copilot Uses

If your security team does NOT want any code going to Anthropic (even through Copilot),
you can restrict it:

**Steps:**
1. Go to: `https://github.com/enterprises/depusa/settings/copilot`
2. Find: **"Model selection"** or **"Model policy"**
3. Options:
   - **Allow all models** — developers can choose GPT-4o, Claude, Gemini
   - **Restrict to specific models** — e.g., only GPT-4o (OpenAI)
   - **Block specific models** — e.g., block Claude, allow everything else
4. Save the policy

**This means:**
```
Security team says: "We only trust OpenAI, not Anthropic"
  → Admin restricts Copilot to GPT-4o only
  → No code ever goes to Anthropic's servers
  → Developers can still use Copilot, just with one model

Security team says: "We trust all GitHub subprocessors"
  → Admin allows all models
  → Developers can choose the best model for their task
```

### What to tell your developer:

> "When Copilot uses Claude as a model, yes — Anthropic's servers process our code
> temporarily. But there are two key protections:
>
> 1. **Contractual:** GitHub's Enterprise agreement with Anthropic prohibits
>    retention and training. Anthropic is a subprocessor under GitHub's terms,
>    not their own default 30-day retention terms.
>
> 2. **Technical:** As admins, we can restrict Copilot to use only specific
>    models. If we don't want code going to Anthropic at all, we block Claude
>    models and only allow OpenAI GPT-4o.
>
> This is very different from using Claude Code directly, where Anthropic's
> default terms (30-day retention) apply unless we negotiate an Enterprise plan."

---

## Updated Summary

| Question | Answer |
|----------|--------|
| Does Copilot use our data structures? | **Yes, if they're visible** (current file or open tabs) |
| Does it invent its own? | **Yes, if it has no context** — it falls back to general patterns |
| How to make it use ours? | Open relevant headers, add context comments, use @workspace |
| Is it effective for a large codebase? | **85% yes** (boilerplate, tests, standard C++), **15% limited** (custom algorithms) |
| Does it understand cross-module deps? | Only what it can see — open tabs + @workspace help significantly |
| Should we trust it blindly? | **Never** — always review, especially for solver/domain logic |
| Where is the @workspace index stored? | Separate from Git repo — vector embeddings on GitHub's search infra |
| Is raw code stored in the index? | **No** — embeddings only. But real code IS sent to LLM during queries |
| Does Copilot retain our code? | **No** — Enterprise guarantees zero retention after response |
| Does Claude Code retain our code? | **Default: 30 days.** Enterprise + ZDR: zero retention |
| Which is safer? | Both are safe WITH Enterprise agreements. Without Enterprise, Copilot is safer (zero retention by default) |
| Does Claude "see" code through Copilot? | **Yes, temporarily** — but under GitHub's contract (zero retention), not Anthropic's default terms |
| Can we block Claude in Copilot? | **Yes** — admins can restrict to specific models (e.g., GPT-4o only) |
| What's the difference: model vs product? | **Model in Copilot** = GitHub's contract governs. **Claude Code standalone** = Anthropic's contract governs |
