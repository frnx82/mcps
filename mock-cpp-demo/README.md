# CAE Solver Demo — Mock C++ Project for GitHub Copilot Enterprise Demo

> **Purpose:** This is a mock C++ CAE (Computer-Aided Engineering) project designed
> to demonstrate GitHub Copilot Enterprise capabilities. It mimics the structure
> of a real FEA solver application without containing any proprietary code.

## Project Structure

```
mock-cpp-demo/
├── CMakeLists.txt              ← Top-level CMake build
├── include/
│   ├── solver/
│   │   ├── FEASolver.h         ← Finite Element Analysis solver
│   │   └── SparseMatrix.h      ← Sparse matrix for large systems
│   ├── mesh/
│   │   ├── MeshGenerator.h     ← Mesh generation algorithms
│   │   └── MeshRefinement.h    ← Adaptive mesh refinement
│   └── utils/
│       ├── MathUtils.h         ← Math utility functions
│       └── Logger.h            ← Logging framework
├── src/
│   ├── solver/
│   │   ├── FEASolver.cpp       ← Solver implementation
│   │   └── SparseMatrix.cpp    ← CSR sparse matrix
│   ├── mesh/
│   │   ├── MeshGenerator.cpp   ← 2D/3D mesh generation
│   │   └── MeshRefinement.cpp  ← Refinement algorithms
│   ├── utils/
│   │   ├── MathUtils.cpp       ← Vector/matrix math
│   │   └── Logger.cpp          ← Thread-safe logger
│   ├── io/
│   │   └── ModelReader.cpp     ← File I/O for CAE models
│   └── main.cpp                ← Application entry point
├── tests/
│   ├── unit/
│   │   ├── test_solver.cpp     ← Solver unit tests
│   │   └── test_mesh.cpp       ← Mesh unit tests
│   └── integration/
│       └── test_pipeline.cpp   ← End-to-end test
├── .github/
│   └── workflows/
│       └── ci.yml              ← GitHub Actions CI pipeline
├── docs/
│   └── architecture.md         ← Architecture overview
├── .gitignore
├── CODEOWNERS                  ← Auto-assign PR reviewers
└── README.md
```

## Building

```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --parallel
ctest --output-on-failure
```

## Key Demo Scenarios for GitHub Copilot Enterprise

> **Setup:** Each developer needs the Copilot extension installed in their IDE
> (VS Code or JetBrains). Ensure Copilot is enabled for the org in GitHub settings.

---

### Scenario 1: Code Completion (Ghost Text)

**Goal:** Show Copilot suggesting context-aware C++ code as you type.

**Steps:**

1. Open `src/solver/FEASolver.cpp`
2. Navigate to the bottom of the file (after `computeReactions`)
3. Start typing a new method:
   ```cpp
   void FEASolver::exportResults(const std::string& filename, const SolverResult& result) {
   ```
4. **Watch:** Copilot will suggest the full method body — file I/O, CSV formatting,
   displacement/stress output — all contextually aware of the `SolverResult` struct.
5. Press `Tab` to accept, or `Esc` to dismiss.

**What to highlight for stakeholders:**
- Copilot understands the `SolverResult` struct fields (displacements, stresses, etc.)
- It generates domain-appropriate code (scientific notation, proper column headers)
- Saves 5-10 minutes of boilerplate writing

**Bonus demo:** Open `src/mesh/MeshRefinement.cpp`, find the `TODO` comment in
`splitHex8()` (line ~170). Place your cursor after `// TODO: Create proper 8 sub-hex connectivity`
and press Enter. Copilot will suggest the hex8→8 hex8 splitting connectivity.

---

### Scenario 2: Copilot Chat — Explain Code

**Goal:** Show Copilot understanding and explaining complex C++ code.

**Steps:**

1. Open `src/solver/FEASolver.cpp`
2. Select the `conjugateGradient()` method (lines ~230-300)
3. Open Copilot Chat (Ctrl+Shift+I in VS Code)
4. Type: **"Explain this Conjugate Gradient solver. What is the preconditioner doing?"**
5. Copilot will explain:
   - The CG algorithm steps (r, p, α, β updates)
   - Jacobi preconditioner (diagonal scaling)
   - Convergence criteria
   - OpenMP parallelization strategy

**More prompts to try:**

| Prompt | Expected Response |
|--------|-------------------|
| "What's the time complexity of assemble()?" | O(elements × DOF²) explanation |
| "Is there a memory leak in FEASolver?" | PIMPL cleanup analysis |
| "Why do we use the penalty method for Dirichlet BCs?" | Explains penalty vs elimination approach |
| "What happens if Poisson's ratio is exactly 0.5?" | Explains incompressibility and matrix singularity |

---

### Scenario 3: Copilot Chat — Generate Tests

**Goal:** Show Copilot generating unit tests from existing code.

**Steps:**

1. Open `include/utils/MathUtils.h`
2. Select the `vonMisesStress()` function signature
3. Open Copilot Chat and type: **"Generate comprehensive unit tests for this function, including edge cases"**
4. Copilot will generate tests for:
   - Pure uniaxial stress (σ_vm = |σ₁₁|)
   - Pure shear (σ_vm = √3 × τ)
   - Hydrostatic pressure (σ_vm = 0)
   - Biaxial stress state
   - Zero stress (σ_vm = 0)
5. Copy the generated tests into `tests/unit/test_solver.cpp`

**Bonus:** Select `computeElasticityMatrix()` and ask:
**"Write a test that verifies D is symmetric and positive definite"**

---

### Scenario 4: Copilot Chat — Fix Bugs

**Goal:** Show Copilot finding and fixing bugs.

**Steps:**

1. Open `src/mesh/MeshGenerator.cpp`
2. In `createBeam()`, temporarily introduce a bug — change:
   ```cpp
   int n2 = n0 + (nx + 1) + 1;
   ```
   to:
   ```cpp
   int n2 = n0 + (nx + 1);  // BUG: wrong connectivity
   ```
3. Select the `createBeam()` function
4. Ask Copilot Chat: **"Review this function for bugs in the hex8 element connectivity"**
5. Copilot will identify the wrong connectivity and suggest the fix

---

### Scenario 5: PR Review with Copilot

**Goal:** Show Copilot auto-reviewing pull requests on GitHub.

**Steps:**

1. Create a branch:
   ```bash
   git checkout -b feature/optimize-sparsity
   ```
2. Open `src/solver/SparseMatrix.cpp` and make some changes:
   - Add a method `void SparseMatrix::transpose()`
   - Intentionally use `malloc` instead of `new` (Copilot should flag this)
   - Add a loop with a potential off-by-one error
3. Commit, push, and open a PR on GitHub
4. **Watch:** Copilot will automatically review and comment:
   - Style issues (malloc vs new/vector)
   - Potential bugs (off-by-one, missing bounds checks)
   - Suggestions for improvement

**What to highlight:**
- Review happens automatically — no manual trigger needed
- Comments appear inline on the exact lines of code
- Saves senior engineers' time on routine code review

---

### Scenario 6: Copilot Chat — Explain Architecture

**Goal:** Show Copilot understanding the full codebase (Enterprise-only feature).

**Steps:**

1. Open Copilot Chat
2. Ask: **"@workspace How does the FEA solver assemble the global stiffness matrix from element stiffness matrices?"**
3. Copilot will explain the full flow across multiple files:
   - `FEASolver::assemble()` → loops over elements
   - `computeElementStiffness()` → Gauss quadrature + B-matrix
   - `SparseMatrix::addValue()` → triplet assembly
   - `SparseMatrix::finalize()` → CSR conversion

**More @workspace prompts:**

| Prompt | Shows |
|--------|-------|
| "@workspace What element types are supported?" | Cross-file enum search |
| "@workspace How are boundary conditions applied?" | Multi-file flow tracing |
| "@workspace Where would I add a new material model?" | Architecture understanding |
| "@workspace Find all TODO comments" | Codebase-wide search |

---

### Scenario 7: Code Completion — OpenMP Patterns

**Goal:** Show Copilot suggesting parallel patterns for C++.

**Steps:**

1. Open `src/solver/SparseMatrix.cpp`
2. Navigate to `multiplySymmetric()` method
3. Add a comment above the outer loop:
   ```cpp
   // Parallelize with OpenMP, using atomic for thread-safe accumulation
   ```
4. Watch Copilot suggest the correct `#pragma omp` directives with
   `atomic` for the symmetric contribution `y[j] += v * x[i]`

---

### Scenario 8: Documentation Generation

**Goal:** Show Copilot generating documentation.

**Steps:**

1. Open `include/mesh/MeshGenerator.h`
2. Place cursor above `class MeshGenerator`
3. Type `/**` and press Enter
4. Copilot will generate a Doxygen comment block with:
   - Class description
   - Usage example
   - Thread safety notes

**Bonus:** Select the entire `MeshRefinement.h` file and ask Chat:
**"Generate a markdown architecture document for this component"**

---

### Demo Script Summary (15-minute demo)

| Time | Scenario | Feature Demonstrated |
|------|----------|---------------------|
| 0-3 min | Scenario 1 | Code Completion (ghost text) |
| 3-6 min | Scenario 2 | Copilot Chat — explain code |
| 6-8 min | Scenario 3 | Copilot Chat — generate tests |
| 8-10 min | Scenario 6 | @workspace — architecture questions |
| 10-13 min | Scenario 5 | PR Review (pre-prepared PR) |
| 13-15 min | Q&A | Open floor for developer questions |

> **Tip:** Pre-record Scenarios 5 (PR Review) since it requires a push + PR + wait.
> Show the recording during the live demo while the audience watches.

---

## License

This is sample/demo code for GitHub Copilot Enterprise evaluation.
Contains NO proprietary code — safe for use on GitHub trial organizations.

