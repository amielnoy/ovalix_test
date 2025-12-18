API test automation

Quick start

1. Copy the example env and set `API_BASE_URL` (or export it directly):

```bash
cp test_automation/.env.example test_automation/.env
# or export directly:
export API_BASE_URL=http://localhost:8000/userapp/users
```

2. Create and activate a Python virtualenv, then install test deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r test_automation/requirements.txt
```

3. Start the application under test (option A: Docker Compose):

```bash
# from repository root
docker compose -f compose.yml up --build -d
```

4. Run tests:

```bash
# run the full test suite under test_automation
pytest -q test_automation/tests

# run just the edge-cases
pytest -q test_automation/tests/edge_cases

# run a single test file
pytest -q test_automation/tests/test_user_crud.py
```

Notes
- Tests read `API_BASE_URL` env var to locate the API. Point it at the collection endpoint (example above).
- The test helpers live in `test_automation/`:
	- `test_automation/http_client.py` — lightweight requests wrapper
	- `test_automation/services/user_service.py` — convenience methods (`create_user`, `get_user`, `update_user`, `delete_user`)
	- Fixtures are defined in `test_automation/conftest.py`.
- CI: GitHub Actions workflow is at `.github/workflows/ci.yml` and uses `docker/compose-action` to start services before running `pytest`.

Troubleshooting
- If a POST returns a 500 with an APPEND_SLASH error, ensure the base URL is correct; the test client normalizes trailing slashes but point `API_BASE_URL` to the collection endpoint (e.g. `/userapp/users`).
- If Actions doesn't trigger on push, check repository Actions settings (Settings → Actions → General) and workflow approvals.

Contact
- If you want me to tighten validations, consolidate tests, or run the full suite in CI, tell me which and I'll proceed.

