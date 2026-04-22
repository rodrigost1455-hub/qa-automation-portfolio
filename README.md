# QA Automation Portfolio

[![QA Automation Suite](https://github.com/rodrigost1455-hub/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/rodrigost1455-hub/qa-automation-portfolio/actions/workflows/tests.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Selenium](https://img.shields.io/badge/selenium-4.27-green.svg)](https://www.selenium.dev/)
[![pytest](https://img.shields.io/badge/pytest-8.3-orange.svg)](https://docs.pytest.org/)

A production-grade QA Automation Framework built with Python, Selenium, and Pytest.
Demonstrates industry-standard practices: Page Object Model, explicit waits, CI/CD integration,
structured HTML reporting, and multi-layer test coverage (unit → integration → E2E).

---

## Architecture

```
qa-automation-portfolio/
│
├── pages/                      # Page Object Model layer
│   ├── base_page.py            #   Base class — all explicit-wait wrappers live here
│   ├── login_page.py           #   Login screen interactions and assertions
│   ├── search_page.py          #   Product inventory: listing, sorting, cart actions
│   └── form_page.py            #   3-step checkout form flow
│
├── tests/
│   ├── test_login.py           # Selenium: login flows (happy path + error states)
│   ├── test_search.py          # Selenium: product sorting and cart badge
│   ├── test_form.py            # Selenium: checkout form validation and completion
│   ├── unit/
│   │   └── test_report_schemas.py    # Pydantic schema validation (FA Report System)
│   ├── integration/
│   │   └── test_reports_api.py       # API response shape & pagination contracts
│   └── e2e/
│       └── test_8d_app.py            # Playwright: 8D QMS application smoke suite
│
├── utils/
│   ├── config.py               # Central config: env vars with safe defaults
│   ├── driver_factory.py       # WebDriver factory (Chrome / Firefox, headless support)
│   └── helpers.py              # Screenshot capture, logger setup, test-data generators
│
├── reports/                    # Generated HTML reports + failure screenshots (gitignored)
├── .github/workflows/
│   └── tests.yml               # CI/CD: 3-job pipeline (unit+integration → selenium → playwright)
├── conftest.py                 # Shared fixtures, failure-screenshot hook
├── requirements.txt
└── pytest.ini
```

### Design Principles

| Principle | Implementation |
|-----------|---------------|
| **Page Object Model** | Every screen is a class; locators and actions are encapsulated, never duplicated in tests |
| **Explicit waits only** | `WebDriverWait` + `expected_conditions` throughout `BasePage`; `implicitly_wait=0` |
| **No hard sleeps** | Zero `time.sleep()` calls in the entire codebase |
| **Test isolation** | Each test gets a fresh `driver` (function-scoped fixture) with automatic teardown |
| **Screenshot on failure** | `pytest_runtest_makereport` hook captures a PNG before driver quits |
| **Environment-driven config** | Every setting overridable via env var — no hard-coded values in test code |

---

## Tech Stack

| Layer | Tool | Version |
|-------|------|---------|
| Language | Python | 3.12+ |
| Browser automation | Selenium + Selenium Manager | 4.27 |
| Test runner | Pytest | 8.3 |
| HTML reports | pytest-html | 4.1 |
| API / schema validation | Pydantic + HTTPX | 2.10 / 0.27 |
| Playwright (legacy E2E) | playwright + pytest-playwright | 1.49 |
| CI/CD | GitHub Actions | — |

> **Why Selenium over Playwright for the main framework?**
> Selenium's WebDriver standard is the dominant protocol in enterprise QA toolchains.
> Demonstrating deep Selenium expertise (explicit waits, POM, multi-browser support)
> is more broadly applicable for SDET roles. Playwright powers the legacy 8D QMS
> suite where its automatic waiting model reduces boilerplate for SPA navigation.

---

## Running Tests Locally

### Prerequisites

- Python 3.12+
- Google Chrome (or Firefox if `BROWSER=firefox`)
- Git

### Setup

```bash
# Clone
git clone https://github.com/rodrigost1455-hub/qa-automation-portfolio
cd qa-automation-portfolio

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies (Selenium Manager auto-downloads ChromeDriver)
pip install -r requirements.txt
```

### Run tests

```bash
# All Selenium tests (headless by default)
pytest tests/test_login.py tests/test_search.py tests/test_form.py -v

# With HTML report saved to reports/
pytest tests/test_login.py tests/test_search.py tests/test_form.py \
  --html=reports/report.html --self-contained-html

# Run with a visible browser window (useful for debugging)
HEADLESS=false pytest tests/test_login.py -v

# Firefox instead of Chrome
BROWSER=firefox pytest tests/test_search.py -v

# Unit tests only (no browser required)
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Full suite with coverage
pytest tests/unit/ tests/integration/ \
  --cov=tests --cov-report=term-missing
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `https://www.saucedemo.com` | Target application base URL |
| `BROWSER` | `chrome` | Browser: `chrome` or `firefox` |
| `HEADLESS` | `true` | Run without UI when `true` |
| `EXPLICIT_WAIT` | `10` | Global WebDriverWait timeout (seconds) |
| `SCREENSHOT_ON_FAILURE` | `true` | Auto-capture PNG on test failure |
| `REPORTS_DIR` | `reports` | Directory for HTML reports and screenshots |

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/tests.yml`) runs on every push
to `main`, `develop`, or `claude/**` branches and on all pull requests to `main`.

```
Push / PR
    │
    ▼
┌─────────────────────────────────┐
│  Job 1: Unit & Integration      │  Python 3.11 + 3.12 matrix
│  pytest tests/unit/             │
│  pytest tests/integration/      │
│  Coverage XML → artifact        │
└──────────────┬──────────────────┘
               │ needs: Job 1
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌──────────────────┐
│  Job 2       │  │  Job 3           │
│  Selenium    │  │  Playwright      │
│  Chrome      │  │  Chromium        │
│  headless    │  │  headless        │
│  HTML report │  │  (continue-on-   │
│  → artifact  │  │   error: true)   │
└──────────────┘  └──────────────────┘
```

**Artifacts produced per run:**

| Artifact | Contents | Retention |
|----------|----------|-----------|
| `coverage-report-py3.11` | `coverage.xml` | 14 days |
| `coverage-report-py3.12` | `coverage.xml` | 14 days |
| `selenium-html-reports` | login/search/form HTML + screenshots | 14 days |
| `playwright-report` | Playwright trace viewer output | 7 days |

---

## Test Coverage Summary

| Suite | File | Tests | Framework |
|-------|------|-------|-----------|
| Login flows | `tests/test_login.py` | 8 | Selenium + POM |
| Product search & sort | `tests/test_search.py` | 8 | Selenium + POM |
| Checkout form | `tests/test_form.py` | 9 | Selenium + POM |
| Pydantic schema validation | `tests/unit/test_report_schemas.py` | 24 | Pytest |
| API response contracts | `tests/integration/test_reports_api.py` | 20 | Pytest |
| 8D QMS smoke | `tests/e2e/test_8d_app.py` | 10 | Playwright |
| **Total** | | **79** | |

---

## Projects Under Test

| Application | Repository | Test Scope |
|-------------|------------|------------|
| Sauce Demo | Public demo at saucedemo.com | Login · Search · Checkout (Selenium) |
| FA Report System | [FA-Report-System](https://github.com/rodrigost1455-hub/FA-Report-System) | Schema validation · API contracts |
| 8D QMS | [8D-app](https://github.com/rodrigost1455-hub/8D-app) | Full D1–D8 workflow (Playwright) |

---

## Future Improvements

- [ ] **Allure reporting** — richer test analytics with trend graphs and step-level screenshots
- [ ] **Data-driven tests** — parameterize credential and form tests using `pytest.mark.parametrize` + CSV/JSON datasets
- [ ] **Cross-browser matrix** — add Firefox and Edge to the CI Selenium job
- [ ] **Visual regression** — integrate Percy or pixelmatch to catch unintended UI changes
- [ ] **API layer tests** — extend HTTPX suite with live contract tests against the FA Report API
- [ ] **Docker runner** — containerised Selenium Grid for reproducible multi-browser execution

---

## Author

**Rodrigo Santana Torrecillas**
Software Engineer · QA Automation Engineer
[LinkedIn](https://www.linkedin.com/in/rodrigo-santana-torrecillas-5b523113b/) · Monterrey, México
