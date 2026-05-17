# Testing Strategy for LearnSQL.ai

This document outlines the recommended best practices and strategies for testing the LearnSQL.ai application, which consists of a Python/FastAPI backend and a Vite-based frontend.

Currently, testing relies on manual Python scripts using `requests`. Transitioning to standardized testing frameworks will improve reliability, developer experience, and code quality.

## 1. Backend Testing (Python / FastAPI)

The backend is built with FastAPI. The best approach is to use `pytest` along with FastAPI's built-in testing tools.

### Recommended Tools
*   **[pytest](https://docs.pytest.org/):** The industry standard for Python testing. It provides a clean, simple syntax and powerful features like fixtures.
*   **[pytest-asyncio](https://pytest-asyncio.readthedocs.io/):** Essential for testing asynchronous FastAPI endpoints and database calls.
*   **FastAPI `TestClient`:** Allows you to test your endpoints without starting a live server, making tests fast and reliable.

### Best Practices
*   **Replace Script-Based Tests:** Convert scripts like `test_backend.py` and `test_api_debug.py` into proper `pytest` files (e.g., `tests/test_endpoints.py`).
*   **Use `TestClient`:** Instead of `requests.get("http://localhost:8000/api/health")`, use:
    ```python
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    def test_health_check():
        response = client.get("/api/health")
        assert response.status_code == 200
    ```
*   **Mocking External Services:** Use `unittest.mock` (or `pytest-mock`) to mock external dependencies like the LLM calls (e.g., OpenAI API) or database connections so your unit tests are deterministic and fast.
*   **Test Database:** Use an isolated, temporary SQLite or PostgreSQL test database for integration tests to ensure you aren't mutating development or production data.

## 2. Frontend Testing (Vite / React)

For a modern Vite-based frontend, we recommend a combination of Vitest and Playwright.

### Recommended Tools
*   **[Vitest](https://vitest.dev/):** A blazing fast unit testing framework native to Vite. It shares the same configuration as your Vite project and is a drop-in replacement for Jest.
*   **[React Testing Library](https://testing-library.com/docs/react-testing-library/intro/):** The standard for testing React components in a user-centric way. Use it with Vitest to ensure components render correctly and respond to user events.
*   **[Playwright](https://playwright.dev/):** For End-to-End (E2E) testing. It tests the application in a real browser to verify that the frontend and backend work together correctly (e.g., simulating a user submitting a SQL query and checking the results).

### Best Practices
*   **Component Testing:** Write unit tests for individual UI components (e.g., testing that the SQL code editor or chatbot message bubbles render correctly).
*   **Mock API Calls:** In component tests, mock the API responses using tools like MSW (Mock Service Worker) so frontend tests don't depend on the backend being running.
*   **E2E Workflows:** Write E2E tests for critical user journeys: signing up, asking the chatbot a question, and completing a learning module.

## 3. Continuous Integration (CI)

Once testing frameworks are in place, tests should run automatically.

*   **GitHub Actions:** Create a CI pipeline (`.github/workflows/test.yml`) that automatically runs both your frontend and backend tests on every Pull Request or push to the `main` branch.
*   **Pre-commit Hooks:** Consider using `husky` (frontend) or `pre-commit` (backend) to run a quick subset of tests and linters before allowing a commit.

## Summary: Next Steps

1.  **Backend:** Add `pytest` and `pytest-mock` to `backend/requirements.txt`. Refactor current `test_*.py` scripts into a dedicated `backend/tests/` directory using `TestClient`.
2.  **Frontend:** Install `vitest`, `jsdom`, and `@testing-library/react` via npm/yarn. Add a basic component test.
3.  **E2E:** Set up Playwright for 2-3 critical user flows.
