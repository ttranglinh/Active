# Active

## Serper setup (ready to call)

1. Create and activate venv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

3. Add your API key:

```powershell
Copy-Item .env.example .env
```

Set `SERPER_API_KEY` in `.env`.

4. Run the Serper ingestion test with fake input:

```powershell
$env:SERPER_API_KEY="your_key_here"
python scripts\collect_serper_raw_linkedin.py --input-file fi_au_saas_security_001.json --target-count 100
```

Outputs:
- Raw API responses: `data/raw/serper/linkedin_search/<run_id>/query_###.json`
- Manifest: `data/raw/serper/linkedin_search/<run_id>/manifest.json`
- Extracted LinkedIn profile URLs:
  - `data/processed/ingestion/linkedin_profile_urls/<run_id>.json`
  - `data/processed/ingestion/linkedin_profile_urls/<run_id>.csv`
