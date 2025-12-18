API test automation framework (live share)

Quick start

1. Copy the example env and (optionally) edit the `API_BASE_URL`:

```bash
cp vsls:/test_automation/.env vsls:/test_automation/.env
# edit the .env file if needed
```

2. Install dependencies and run tests from your environment:

```bash
python3 -m pip install -r vsls:/test_automation/requirements.txt
pytest -q vsls:/test_automation/tests -s
```

