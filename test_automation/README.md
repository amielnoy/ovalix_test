API test automation framework (live share)

Quick start

1. Copy the example env and (optionally) edit the `API_BASE_URL`:

```bash
cp <Root Folder>/test_automation/.env <Root Folder>/test_automation/.env
# edit the .env file if needed
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

Files in this folder:

- `http_client.py` — HTTP wrapper
- `services/user_service.py` — user service layer
- `conftest.py` — pytest fixtures
- `tests/` — pytest test files (CRUD and edge cases)

Notes
- Tests read `API_BASE_URL` env var to locate the API. Point it at the collection endpoint (example above).
- The test helpers live in `test_automation/`:
	- `test_automation/http_client.py` — lightweight requests wrapper
	- `test_automation/services/user_service.py` — convenience methods (`create_user`, `get_user`, `update_user`, `delete_user`)
	- Fixtures are defined in `test_automation/conftest.py`.
- CI: GitHub Actions workflow is at `.github/workflows/ci.yml` and uses `docker/compose-action` to start services before running `pytest`.

Run CI from GitHub

You can trigger the CI workflow manually from the GitHub UI using the `workflow_dispatch` trigger added to `.github/workflows/ci.yml`:

- Open the repository on GitHub and go to the `Actions` tab.
- Select the `CI` workflow, then click the `Run workflow` button.
- Optional inputs:
	- `run_full_suite` (default `true`) — set to `false` to skip long tests.
	- `api_base_url` — override `API_BASE_URL` for the run (for example `http://staging.example.com/userapp/users`).

The manual run is useful for debugging CI-only failures or validating fixes without pushing additional commits.

Troubleshooting
- If a POST returns a 500 with an APPEND_SLASH error, ensure the base URL is correct; the test client normalizes trailing slashes but point `API_BASE_URL` to the collection endpoint (e.g. `/userapp/users`).
- If Actions doesn't trigger on push, check repository Actions settings (Settings → Actions → General) and workflow approvals.

Contact
- If you want me to tighten validations, consolidate tests, or run the full suite in CI, tell me which and I'll proceed.
