# QA Automation Portfolio — Rodrigo Santana

![CI](https://github.com/rodrigost1455-hub/qa-automation-portfolio/actions/workflows/ci.yml/badge.svg)

Test suites for my production projects, written as part of my transition into QA Automation Engineering.

I already build and ship production software. This repo documents my practice in systematic test engineering: unit tests, integration tests, API contract testing, and E2E automation.

---

## Projects Covered

| Project | Description | Test Types |
|---------|-------------|------------|
| [FA Report System](https://github.com/rodrigost1455-hub/FA-Report-System) | FastAPI PDF automation for failure analysis | Unit · Integration · API |
| [StatPro Industrial](https://github.com/rodrigost1455-hub/STAT-PRO) | Offline SPC platform | Unit (coming) |
| [8D QMS](https://github.com/rodrigost1455-hub/8D-app) | Non-conformance tracking app | E2E Playwright (coming) |

---

## Test Coverage

| Module | Framework | Status |
|--------|-----------|--------|
| Report schema validation (Pydantic) | Pytest | ✅ Active |
| Report API endpoints (FastAPI) | Pytest + HTTPX | ✅ Active |
| SPC calculations (StatPro) | Pytest | 🚧 In progress |
| 8D App UI flows | Playwright | 📋 Planned |

---

## Stack

- **Test runner:** Pytest
- - **Async testing:** pytest-asyncio
  - - **API testing:** HTTPX (async client)
    - - **Mocking:** pytest-mock, unittest.mock
      - - **E2E (coming):** Playwright
        - - **CI:** GitHub Actions
         
          - ---

          ## Run Tests Locally

          ```bash
          # 1. Clone this repo
          git clone https://github.com/rodrigost1455-hub/qa-automation-portfolio
          cd qa-automation-portfolio

          # 2. Create virtual environment
          python -m venv venv
          source venv/bin/activate  # Windows: venv\Scripts\activate

          # 3. Install dependencies
          pip install -r requirements.txt

          # 4. Run all tests
          pytest

          # 5. Run with coverage report
          pytest --cov=tests --cov-report=term-missing

          # 6. Run only unit tests
          pytest tests/unit/ -v

          # 7. Run only integration tests
          pytest tests/integration/ -v
          ```

          ---

          ## CI/CD

          Tests run automatically on every push and pull request via GitHub Actions.
          See `.github/workflows/ci.yml`.

          ---

          ## Author

          **Rodrigo Santana Torrecillas**
          Software Engineer · QA Automation
          [LinkedIn](https://www.linkedin.com/in/rodrigo-santana-torrecillas-5b523113b/) · Monterrey, México
