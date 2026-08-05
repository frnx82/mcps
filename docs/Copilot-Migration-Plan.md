# GitHub Copilot Enterprise — Migration & Implementation Plan
## Prerequisites, Phase-by-Phase Rollout & Cost Estimation

> **For:** Engineering & Management Teams  
> **Date:** August 2026  
> **Scope:** Layer 1 — GitHub Copilot Enterprise for 50+ C++ developers  
> **Timeline:** 15-day demo → phased production rollout

---

## Table of Contents

1. [Two Scenarios — With GitHub vs With CVS](#1-two-scenarios)
2. [Prerequisites — What You Need Before Starting](#2-prerequisites)
3. [Phase 0: Demo in 15 Days (Proof of Concept)](#3-phase-0-demo-in-15-days)
4. [Phase 1: Foundation Setup (Weeks 1-2)](#4-phase-1-foundation-setup)
5. [Phase 2: Pilot Rollout (Weeks 3-4)](#5-phase-2-pilot-rollout)
6. [Phase 3: Full Migration — CVS to GitHub (Weeks 5-8)](#6-phase-3-full-migration)
7. [Phase 4: Full Copilot Rollout (Weeks 9-10)](#7-phase-4-full-copilot-rollout)
8. [Phase 5: Optimization & CVS Decommission (Weeks 11-12)](#8-phase-5-optimization)
9. [Cost Estimation — Enterprise + Consulting](#9-cost-estimation)
10. [Timeline Summary](#10-timeline-summary)
11. [Large C++ Repository — Migration Complexities & Build Infrastructure](#11-large-c-repository--migration-complexities--build-infrastructure)

---

## 1. Two Scenarios

### Scenario A: CVS → GitHub Migration + Copilot Enterprise (Recommended)

```
CURRENT STATE:                       TARGET STATE:
  CVS (source control)                 GitHub Enterprise Cloud (source control)
  Visual Studio 2022 (IDE)    →        Visual Studio 2022 + Copilot Enterprise
  Manual code reviews                  Copilot-powered PR reviews
  No CI/CD automation                  GitHub Actions CI/CD
```

**Why recommended:** Copilot PR reviews, code search, and codebase indexing only work with code on GitHub. Full value of the $39/user investment.

### Scenario B: Keep CVS + Add Copilot Enterprise (Partial Value)

```
CURRENT STATE:                       TARGET STATE:
  CVS (source control — kept)          CVS (unchanged)
  Visual Studio 2022 (IDE)    →        Visual Studio 2022 + Copilot Enterprise
  Manual code reviews                  Manual code reviews (unchanged)
```

**What works:** Inline completions, Copilot Chat, code generation — all work on LOCAL files regardless of source control.

**What doesn't work without GitHub:**
- ❌ Copilot PR code reviews (requires GitHub PRs)
- ❌ Copilot code search (requires GitHub-hosted repos)
- ❌ Codebase indexing (Enterprise feature, GitHub repos only)
- ❌ GitHub Actions CI/CD

**You get ~60% of Copilot's value with CVS vs ~100% with GitHub.**

> **Recommendation:** Start with Scenario B for the 15-day demo (zero migration risk), then proceed with Scenario A for full value.

---

## 2. Prerequisites — What You Need Before Starting

### Mandatory Prerequisites

| # | Prerequisite | Status | Who Owns It | Effort |
|---|---|---|---|---|
| 1 | **GitHub Enterprise Cloud account** | ☐ Pending | IT / Admin | 1 day |
| 2 | **GitHub Organization** created under Enterprise | ☐ Pending | IT / Admin | 1 hour |
| 3 | **Copilot Enterprise** licenses purchased (50+ seats at $39/user/mo) | ☐ Pending vendor pricing | Management | 1 day |
| 4 | **Visual Studio 2022 v17.8+** on all developer machines | ☐ Verify | IT / Desktop Support | 1-3 days |
| 5 | **GitHub accounts** for all 50+ developers | ☐ Pending | IT / Admin | 1 day |
| 6 | **SAML/SSO** identity provider configured (Azure AD, Okta, etc.) | ☐ Pending | IT Security | 2-3 days |
| 7 | **Management approval** for code in cloud (GitHub's Azure servers) | ☐ Pending | CISO / Management | Decision |
| 8 | **Content exclusion list** — which code directories to block from Copilot | ☐ Pending | Tech Lead | 1 day |
| 9 | **Network access** — developers can reach `github.com` and `copilot.github.com` | ☐ Verify | Network / Firewall team | 1 day |

### For Demo Only (Scenario B — CVS Stays)

| # | Prerequisite | Status | Who Owns It | Effort |
|---|---|---|---|---|
| 1 | GitHub Enterprise trial or paid account | ☐ Pending | Admin | 1 day |
| 2 | Copilot Enterprise license (5-10 seats for demo) | ☐ Pending | Admin | 1 day |
| 3 | Visual Studio 2022 17.8+ (5-10 developer machines) | ☐ Verify | IT | 1 day |
| 4 | GitHub accounts for demo participants | ☐ Pending | Admin | 1 hour |
| 5 | Sample C++ project (non-sensitive) for demo | ☐ Prepare | Tech Lead | 1 day |

### For Full Migration (Scenario A — CVS to GitHub)

| # | Additional Prerequisite | Status | Who Owns It | Effort |
|---|---|---|---|---|
| 10 | **CVS repository audit** — total size, number of modules, branch count, history depth | ☐ Pending | Consultant | 1-2 days |
| 11 | **cvs2git or cvs-fast-export** tool installed and tested | ☐ Pending | Consultant | 1 day |
| 12 | **Git training plan** for developers (CVS → Git workflow changes) | ☐ Pending | Consultant | 1 day |
| 13 | **Branch strategy** decision (trunk-based, GitFlow, or GitHub Flow) | ☐ Pending | Tech Lead + Consultant | Decision |
| 14 | **CI/CD requirements** documented (current build process) | ☐ Pending | Build Engineer | 1 day |
| 15 | **Parallel run window** agreed (how long CVS and GitHub run side-by-side) | ☐ Pending | Management | Decision |

---

## 3. Phase 0: Demo in 15 Days (Proof of Concept)

> **Goal:** Show management and developers that Copilot Enterprise works with their C++ CAE code in Visual Studio 2022. No migration required.

### Day 1-3: Setup

| Day | Task | Owner |
|---|---|---|
| 1 | Request GitHub Enterprise trial (or purchase) | Admin |
| 1 | Create GitHub org, enable Copilot Enterprise | Admin + Consultant |
| 2 | Create GitHub accounts for 5-10 demo participants | Admin |
| 2 | Assign Copilot Enterprise licenses to demo users | Admin |
| 3 | Install/verify Visual Studio 2022 17.8+ on demo machines | IT |
| 3 | Sign in to GitHub from Visual Studio, enable Copilot extension | Demo users |

### Day 4-5: Prepare Demo Environment

| Day | Task | Owner |
|---|---|---|
| 4 | Create a sample GitHub repo with representative C++ code | Consultant |
| 4 | Upload `copilot-instructions.md` with CAE-specific review rules | Consultant |
| 5 | Configure content exclusion for sensitive directories (if any) | Admin + Consultant |
| 5 | Test Copilot completions, chat, and review on sample code | Consultant |

### Day 6-10: Developer Trial

| Day | Task | Owner |
|---|---|---|
| 6-10 | 5-10 developers use Copilot on their daily C++ work | Demo users |
| 6-10 | Developers work on LOCAL files from CVS (no migration needed) | Demo users |
| 6-10 | Consultant collects feedback — what worked, what didn't | Consultant |
| 8 | Mid-trial check-in with team | Consultant |

### Day 11-13: Demonstrate Value

| Day | Task | Owner |
|---|---|---|
| 11 | Compile developer feedback and productivity observations | Consultant |
| 12 | Prepare demo presentation with before/after examples | Consultant |
| 13 | Create a sample PR on GitHub to show Copilot PR review capability | Consultant |

### Day 14-15: Management Presentation

| Day | Task | Owner |
|---|---|---|
| 14 | Present demo results to management | Consultant + Tech Lead |
| 15 | Go/No-Go decision for full rollout | Management |

### Demo Deliverables

- ✅ Working Copilot Enterprise in Visual Studio 2022
- ✅ Developer feedback report (5-10 developers, 5 days of usage)
- ✅ Sample `copilot-instructions.md` tailored for the C++ CAE codebase
- ✅ Copilot PR review demo on sample GitHub repo
- ✅ Security configuration demonstration (content exclusion, audit logs)
- ✅ Cost projection for 50+ developer full rollout

---

## 4. Phase 1: Foundation Setup (Weeks 1-2)

> **After demo approval.** Set up GitHub Enterprise and security controls.

| Week | Task | Owner | Deliverable |
|---|---|---|---|
| 1 | Purchase GitHub Enterprise Cloud (50+ seats) | Admin / Procurement | Active Enterprise account |
| 1 | Purchase Copilot Enterprise licenses (50+ seats) | Admin / Procurement | Licenses provisioned |
| 1 | Configure SAML/SSO integration | IT Security | SSO login working |
| 1 | Set up Enterprise Managed Users (if chosen) | IT / Admin | Managed user accounts |
| 2 | Create GitHub organization structure (teams, repos) | Consultant | Org configured |
| 2 | Configure content exclusion policies | Admin + Tech Lead | Sensitive paths excluded |
| 2 | Enable audit logging | Admin | Audit trail active |
| 2 | Set organization-wide Copilot policies | Admin | Policies enforced |

---

## 5. Phase 2: Pilot Rollout — Copilot on CVS (Weeks 3-4)

> **All 50+ developers get Copilot.** Code stays on CVS. No migration yet.

| Week | Task | Owner | Deliverable |
|---|---|---|---|
| 3 | Install VS 2022 Copilot extension on all developer machines | IT + Developers | All devs connected |
| 3 | Deploy `copilot-instructions.md` with C++ CAE rules | Consultant | Review rules active |
| 3 | Deploy path-specific instruction files (solver, mesh, IO) | Consultant | Module rules active |
| 3 | Developer training session (1 hour) — Copilot basics | Consultant | Team trained |
| 4 | Monitor usage, collect feedback | Consultant | Usage report |
| 4 | Tune copilot-instructions based on developer feedback | Consultant | Optimized rules |
| 4 | Address issues and edge cases | Consultant | Issues resolved |

> At this point, all developers have Copilot working on their LOCAL C++ files from CVS. Inline completions, chat, and code generation are fully functional. PR reviews are NOT available yet (need GitHub).

---

## 6. Phase 3: Full Migration — CVS to GitHub (Weeks 5-8)

> **The big migration.** CVS history is converted to Git and pushed to GitHub.

### Week 5: CVS Audit & Preparation

| Task | Owner | Deliverable |
|---|---|---|
| Full CVS repository audit (modules, size, branch count) | Consultant | Audit report |
| Identify CVS modules to migrate (priority order) | Tech Lead + Consultant | Migration priority list |
| Install and test cvs2git / cvs-fast-export | Consultant | Tool ready |
| Define Git branch strategy (GitHub Flow recommended) | Consultant + Tech Lead | Branch strategy doc |
| Set up GitHub repos (one per CVS module or monorepo) | Consultant | Repos created |

### Week 6: Migration Execution (Non-Production First)

| Task | Owner | Deliverable |
|---|---|---|
| Convert first CVS module to Git (with full history) | Consultant | First repo migrated |
| Validate history, branches, tags are correct | Consultant + Tech Lead | Validation report |
| Push to GitHub, set up branch protection rules | Consultant | Protected main branch |
| Set up CODEOWNERS file | Tech Lead | Review assignments |
| Create PR template with checklist | Consultant | PR template ready |

### Week 7: Migration Execution (Remaining Modules)

| Task | Owner | Deliverable |
|---|---|---|
| Convert remaining CVS modules to Git | Consultant | All repos migrated |
| Set up GitHub Actions CI/CD (MSBuild + tests) | Consultant | CI pipeline active |
| Configure Copilot PR reviews on migrated repos | Consultant | PR reviews enabled |
| Developer training session (1 hour) — Git workflow, PRs | Consultant | Team trained on Git |

### Week 8: Parallel Run & Validation

| Task | Owner | Deliverable |
|---|---|---|
| Parallel run: developers commit to both CVS and GitHub | All developers | Dual-commit workflow |
| Validate builds work from GitHub (MSBuild via Actions) | Consultant + Build Engineer | Build validated |
| Test Copilot PR reviews on real PRs | Developers | PR reviews working |
| Address migration issues | Consultant | Issues resolved |

---

## 7. Phase 4: Full Copilot Rollout (Weeks 9-10)

> **Copilot now has full power** — PR reviews, codebase indexing, search.

| Week | Task | Owner | Deliverable |
|---|---|---|---|
| 9 | Enable codebase indexing (Enterprise feature) | Admin | Indexing active |
| 9 | All developers switch primary source to GitHub | All developers | CVS → GitHub cutover |
| 9 | Copilot PR review training session | Consultant | Team trained |
| 10 | Monitor full-stack usage (completions + chat + PR reviews) | Consultant | Usage dashboard |
| 10 | Tune content exclusion and review rules based on real PRs | Consultant | Optimized config |
| 10 | Knowledge transfer to internal admin | Consultant | Admin self-sufficient |

---

## 8. Phase 5: Optimization & CVS Decommission (Weeks 11-12)

| Week | Task | Owner | Deliverable |
|---|---|---|---|
| 11 | Final CVS sync — ensure all commits are in GitHub | Consultant | Sync verified |
| 11 | Set CVS to read-only | Admin | CVS locked |
| 11 | Productivity report — before vs after metrics | Consultant | ROI report |
| 12 | CVS archive (keep backup for compliance) | Admin | CVS archived |
| 12 | Project close, final documentation | Consultant | Project complete |

---

## 9. Cost Estimation

### GitHub Enterprise + Copilot Licensing

| Item | Per User/Month | 50 Users/Month | Annual (50 users) |
|---|---|---|---|
| GitHub Enterprise Cloud | $21 | $1,050 | $12,600 |
| Copilot Enterprise | $39 | $1,950 | $23,400 |
| **Total licensing** | **$60** | **$3,000** | **$36,000** |

> ⚠️ Pricing under negotiation with vendor. Volume discounts may apply for 50+ seats.

### Demo Phase Licensing (15 Days, 10 Users)

| Item | 10 Users × 1 Month | Notes |
|---|---|---|
| GitHub Enterprise Cloud | $210 | 1 month trial or paid |
| Copilot Enterprise | $390 | 10 seats × $39 |
| **Demo phase total** | **$600** | One-time for 15-day demo |

### Total Project Cost — Year 1

| Cost Category | Demo Only | Demo + Copilot (CVS stays) | Full Package (Migration + Copilot) |
|---|---|---|---|
| **GitHub Enterprise licensing** | $210 (1 mo, 10 users) | $12,600/year (50 users) | $12,600/year |
| **Copilot Enterprise licensing** | $390 (1 mo, 10 users) | $23,400/year (50 users) | $23,400/year |
| **Total Year 1** | **$600** | **$36,000** | **$36,000** |
| **Ongoing annual (Year 2+)** | — | $36,000 (licensing only) | $36,000 (licensing only) |

> ⚠️ Migration execution costs (tooling, CI/CD setup, training) are separate and depend on whether internal teams or external support handles the work.

### Cost Per Developer Per Month

| Scenario | Monthly/Dev | Annual/Dev |
|---|---|---|
| Demo only (10 devs) | $60 (licensing) | $720 |
| Copilot on CVS (50 devs) | $60 (licensing) | $720 |
| Full migration (50 devs) | $60 (licensing) | $720 |

---

## 10. Timeline Summary

```
AGGRESSIVE TIMELINE — 14 WEEKS TOTAL

Week  0         Demo Prep ░░░
Week  1-2       PHASE 0: 15-Day Demo ████████████████
                ↓ Management Go/No-Go Decision
Week  3-4       PHASE 1: Foundation ████████
Week  5-6       PHASE 2: Copilot on CVS ████████
Week  7-10      PHASE 3: CVS → GitHub Migration ████████████████
Week  11-12     PHASE 4: Full Copilot Rollout ████████
Week  13-14     PHASE 5: Optimization & Close ████████

KEY MILESTONES:
  Day 15:    Demo complete → Go/No-Go
  Week 6:    All 50 devs have Copilot (on CVS)
  Week 10:   All code on GitHub, PR reviews active
  Week 14:   CVS decommissioned, project complete
```

### If CVS Stays (No Migration)

```
SHORTER TIMELINE — 6 WEEKS

Week  0         Demo Prep ░░░
Week  1-2       PHASE 0: 15-Day Demo ████████████████
                ↓ Management Go/No-Go Decision
Week  3-4       PHASE 1: Foundation + Copilot Setup ████████
Week  5-6       PHASE 2: Full Rollout + Optimization ████████
                ↓ Done (but no PR reviews or code search)
```

---

## 11. Large C++ Repository — Migration Complexities & Build Infrastructure

> **This section addresses the real-world challenges of migrating a large C++ codebase with DLLs, libraries, and multi-platform build targets to GitHub.**

### 11.1 Repository Size — Limits & Constraints

GitHub has specific limits that affect large C++ projects:

| Limit | Value | Impact on Your Project |
|---|---|---|
| **Recommended repo size** | Under **1 GB** | Most C++ source code fits easily |
| **Soft cap (warnings)** | **5 GB** | GitHub may contact you to reduce size |
| **Individual file limit** | **100 MB** per file | DLLs and libraries MUST use Git LFS |
| **Git LFS free storage** | 1 GB storage + 1 GB bandwidth/month | Will be exceeded quickly with DLLs |
| **Git LFS paid** | $5/month per 50 GB storage + 50 GB bandwidth | Budget based on binary count |

### What Counts Toward Size

```
COUNTS toward repo size (keep in repo):
  ✅ C++ source files (.cpp, .h, .hpp)           → Small (typically < 500 MB total)
  ✅ Makefiles, CMakeLists.txt, .vcxproj          → Small (< 10 MB)
  ✅ Config files, scripts                         → Small (< 5 MB)

MUST use Git LFS (large binary files):
  ⚠️ Pre-built DLLs (.dll)                        → Can be 10-500 MB each
  ⚠️ Static libraries (.lib, .a)                  → Can be 50-200 MB each
  ⚠️ Shared libraries (.so)                       → Can be 10-100 MB each
  ⚠️ Debug symbols (.pdb)                         → Can be 100 MB+ each
  ⚠️ Third-party libraries                        → Can be 1 GB+ total

SHOULD NOT be in repo at all:
  ❌ Build output (.exe, .obj, .o)                 → Use GitHub Releases instead
  ❌ Intermediate files                             → Add to .gitignore
  ❌ Package manager cache (vcpkg, conan)           → Download during build
```

### 11.2 Git LFS — Handling DLLs and Libraries

**What is Git LFS?** Instead of storing large binary files directly in Git, LFS stores a small pointer file in the repo and keeps the actual file on a separate LFS server.

**Configuration (.gitattributes):**

```gitattributes
# Track all binary file types via Git LFS
*.dll filter=lfs diff=lfs merge=lfs -text
*.lib filter=lfs diff=lfs merge=lfs -text
*.a filter=lfs diff=lfs merge=lfs -text
*.so filter=lfs diff=lfs merge=lfs -text
*.pdb filter=lfs diff=lfs merge=lfs -text
*.exe filter=lfs diff=lfs merge=lfs -text
*.obj filter=lfs diff=lfs merge=lfs -text
*.o filter=lfs diff=lfs merge=lfs -text
```

**LFS Cost Estimate:**

| Binary Assets | Estimated Size | Monthly LFS Cost |
|---|---|---|
| 50 DLLs + libs (pre-built) | ~2 GB | $5 (50 GB pack covers this) |
| 100 DLLs + libs | ~5 GB | $5 (still within 50 GB) |
| 500+ DLLs + libs + PDBs | ~20 GB | $5-10 |
| Bandwidth (50 dev clones/week) | ~50-200 GB/month | $5-20 |
| **Total monthly LFS cost** | | **$10-30/month** |

### 11.3 Clone & Checkout Performance

**Will checkout/clone be slow with a large repo?**

| Operation | Small Repo (< 1 GB) | Large Repo (5-10 GB with LFS) | Mitigation |
|---|---|---|---|
| **First clone** | 30 seconds | **5-15 minutes** | Use shallow clone: `git clone --depth 1` |
| **Daily pull** | 1-5 seconds | **10-30 seconds** | Normal — only downloads changed files |
| **Switching branches** | Instant | **30-60 seconds** (if LFS files differ) | Use `git lfs fetch --recent` |
| **CI clone per build** | 15 seconds | **3-10 minutes** | Shallow clone + LFS selective fetch |

**Mitigations for slow clones:**

```
FOR DEVELOPERS:
  git clone --depth 1 https://github.com/your-org/morpher.git
  # Clones only latest commit — fast, skips full history
  
  git lfs pull --include="libs/needed/**"
  # Only download LFS files you actually need

FOR CI BUILDS:
  - uses: actions/checkout@v4
    with:
      lfs: false        # Skip LFS unless this job needs binaries
      fetch-depth: 1    # Shallow clone
```

> **Reality check:** Daily workflow (pull, edit, push) will NOT be noticeably slower than CVS for source code. The only slow operation is the **first clone** or cloning large LFS binaries.

### 11.4 Build Infrastructure — Cloud Runners vs Self-Hosted

#### Option A: GitHub-Hosted Cloud Runners

```
What GitHub provides:
  Windows: windows-latest (Windows Server 2022, 4 vCPU, 16 GB RAM)
  Linux:   ubuntu-latest (Ubuntu 22.04/24.04, 4 vCPU, 16 GB RAM)
  macOS:   macos-latest (macOS 14+, 3-4 vCPU, 14 GB RAM)

Included in Enterprise:
  ✅ 50,000 minutes/month (Linux)
  ✅ Equivalent Windows minutes (2x multiplier)
  ✅ Pre-installed: Visual Studio Build Tools, MSBuild, CMake, gcc, clang
```

| Pros | Cons |
|---|---|
| ✅ Zero setup — works immediately | ❌ 4 vCPU is SLOW for large C++ builds |
| ✅ Clean environment every build | ❌ No persistent cache — rebuilds everything |
| ✅ GitHub manages updates/patches | ❌ C++ build may take 30-60+ minutes |
| ✅ Scales automatically | ❌ Large repo clones consume bandwidth |
| | ❌ Custom toolchains/SDKs must be installed every run |

#### Option B: Self-Hosted Runners (Recommended for C++ Builds)

```
Your own machines running the GitHub Actions runner:
  Windows: Your build server with full Visual Studio 2022 installed
  Linux:   Your build server with gcc/clang toolchain

Setup (surprisingly easy):
  1. GitHub Org → Settings → Actions → Runners → New self-hosted runner
  2. Download runner package (single script)
  3. Run: ./config.sh --url https://github.com/your-org --token <TOKEN>
  4. Run: ./run.sh (or install as service)
  
  Total setup time: ~30 minutes per machine
```

| Pros | Cons |
|---|---|
| ✅ Full hardware control (16+ cores, 64 GB RAM) | ⚠️ You manage the machine |
| ✅ **Persistent cache** — incremental builds | ⚠️ You handle updates/patches |
| ✅ Pre-installed toolchains (no re-install per build) | ⚠️ Security: runner has network access |
| ✅ No bandwidth cost for LFS (local network) | ⚠️ Uptime is your responsibility |
| ✅ Build time: 5-15 min (vs 30-60 min cloud) | |
| ✅ **Existing build machines can become runners** | |

#### Recommendation

```
FOR YOUR C++ CAE PROJECT:

  ✅ Use SELF-HOSTED runners for builds
     → Use your existing build machines
     → Add GitHub Actions runner software (30 min setup)
     → Keep persistent cache for fast incremental builds
     → No need to download DLLs/libs every build
     
  ✅ Use GitHub-hosted runners for lightweight tasks
     → Linting, formatting checks, documentation
     → PR label automation
     → Tasks that don't need the full C++ toolchain
```

### 11.5 Build Pipeline Configuration — MSBuild & Makefiles

#### Windows Builds (.exe) with MSBuild

```yaml
# .github/workflows/build-windows.yml
name: Build Windows (.exe)
on: [push, pull_request]

jobs:
  build-windows:
    runs-on: self-hosted  # Your Windows build machine
    # runs-on: windows-latest  # OR use GitHub-hosted (slower)
    
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true         # Download DLLs/libs via LFS
          fetch-depth: 1    # Shallow clone for speed

      - name: Setup MSBuild
        uses: microsoft/setup-msbuild@v2

      - name: Restore NuGet packages (if used)
        run: nuget restore morpher.sln

      - name: Build Release
        run: msbuild morpher.sln /p:Configuration=Release /p:Platform=x64 /m
        # /m = parallel build (uses all cores)

      - name: Run Unit Tests
        run: ./build/Release/morpher_tests.exe --gtest_output=xml:test-results.xml

      - name: Upload Build Artifact
        uses: actions/upload-artifact@v4
        with:
          name: morpher-windows-x64
          path: build/Release/morpher.exe
```

#### Linux Builds with Make/CMake

```yaml
# .github/workflows/build-linux.yml
name: Build Linux Binary
on: [push, pull_request]

jobs:
  build-linux:
    runs-on: self-hosted  # Your Linux build machine
    # runs-on: ubuntu-latest  # OR use GitHub-hosted
    
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true
          fetch-depth: 1

      - name: Install dependencies
        run: sudo apt-get install -y build-essential cmake libboost-all-dev

      - name: Configure with CMake
        run: cmake -B build -S . -DCMAKE_BUILD_TYPE=Release

      - name: Build
        run: cmake --build build --config Release -j$(nproc)
        # -j$(nproc) = use all CPU cores

      - name: Run Tests
        run: cd build && ctest --output-on-failure

      - name: Upload Build Artifact
        uses: actions/upload-artifact@v4
        with:
          name: morpher-linux-x64
          path: build/morpher
```

#### Cross-Platform Matrix Build (Both in One Workflow)

```yaml
# .github/workflows/build-all.yml
name: Cross-Platform Build
on: [push, pull_request]

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: self-hosted-windows   # Your Windows runner label
            build-cmd: msbuild morpher.sln /p:Configuration=Release /p:Platform=x64 /m
            artifact-name: morpher-windows
            artifact-path: build/Release/morpher.exe
          - os: self-hosted-linux     # Your Linux runner label
            build-cmd: cmake -B build -S . -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc)
            artifact-name: morpher-linux
            artifact-path: build/morpher
    
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true
          fetch-depth: 1

      - name: Build
        run: ${{ matrix.build-cmd }}

      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.artifact-name }}
          path: ${{ matrix.artifact-path }}
```

### 11.6 How Hard Is Each Part?

| Task | Difficulty | Time | Notes |
|---|---|---|---|
| **CVS → Git history conversion** | 🟡 Medium | 1-3 days | Tools exist (cvs2git). May need cleanup |
| **Git LFS setup for DLLs/libs** | 🟢 Easy | 2-4 hours | Configure .gitattributes, push to LFS |
| **Self-hosted runner setup (Windows)** | 🟢 Easy | 30 min per machine | Download script, configure, run |
| **Self-hosted runner setup (Linux)** | 🟢 Easy | 30 min per machine | Same process |
| **MSBuild pipeline (Windows .exe)** | 🟡 Medium | 1-2 days | Map existing build steps to YAML |
| **CMake/Make pipeline (Linux)** | 🟡 Medium | 1-2 days | Map existing build steps to YAML |
| **Cross-platform matrix build** | 🟡 Medium | 1 day | Combine both into one workflow |
| **Copilot PR review on builds** | 🟢 Easy | 1 hour | Automatic once pipelines exist |
| **Branch protection (require CI pass)** | 🟢 Easy | 30 min | Settings → Branch rules |
| **Migrating custom build scripts** | 🔴 Hard | 3-5 days | Depends on complexity of existing scripts |
| **Handling build dependencies (vcpkg/conan)** | 🟡 Medium | 1-2 days | Set up package manager in pipeline |

### 11.7 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Repo too large (> 5 GB source)** | Low | High | Split into multiple repos or use Git submodules |
| **LFS bandwidth exceeded** | Medium | Low | Buy additional LFS packs ($5/50 GB) |
| **Cloud runner too slow for C++ builds** | High | Medium | Use self-hosted runners (recommended) |
| **MSBuild config differences (local vs CI)** | Medium | Medium | Pin toolset versions, use CMake Presets |
| **DLL dependency hell (missing at build time)** | Medium | High | Use vcpkg/conan, or cache DLLs on self-hosted runner |
| **CVS history conversion loses data** | Low | High | Validate before switching: compare file counts, diffs |
| **Developers unfamiliar with Git** | High | Medium | Training session (1-2 hours), cheat sheet |
| **Build times increase in CI** | Medium | Medium | Incremental builds on self-hosted, ccache for gcc |

### 11.8 Alternative: Keep Binaries Out of GitHub

If the DLL/library count is very large (100+ pre-built binaries), consider:

```
OPTION: Binary Artifact Server (Separate from GitHub)

  GitHub repo contains:
    ✅ C++ source code only (.cpp, .h, .hpp)
    ✅ Build scripts and configs
    ✅ CMakeLists.txt / .vcxproj files
    ❌ NO DLLs, NO .lib files, NO binaries

  Binary artifacts stored in:
    → Artifactory (JFrog)
    → Azure Artifacts
    → AWS S3
    → Network share (for self-hosted runners)

  Build pipeline:
    Step 1: Checkout source from GitHub
    Step 2: Download pre-built DLLs from artifact server
    Step 3: Build
    Step 4: Upload output (.exe / Linux binary) to GitHub Releases

  Benefits:
    ✅ GitHub repo stays small (< 1 GB)
    ✅ No LFS bandwidth costs
    ✅ Faster clones for developers
    ✅ Binaries versioned separately from source
```

---

> **Next step:** Complete prerequisites (Section 2), then kick off Phase 0 demo. The 15-day demo requires minimal licensing investment ($600) and gives management concrete evidence to approve the full rollout.
