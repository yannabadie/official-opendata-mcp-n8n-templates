# Official Open-Data MCP & n8n Templates (SIRENE, TED Europa, BOAMP, ClinicalTrials, US NPI, PubMed)

Ready-to-import **n8n workflow templates**, **Claude / Cursor / Antigravity MCP config (`mcp.json`)**, and a **zero-dependency Python CLI** for querying **5 official European and U.S. government & biomedical open-data registries** with **zero proxies, zero CAPTCHAs, and deterministic JSON schemas**.

---

## Included Open-Data Registries & Live Actors

| Registry / Domain | Official Upstream APIs | Highlights | Live Apify Actor (Pay-Per-Event + MCP) |
|---|---|---|---|
| **French Companies & KYC** | DINUM/INSEE/INPI SIRENE/RNE + DILA BODACC + BOAMP | **FREE `count` mode**, GPS radius search (`/near_point`), RGE/Qualiopi/Bio/ESS filters, EU VAT, financials, executives & opt-in insolvency KYC (`$6 / 1,000`) | [`yannabadie/french-company-intelligence-mcp`](https://apify.com/yannabadie/french-company-intelligence-mcp) |
| **EU & France Public Tenders** | EU TED Search API v3 (27 countries) + French BOAMP | Direct **buyer email, phone & website**, award winners (`can-standard`), `minValueEur`, `deadlineAfter` & raw TED Expert Query (`$3–$4 / 1,000`) | [`yannabadie/eu-public-tenders-ted-boamp`](https://apify.com/yannabadie/eu-public-tenders-ted-boamp) |
| **Global Clinical Trials** | U.S. NIH ClinicalTrials.gov REST API v2 (500k+ studies) | **FREE `count` mode**, paste ClinicalTrials.gov URLs or NCT IDs, central & site contact emails/phones, phases, sponsors & `updatedSince` watch (`$5 / 1,000`) | [`yannabadie/clinical-trials-api-mcp`](https://apify.com/yannabadie/clinical-trials-api-mcp) |
| **U.S. Doctors & Clinics (NPI)** | U.S. CMS NPPES NPI Registry API v2.1 (8M+ providers) | **Flat `$2.50 / 1,000` all-inclusive** (zero phone surcharge), FREE `count` mode, practice phones/fax, licenses & Authorized Official decision-makers | [`yannabadie/npi-healthcare-providers-mcp`](https://apify.com/yannabadie/npi-healthcare-providers-mcp) |
| **PubMed & Europe PMC Papers** | EMBL-EBI Europe PMC & PubMed REST API (37M+ papers) | **100% untruncated abstracts**, author emails, ORCIDs, citations, MeSH, NIH/EU grants, linked NCT trials & **free PDF URLs** (`$2 / 1,000`, FREE `count` mode) | [`yannabadie/pubmed-europepmc-api-mcp`](https://apify.com/yannabadie/pubmed-europepmc-api-mcp) |

> Prefer a **zero-API-key local stdio MCP server** for quick interactive lookups in Claude/Cursor? See [`yannabadie/eu-us-opendata-mcp`](https://github.com/yannabadie/eu-us-opendata-mcp).

*Free Apify accounts include `$5/month` of usage credits — enough to run ~800–1,600 records/month for free.*

---

## 1. Ready-to-Import n8n Templates (`workflows/`)

1. **[`workflows/n8n_eu_public_tenders_slack_sheets.json`](workflows/n8n_eu_public_tenders_slack_sheets.json)**
   - Daily 08:00 trigger -> queries EU TED v3 + French BOAMP -> upserts tenders (with `buyerEmail` & `buyerPhone`) into Google Sheets + posts Slack alerts.
2. **[`workflows/n8n_french_company_kyc_enrichment.json`](workflows/n8n_french_company_kyc_enrichment.json)**
   - Webhook taking a SIREN list -> enriches SIRENE/RNE + EU VAT + BODACC insolvency notices -> automatically routes `high_risk` / `closed` entities to a Slack compliance channel.
3. **[`workflows/n8n_clinical_trials_sponsor_watch.json`](workflows/n8n_clinical_trials_sponsor_watch.json)**
   - Daily 08:00 trigger -> watches updated Phase 2/3 industry clinical trials -> upserts NCT studies + contact emails into Google Sheets + sends Slack pipeline alerts.
4. **[`workflows/n8n_us_npi_healthcare_leads_sheets.json`](workflows/n8n_us_npi_healthcare_leads_sheets.json)**
   - Queries U.S. CMS NPI Registry API v2.1 (`NPI-2` clinics & group practices with phone only) -> upserts phones, fax, and Authorized Official contacts into Google Sheets.
5. **[`workflows/n8n_pubmed_kol_literature_watch.json`](workflows/n8n_pubmed_kol_literature_watch.json)**
   - Weekly Monday 08:00 trigger -> queries PubMed & Europe PMC (`onlyWithEmail: true`, `hasFreePdf: true`) -> upserts papers, author emails, linked NCT trials & free PDF links into Google Sheets + Slack alerts.

### Import into n8n (60 seconds)
1. Download any `.json` file from `workflows/` and click **Import from File** in n8n.
2. Add `APIFY_TOKEN` (and optional `SLACK_WEBHOOK_URL`) to your n8n environment variables.
3. Customize filters (`cpvCodes`, `countries`, `condition`, `phases`, `sirens`) and activate.

---

## 2. Connect to Claude Code, Cursor, or Antigravity via MCP (`mcp/mcp.json`)

Drop [`mcp/mcp.json`](mcp/mcp.json) into your MCP client configuration (set `APIFY_TOKEN`):

```json
{
  "mcpServers": {
    "apify-official-opendata": {
      "url": "https://mcp.apify.com/?actors=yannabadie/french-company-intelligence-mcp,yannabadie/eu-public-tenders-ted-boamp,yannabadie/clinical-trials-api-mcp,yannabadie/npi-healthcare-providers-mcp,yannabadie/pubmed-europepmc-api-mcp",
      "headers": {
        "Authorization": "Bearer ${APIFY_TOKEN}"
      }
    }
  }
}
```

---

## 3. Zero-Dependency Python CLI (`examples/quickstart_cli.py`)

```bash
export APIFY_TOKEN="your_apify_token"

# Preview exact match count for FREE (0 per-record charges)
python3 examples/quickstart_cli.py french-companies --postal-code 75008 --qualiopi --mode count
python3 examples/quickstart_cli.py clinical-trials --condition diabetes --phases PHASE3 --mode count

# Extract live EU + French IT procurement tenders with buyer contacts
python3 examples/quickstart_cli.py eu-tenders --countries FRA,DEU --cpv 72 --max 10
```

---

## License
MIT — free to fork, self-host, and adapt inside commercial n8n, Python, or AI agent pipelines.
