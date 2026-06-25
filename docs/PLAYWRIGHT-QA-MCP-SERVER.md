# Playwright QA MCP Server

> **AI-Powered QA Testing with FastMCP + Playwright**
> An MCP (Model Context Protocol) server that enables AI agents to perform automated browser testing through natural language instructions.

---

## Table of Contents

- [Overview](#overview)
- [Benefits](#benefits)
- [Architecture](#architecture)
- [Tool Catalog](#tool-catalog)
- [Implementation Guide](#implementation-guide)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [FAQ](#faq)

---

## Overview

### What Is It?

The **Playwright QA MCP Server** is a bridge between AI agents (Gemini, Claude, etc.) and the Playwright browser automation framework. It exposes browser testing capabilities as MCP **tools** that an AI agent can invoke to:

- Navigate web applications
- Interact with UI elements (click, type, select)
- Assert expected behavior (text visible, URL correct, no errors)
- Capture evidence (screenshots, videos, network logs)
- Generate test reports

### Why Build This?

Traditional QA automation requires writing and maintaining test scripts. This MCP server lets QA teams **describe tests in natural language** and have an AI agent execute them via Playwright — dramatically lowering the barrier to test creation and maintenance.

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| MCP Framework | [FastMCP](https://github.com/jlowin/fastmcp) (Python) | MCP server scaffolding |
| Browser Engine | [Playwright](https://playwright.dev/python/) | Cross-browser automation |
| Transport | stdio / SSE | Agent ↔ Server communication |
| Reporting | HTML / JSON | Test result output |

---

## Benefits

### 1. 🗣️ Natural Language Testing
QA engineers and non-technical stakeholders can describe tests in plain English. The AI agent translates intent into tool calls.

```
"Go to the login page, enter admin/password123, click Sign In, 
 and verify the dashboard loads with the welcome message."
```

### 2. 🔄 Zero Test Script Maintenance
No Selenium/Playwright scripts to maintain. When the UI changes, the AI adapts its approach rather than breaking on hardcoded selectors.

### 3. 🌐 Cross-Browser Testing Out of the Box
Playwright supports **Chromium, Firefox, and WebKit** — test on all three with a single tool call.

### 4. 📸 Built-in Evidence Collection
Every test can automatically capture:
- Full-page screenshots
- Session recordings (video)
- Network request logs (HAR)
- Console error logs
- Accessibility audit results

### 5. 🔗 Seamless CI/CD Integration
Run the MCP server as a sidecar in your pipeline. AI agents can execute smoke tests post-deployment and report results to Slack, Jira, or dashboards.

### 6. 🧪 Exploratory Testing
AI agents can **explore** your application, clicking through flows, discovering edge cases, and reporting anomalies — something traditional automation cannot do.

### 7. ♿ Accessibility Testing
Integrated [axe-core](https://github.com/dequelabs/axe-core) scanning lets you catch WCAG violations automatically on every page.

### 8. 📊 Visual Regression Detection
Compare screenshots across releases to detect unintended UI changes — pixel-level diff with configurable thresholds.

### 9. 💰 Cost Reduction
- Reduces manual QA effort by 60-80%
- Eliminates script maintenance overhead
- Enables shift-left testing (developers test earlier)

### 10. 🚀 Faster Release Cycles
Automated smoke/regression testing on every deployment means faster confidence to release.

---

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────┐
│                     AI Agent                            │
│              (Gemini / Claude / GPT)                    │
│                                                         │
│  "Test the login flow on staging with invalid creds"    │
└─────────────┬───────────────────────────────────────────┘
              │ MCP Protocol (stdio or SSE)
              ▼
┌─────────────────────────────────────────────────────────┐
│              FastMCP Server                             │
│         playwright-qa-mcp                               │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Browser  │  │ Assertion│  │ Reporting│              │
│  │ Tools    │  │ Tools    │  │ Tools    │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │              │              │                    │
│  ┌────▼──────────────▼──────────────▼─────┐             │
│  │         Session Manager                │             │
│  │   (Browser pool, page contexts,        │             │
│  │    console listeners, network capture) │             │
│  └────────────────┬───────────────────────┘             │
│                   │                                      │
│  ┌────────────────▼───────────────────────┐             │
│  │         Playwright Engine              │             │
│  │   Chromium  │  Firefox  │  WebKit      │             │
│  └────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│              Target Application                         │
│         (Web app under test)                            │
└─────────────────────────────────────────────────────────┘
```

### Component Breakdown

| Component | Responsibility |
|-----------|---------------|
| **FastMCP Server** | Registers tools, handles MCP protocol, manages lifecycle |
| **Session Manager** | Manages browser instances, pages, cookies, and state |
| **Browser Tools** | Navigation, clicking, typing, file uploads |
| **Assertion Tools** | Text checks, element existence, URL validation, a11y |
| **Reporting Tools** | Screenshots, videos, HTML reports, JSON summaries |
| **Playwright Engine** | Actual browser automation (Chromium/Firefox/WebKit) |

---

## Tool Catalog

### Browser Management

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `launch_browser` | `browser_type`, `headless`, `viewport` | session_id | Start a browser session |
| `close_browser` | `session_id` | status | Tear down a session |
| `new_page` | `session_id`, `url` | page_id | Open a new tab |
| `set_viewport` | `width`, `height` or `device` preset | confirmation | Resize viewport |
| `set_cookies` | `cookies[]` | confirmation | Set browser cookies |
| `clear_storage` | `type` (cookies/localStorage/all) | confirmation | Clear browser data |

### Navigation

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `navigate` | `url`, `wait_until` | status, title, load_time | Go to URL |
| `go_back` | — | new URL | Browser back |
| `go_forward` | — | new URL | Browser forward |
| `reload` | — | status | Reload page |
| `wait_for_selector` | `selector`, `timeout` | found (bool) | Wait for element |
| `wait_for_navigation` | `url_pattern`, `timeout` | new URL | Wait for nav |

### Interaction

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `click` | `selector` or `text` or `role` | confirmation | Click element |
| `double_click` | `selector` | confirmation | Double-click |
| `right_click` | `selector` | confirmation | Right-click / context menu |
| `fill` | `selector`, `value` | confirmation | Type into input |
| `clear_and_fill` | `selector`, `value` | confirmation | Clear then type |
| `select_option` | `selector`, `value` or `label` | confirmation | Dropdown select |
| `check` | `selector` | confirmation | Check checkbox |
| `uncheck` | `selector` | confirmation | Uncheck checkbox |
| `upload_file` | `selector`, `file_path` | confirmation | Upload file |
| `press_key` | `key` (Enter, Tab, Escape, etc.) | confirmation | Keyboard input |
| `hover` | `selector` | confirmation | Mouse hover |
| `drag_and_drop` | `source`, `target` | confirmation | Drag element |
| `scroll` | `direction`, `amount` | confirmation | Scroll page |

### Assertions

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `assert_text_visible` | `text`, `exact` | pass/fail + details | Check text on page |
| `assert_text_not_visible` | `text` | pass/fail | Verify text absent |
| `assert_element_visible` | `selector` | pass/fail + count | Check element exists |
| `assert_element_hidden` | `selector` | pass/fail | Check element hidden |
| `assert_url` | `url` or `pattern` | pass/fail + actual URL | Validate URL |
| `assert_title` | `title` or `pattern` | pass/fail + actual title | Validate title |
| `assert_element_text` | `selector`, `expected` | pass/fail + actual | Element text match |
| `assert_input_value` | `selector`, `expected` | pass/fail + actual | Input value match |
| `assert_element_count` | `selector`, `expected_count` | pass/fail + actual | Count elements |
| `assert_attribute` | `selector`, `attr`, `value` | pass/fail + actual | Attribute check |

### Auditing

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `check_accessibility` | `standard` (WCAG 2.0/2.1) | violations[] | axe-core a11y audit |
| `check_console_errors` | — | errors[] | JS console errors |
| `check_broken_links` | `scope` (page/site) | broken_links[] | Validate all hrefs |
| `check_performance` | — | metrics (LCP, FCP, CLS, etc.) | Core Web Vitals |
| `check_responsive` | `breakpoints[]` | screenshots per breakpoint | Responsive check |

### Evidence & Reporting

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `screenshot` | `name`, `full_page`, `selector` | file_path | Capture screenshot |
| `screenshot_diff` | `baseline`, `current`, `threshold` | diff_percentage, diff_image | Visual regression |
| `start_recording` | `name` | confirmation | Start video recording |
| `stop_recording` | — | video_path | Stop and save video |
| `get_network_log` | `filter` | requests[] | Network request log |
| `generate_report` | `format` (html/json/md) | report_path | Test summary report |

### Test Orchestration

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `run_scenario` | `steps[]` | results[] with pass/fail | Multi-step test execution |
| `run_suite` | `scenarios[]` | aggregated results | Run multiple scenarios |
| `run_data_driven` | `scenario`, `data_table[]` | results per data row | Parameterized testing |

---

## Implementation Guide

### Project Structure

```
services/mcp_playwright/
├── main.py                 # FastMCP server entry point
├── config.py               # Configuration (timeouts, defaults)
├── session_manager.py      # Browser session lifecycle
├── tools/
│   ├── __init__.py
│   ├── browser.py          # launch, close, viewport tools
│   ├── navigation.py       # navigate, back, forward, wait tools
│   ├── interaction.py      # click, fill, select, upload tools
│   ├── assertions.py       # assert_* tools
│   ├── auditing.py         # accessibility, console, performance tools
│   └── reporting.py        # screenshot, video, report tools
├── utils/
│   ├── selectors.py        # Smart selector resolution
│   └── reporter.py         # Report generation (HTML/JSON)
├── templates/
│   └── report.html         # HTML report template
├── manifests/
│   └── deploy.yaml         # K8s deployment
├── Dockerfile
├── requirements.txt
└── README.md
```

### Step 1: Install Dependencies

```bash
pip install fastmcp playwright
playwright install  # Downloads browser binaries
```

**requirements.txt:**
```
fastmcp>=2.0.0
playwright>=1.45.0
axe-playwright-python>=0.1.0
Pillow>=10.0.0        # For screenshot comparison
Jinja2>=3.1.0         # For HTML report templates
```

### Step 2: Core Server Implementation

```python
# main.py
import asyncio
from contextlib import asynccontextmanager
from fastmcp import FastMCP
from playwright.async_api import async_playwright
from session_manager import SessionManager

# ── Lifespan: manage Playwright lifecycle ──────────────
@asynccontextmanager
async def lifespan(server):
    """Start Playwright on server boot, clean up on shutdown."""
    pw = await async_playwright().start()
    server.state["pw"] = pw
    server.state["sessions"] = SessionManager(pw)
    yield
    await server.state["sessions"].close_all()
    await pw.stop()

# ── FastMCP Server ─────────────────────────────────────
mcp = FastMCP(
    "playwright-qa",
    description="QA Testing MCP Server — Automate browser tests with Playwright",
    lifespan=lifespan,
)

# ── Tool: Launch Browser ───────────────────────────────
@mcp.tool()
async def launch_browser(
    browser_type: str = "chromium",
    headless: bool = True,
    viewport_width: int = 1280,
    viewport_height: int = 720,
) -> dict:
    """Launch a browser instance for testing.
    
    Args:
        browser_type: One of 'chromium', 'firefox', 'webkit'
        headless: Run without GUI (True for CI/CD)
        viewport_width: Browser viewport width in pixels
        viewport_height: Browser viewport height in pixels
    """
    sessions = mcp.state["sessions"]
    session_id = await sessions.create(
        browser_type=browser_type,
        headless=headless,
        viewport={"width": viewport_width, "height": viewport_height},
    )
    return {
        "session_id": session_id,
        "browser": browser_type,
        "headless": headless,
        "viewport": f"{viewport_width}x{viewport_height}",
    }

# ── Tool: Navigate ─────────────────────────────────────
@mcp.tool()
async def navigate(url: str, wait_until: str = "networkidle") -> dict:
    """Navigate to a URL and wait for the page to load.
    
    Args:
        url: The URL to navigate to
        wait_until: Wait condition — 'load', 'domcontentloaded', 'networkidle'
    """
    page = mcp.state["sessions"].get_active_page()
    import time
    start = time.time()
    response = await page.goto(url, wait_until=wait_until)
    load_time = round(time.time() - start, 2)
    return {
        "url": url,
        "status": response.status if response else None,
        "title": await page.title(),
        "load_time_seconds": load_time,
    }

# ── Tool: Click ────────────────────────────────────────
@mcp.tool()
async def click(
    selector: str = "",
    text: str = "",
    role: str = "",
    timeout: int = 5000,
) -> dict:
    """Click an element on the page.
    
    Provide ONE of: selector (CSS/XPath), text (visible text), 
    or role (ARIA role like 'button', 'link').
    
    Args:
        selector: CSS selector or XPath
        text: Visible text to find and click
        role: ARIA role (e.g., 'button', 'link', 'menuitem')
        timeout: Max wait time in milliseconds
    """
    page = mcp.state["sessions"].get_active_page()
    if text:
        await page.get_by_text(text).click(timeout=timeout)
        return {"clicked": f"text='{text}'"}
    elif role:
        await page.get_by_role(role).first.click(timeout=timeout)
        return {"clicked": f"role='{role}'"}
    else:
        await page.click(selector, timeout=timeout)
        return {"clicked": selector}

# ── Tool: Fill Form ────────────────────────────────────
@mcp.tool()
async def fill(
    selector: str = "",
    label: str = "",
    placeholder: str = "",
    value: str = "",
) -> dict:
    """Fill a form input field.
    
    Identify the field by CSS selector, label text, or placeholder.
    
    Args:
        selector: CSS selector for the input
        label: Associated label text
        placeholder: Placeholder text of the input
        value: Value to type into the field
    """
    page = mcp.state["sessions"].get_active_page()
    if label:
        await page.get_by_label(label).fill(value)
        return {"filled": f"label='{label}'", "value": value}
    elif placeholder:
        await page.get_by_placeholder(placeholder).fill(value)
        return {"filled": f"placeholder='{placeholder}'", "value": value}
    else:
        await page.fill(selector, value)
        return {"filled": selector, "value": value}

# ── Tool: Assert Text Visible ──────────────────────────
@mcp.tool()
async def assert_text_visible(text: str, exact: bool = False) -> dict:
    """Assert that specific text is visible on the page.
    
    Args:
        text: The text to search for
        exact: If True, match exact text; if False, substring match
    """
    page = mcp.state["sessions"].get_active_page()
    locator = page.get_by_text(text, exact=exact)
    count = await locator.count()
    return {
        "assertion": "text_visible",
        "text": text,
        "passed": count > 0,
        "occurrences": count,
    }

# ── Tool: Screenshot ──────────────────────────────────
@mcp.tool()
async def screenshot(
    name: str = "screenshot",
    full_page: bool = True,
    selector: str = "",
) -> dict:
    """Take a screenshot of the page or a specific element.
    
    Args:
        name: Filename for the screenshot (without extension)
        full_page: Capture the entire scrollable page
        selector: If provided, screenshot only this element
    """
    page = mcp.state["sessions"].get_active_page()
    path = f"./reports/{name}.png"
    if selector:
        element = page.locator(selector)
        await element.screenshot(path=path)
    else:
        await page.screenshot(path=path, full_page=full_page)
    return {"screenshot": path, "full_page": full_page}

# ── Tool: Check Accessibility ──────────────────────────
@mcp.tool()
async def check_accessibility(standard: str = "wcag2aa") -> dict:
    """Run an accessibility audit using axe-core.
    
    Args:
        standard: Accessibility standard — 'wcag2a', 'wcag2aa', 'wcag21aa'
    """
    page = mcp.state["sessions"].get_active_page()
    # Inject axe-core and run audit
    await page.evaluate("""
        await new Promise((resolve) => {
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.0/axe.min.js';
            script.onload = resolve;
            document.head.appendChild(script);
        });
    """)
    results = await page.evaluate("await axe.run()")
    violations = results.get("violations", [])
    return {
        "standard": standard,
        "passed": len(violations) == 0,
        "violation_count": len(violations),
        "violations": [
            {
                "id": v["id"],
                "impact": v["impact"],
                "description": v["description"],
                "nodes_affected": len(v["nodes"]),
            }
            for v in violations
        ],
    }

# ── Tool: Check Console Errors ─────────────────────────
@mcp.tool()
async def check_console_errors() -> dict:
    """Return any JavaScript console errors captured during the session."""
    errors = mcp.state["sessions"].get_console_errors()
    return {
        "passed": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors,
    }

# ── Tool: Run Test Scenario ────────────────────────────
@mcp.tool()
async def run_scenario(name: str, steps: list[dict]) -> dict:
    """Execute a multi-step test scenario.
    
    Args:
        name: Name of the test scenario
        steps: List of steps, each with 'action' and 'params'.
        
    Example steps:
        [
            {"action": "navigate", "params": {"url": "https://app.example.com/login"}},
            {"action": "fill", "params": {"label": "Email", "value": "admin@test.com"}},
            {"action": "fill", "params": {"label": "Password", "value": "secret123"}},
            {"action": "click", "params": {"text": "Sign In"}},
            {"action": "assert_text_visible", "params": {"text": "Welcome, Admin"}},
            {"action": "screenshot", "params": {"name": "login-success"}}
        ]
    """
    results = []
    all_passed = True
    
    for i, step in enumerate(steps):
        try:
            action = step["action"]
            params = step.get("params", {})
            tool_fn = mcp.tools.get(action)
            result = await tool_fn(**params)
            passed = result.get("passed", True) if isinstance(result, dict) else True
            results.append({
                "step": i + 1,
                "action": action,
                "status": "PASS" if passed else "FAIL",
                "result": result,
            })
            if not passed:
                all_passed = False
        except Exception as e:
            results.append({
                "step": i + 1,
                "action": step["action"],
                "status": "ERROR",
                "error": str(e),
            })
            all_passed = False
    
    return {
        "scenario": name,
        "total_steps": len(steps),
        "passed": all_passed,
        "results": results,
    }

# ── Tool: Generate Report ──────────────────────────────
@mcp.tool()
async def generate_report(
    title: str = "QA Test Report",
    format: str = "json",
) -> dict:
    """Generate a test report from the current session.
    
    Args:
        title: Report title
        format: Output format — 'json', 'html', or 'markdown'
    """
    session = mcp.state["sessions"].get_active_session()
    report = {
        "title": title,
        "timestamp": asyncio.get_event_loop().time(),
        "browser": session["browser_type"],
        "results": session.get("test_results", []),
        "screenshots": session.get("screenshots", []),
        "console_errors": session.get("console_errors", []),
    }
    
    path = f"./reports/{title.lower().replace(' ', '_')}.{format}"
    # Save report (implementation depends on format)
    return {"report_path": path, "format": format}

# ── Entry Point ────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
```

### Step 3: Session Manager

```python
# session_manager.py
import uuid
from playwright.async_api import Playwright, Browser, Page

class SessionManager:
    """Manages browser sessions, pages, and captured data."""
    
    def __init__(self, playwright: Playwright):
        self.pw = playwright
        self.sessions: dict[str, dict] = {}
        self.active_session_id: str | None = None
    
    async def create(
        self,
        browser_type: str = "chromium",
        headless: bool = True,
        viewport: dict = None,
    ) -> str:
        """Create a new browser session."""
        session_id = str(uuid.uuid4())[:8]
        
        launcher = getattr(self.pw, browser_type)
        browser = await launcher.launch(headless=headless)
        context = await browser.new_context(
            viewport=viewport or {"width": 1280, "height": 720},
            record_video_dir="./reports/videos/",
        )
        page = await context.new_page()
        
        # Capture console messages
        console_errors = []
        page.on("console", lambda msg: (
            console_errors.append({
                "type": msg.type,
                "text": msg.text,
                "location": str(msg.location),
            }) if msg.type == "error" else None
        ))
        
        self.sessions[session_id] = {
            "browser": browser,
            "context": context,
            "page": page,
            "browser_type": browser_type,
            "console_errors": console_errors,
            "test_results": [],
            "screenshots": [],
        }
        self.active_session_id = session_id
        return session_id
    
    def get_active_page(self) -> Page:
        """Get the active page."""
        return self.sessions[self.active_session_id]["page"]
    
    def get_active_session(self) -> dict:
        """Get the active session data."""
        return self.sessions[self.active_session_id]
    
    def get_console_errors(self) -> list:
        """Get console errors from the active session."""
        return self.sessions[self.active_session_id]["console_errors"]
    
    async def close_all(self):
        """Close all browser sessions."""
        for session in self.sessions.values():
            await session["context"].close()
            await session["browser"].close()
        self.sessions.clear()
```

---

## Usage Examples

### Example 1: Smoke Test After Deployment

**Agent prompt:**
```
Run a smoke test on https://myapp.example.com — check that the homepage loads,
the login page works, and there are no JavaScript errors.
```

**What the AI agent does (tool calls):**
```json
[
  {"tool": "launch_browser", "params": {"browser_type": "chromium"}},
  {"tool": "navigate", "params": {"url": "https://myapp.example.com"}},
  {"tool": "assert_text_visible", "params": {"text": "Welcome"}},
  {"tool": "check_console_errors", "params": {}},
  {"tool": "navigate", "params": {"url": "https://myapp.example.com/login"}},
  {"tool": "assert_element_visible", "params": {"selector": "#login-form"}},
  {"tool": "screenshot", "params": {"name": "smoke-test-login"}},
  {"tool": "close_browser", "params": {}}
]
```

### Example 2: Login Flow Test

**Agent prompt:**
```
Test the login flow: go to /login, enter "user@test.com" and "Password1!", 
click Sign In, verify the dashboard shows "Hello, User".
```

**Using `run_scenario`:**
```json
{
  "tool": "run_scenario",
  "params": {
    "name": "Login Flow",
    "steps": [
      {"action": "navigate", "params": {"url": "https://app.example.com/login"}},
      {"action": "fill", "params": {"label": "Email", "value": "user@test.com"}},
      {"action": "fill", "params": {"label": "Password", "value": "Password1!"}},
      {"action": "click", "params": {"text": "Sign In"}},
      {"action": "assert_text_visible", "params": {"text": "Hello, User"}},
      {"action": "assert_url", "params": {"pattern": "*/dashboard*"}},
      {"action": "screenshot", "params": {"name": "login-success"}}
    ]
  }
}
```

### Example 3: Cross-Browser Visual Regression

**Agent prompt:**
```
Take screenshots of the homepage on Chromium, Firefox, and WebKit 
and compare them for visual differences.
```

### Example 4: Accessibility Audit

**Agent prompt:**
```
Run a WCAG 2.1 AA accessibility audit on every page of the marketing site.
Report all critical and serious violations.
```

### Example 5: Form Validation Testing

**Agent prompt:**
```
Test the registration form with these scenarios:
1. Submit empty form — verify error messages
2. Enter invalid email — verify email validation
3. Enter mismatched passwords — verify password match error
4. Fill everything correctly — verify success message
```

---

## Configuration

### config.py

```python
# Default configuration for the Playwright QA MCP Server

CONFIG = {
    # Browser defaults
    "default_browser": "chromium",
    "headless": True,
    "default_viewport": {"width": 1280, "height": 720},
    
    # Timeouts (milliseconds)
    "navigation_timeout": 30000,
    "action_timeout": 5000,
    "assertion_timeout": 5000,
    
    # Screenshots
    "screenshot_dir": "./reports/screenshots/",
    "screenshot_format": "png",  # png or jpeg
    "full_page_screenshots": True,
    
    # Video recording
    "video_dir": "./reports/videos/",
    "record_video": False,  # Enable per-session
    
    # Reporting
    "report_dir": "./reports/",
    "report_format": "html",  # html, json, markdown
    
    # Visual regression
    "diff_threshold": 0.1,  # 0.1% pixel difference tolerance
    "baseline_dir": "./reports/baselines/",
    
    # Accessibility
    "a11y_standard": "wcag2aa",
    
    # Device presets
    "devices": {
        "mobile": {"width": 375, "height": 812},      # iPhone X
        "tablet": {"width": 768, "height": 1024},      # iPad
        "desktop": {"width": 1920, "height": 1080},    # Full HD
        "laptop": {"width": 1366, "height": 768},      # Common laptop
    },
}
```

### MCP Client Configuration (claude_desktop_config.json)

```json
{
  "mcpServers": {
    "playwright-qa": {
      "command": "python",
      "args": ["/path/to/services/mcp_playwright/main.py"],
      "env": {
        "PLAYWRIGHT_BROWSERS_PATH": "/path/to/browsers"
      }
    }
  }
}
```

### Gemini Code Assist / VS Code MCP Settings

```json
{
  "mcpServers": {
    "playwright-qa": {
      "command": "python",
      "args": ["./services/mcp_playwright/main.py"],
      "transportType": "stdio"
    }
  }
}
```

---

## Deployment

### Local Development

```bash
cd services/mcp_playwright
pip install -r requirements.txt
playwright install chromium
python main.py  # Starts MCP server on stdio
```

### Docker

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 \
    libgbm1 libpango-1.0-0 libcairo2 libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium --with-deps

COPY . .

CMD ["python", "main.py"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: playwright-qa-mcp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: playwright-qa-mcp
  template:
    metadata:
      labels:
        app: playwright-qa-mcp
    spec:
      containers:
        - name: playwright-qa
          image: your-registry/playwright-qa-mcp:latest
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "2Gi"
              cpu: "2000m"
          volumeMounts:
            - name: reports
              mountPath: /app/reports
      volumes:
        - name: reports
          emptyDir: {}
```

### CI/CD Integration (GitHub Actions)

```yaml
name: QA Smoke Tests
on:
  deployment:
    types: [completed]

jobs:
  smoke-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          pip install fastmcp playwright
          playwright install chromium --with-deps
      - name: Run MCP QA Tests
        run: python run_smoke_tests.py
      - name: Upload Reports
        uses: actions/upload-artifact@v4
        with:
          name: qa-reports
          path: reports/
```

---

## FAQ

### General

**Q: What is MCP (Model Context Protocol)?**
A: MCP is an open protocol that allows AI assistants (like Gemini, Claude) to securely connect to external tools and data sources. Think of it as a "USB-C for AI" — a standard way to plug capabilities into AI agents.

**Q: Why use FastMCP instead of building from scratch?**
A: FastMCP is a high-level Python framework that handles all the MCP protocol boilerplate — transport, tool registration, type validation, error handling. You just define your tools as Python functions with decorators.

**Q: Can this replace my existing QA automation framework?**
A: It's best used **alongside** existing frameworks, not as a replacement. Use it for:
- Exploratory testing (AI-driven)
- Smoke tests (quick post-deploy checks)
- Accessibility audits
- Visual regression
Keep your existing Playwright/Selenium scripts for complex, data-driven regression suites.

---

### Technical

**Q: How does the AI agent know which tools to call?**
A: MCP tools include descriptions and parameter schemas. The AI agent reads these descriptions and determines which tools to call based on the user's natural language request. Good tool descriptions are critical.

**Q: What browsers are supported?**
A: Playwright supports **Chromium** (Chrome, Edge), **Firefox**, and **WebKit** (Safari). All three can be launched via the `launch_browser` tool.

**Q: Can I test authenticated flows?**
A: Yes. You can:
1. Use `fill` + `click` to log in through the UI
2. Use `set_cookies` to inject auth cookies directly
3. Use Playwright's `storageState` to save/restore authenticated sessions

**Q: How do I handle dynamic content / SPAs?**
A: Use the `wait_for_selector` and `wait_for_navigation` tools. Playwright automatically waits for elements and handles AJAX calls with its `networkidle` wait strategy.

**Q: Can I run tests in parallel?**
A: Yes. Create multiple browser sessions with `launch_browser` (each gets a unique `session_id`). The session manager supports concurrent sessions.

**Q: What about file downloads?**
A: Playwright supports download handling. A `handle_download` tool can be added to wait for and save downloaded files.

---

### Security

**Q: Is it safe to run in production?**
A: The MCP server should only be deployed in **staging/test environments**. It has full browser control, so restrict access via:
- Network policies (K8s)
- Authentication on the MCP transport layer
- Read-only access to target applications

**Q: Can it access internal applications?**
A: Yes, as long as the server has network access. In Kubernetes, deploy it in the same namespace or grant appropriate network policies.

---

### Performance

**Q: How much memory does it need?**
A: Each Chromium instance uses ~100-300MB. Recommended:
- **1 session**: 512MB minimum
- **5 concurrent sessions**: 2GB minimum
- **CI/CD (single browser)**: 1GB is comfortable

**Q: What's the overhead vs raw Playwright?**
A: Minimal. The MCP protocol adds ~1-5ms per tool call for serialization. The bottleneck is always the browser, not the MCP layer.

**Q: Can it handle long-running test suites?**
A: Yes. Use `run_suite` for orchestration. For very long suites (30+ minutes), consider splitting into smaller scenarios to avoid browser memory leaks.

---

### Integration

**Q: Which AI agents work with this?**
A: Any MCP-compatible agent:
- **Google Gemini** (via Gemini Code Assist, Vertex AI)
- **Anthropic Claude** (via Claude Desktop, API)
- **Custom agents** built with LangChain, AutoGen, etc.

**Q: Can I trigger tests from Slack/Teams?**
A: Yes. Build a bot that:
1. Receives a command ("test the login page")
2. Sends it to an AI agent connected to the MCP server
3. Returns the test results + screenshots to the channel

**Q: Can I integrate with Jira/TestRail?**
A: Add custom tools like `create_jira_bug` or `update_test_case` that call their APIs. The AI agent can automatically file bugs when tests fail.

---

## Roadmap

| Phase | Features | Timeline |
|-------|----------|----------|
| **v1.0** | Core tools (navigate, click, fill, assert, screenshot) | Week 1-2 |
| **v1.1** | Accessibility auditing, console error checks | Week 3 |
| **v1.2** | Visual regression (screenshot diff) | Week 4 |
| **v2.0** | Test orchestration (scenarios, suites, data-driven) | Week 5-6 |
| **v2.1** | HTML/PDF report generation | Week 7 |
| **v3.0** | CI/CD integration, Slack/Jira connectors | Week 8-10 |
| **v3.1** | Performance testing (Core Web Vitals) | Week 11 |
| **v4.0** | AI-powered exploratory testing (self-guided crawling) | Week 12+ |

---

## References

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Playwright Python Documentation](https://playwright.dev/python/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [axe-core Accessibility Engine](https://github.com/dequelabs/axe-core)
- [Playwright Test Best Practices](https://playwright.dev/docs/best-practices)
