# Official Open-Data & Web Intelligence MCP & n8n Templates (9 Actors, 9 Workflows)

Ready-to-import, **n8n Creator-ready workflow templates** (each with canvas sticky notes, validation filters, idempotent Google Sheets upserts & zero hardcoded secrets), **Claude / Cursor / Antigravity MCP config (`mcp.json`)**, and a **zero-dependency Python CLI** covering **9 deterministic, zero-proxy Apify Actors** across EU/U.S. government open data, biomedical registries, B2B hiring/enrichment, newsletters, and media sentiment.

---

## Included Registries, Intelligence Feeds & Actors (9 Pay-Per-Event + MCP Actors, All `256 MB` RAM)

| Domain / Suite | Upstream Public APIs & Sources | Highlights | Apify Actor (Pay-Per-Event + MCP) |
|---|---|---|---|
| **French Companies & KYC** | DINUM/INSEE/INPI SIRENE/RNE + DILA BODACC + BOAMP | **FREE `count` mode**, GPS radius (`/near_point`), RGE/Qualiopi/Bio/ESS filters, EU VAT & opt-in insolvency KYC (`$6 / 1,000`) | [`yannabadie/french-company-intelligence-mcp`](https://apify.com/yannabadie/french-company-intelligence-mcp) |
| **EU & France Public Tenders** | EU TED Search API v3 (27 countries) + French BOAMP | Direct **buyer email, phone & website**, award winners, `minValueEur`, `deadlineAfter` & TED Expert Query (`$3–$4 / 1,000`) | [`yannabadie/eu-public-tenders-ted-boamp`](https://apify.com/yannabadie/eu-public-tenders-ted-boamp) |
| **Global Clinical Trials** | U.S. NIH ClinicalTrials.gov REST API v2 (500k+ studies) | **FREE `count` mode**, paste ClinicalTrials.gov URLs or NCT IDs, central & site contact emails/phones & `updatedSince` watch (`$5 / 1,000`) | [`yannabadie/clinical-trials-api-mcp`](https://apify.com/yannabadie/clinical-trials-api-mcp) |
| **U.S. Doctors & Clinics (NPI)** | U.S. CMS NPPES NPI Registry API v2.1 (8M+ providers) | **Flat `$2.50 / 1,000` all-inclusive** (zero phone surcharge), FREE `count` mode, practice phones/fax & Authorized Officials | [`yannabadie/npi-healthcare-providers-mcp`](https://apify.com/yannabadie/npi-healthcare-providers-mcp) |
| **PubMed & Europe PMC Papers** | EMBL-EBI Europe PMC & PubMed REST API (37M+ papers) | **100% untruncated abstracts**, author emails, ORCIDs, citations, MeSH, grants, linked NCT trials & **free PDF URLs** (`$2 / 1,000`, FREE `count`) | [`yannabadie/pubmed-europepmc-api-mcp`](https://apify.com/yannabadie/pubmed-europepmc-api-mcp) |
| **Multi-ATS Career Jobs** | Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee & Workday CXS | **7 zero-key public ATS JSON APIs**, FREE `count` & `detect_boards` modes, hybrid salary extraction (`$3 / 1,000`) | [`yannabadie/multi-ats-jobs-api-mcp`](https://apify.com/yannabadie/multi-ats-jobs-api-mcp) |
| **Substack Newsletters & Rankings** | Substack Public JSON APIs (cursor-paginated archive, leaderboards, search) | Full plain-text posts, paywall flags, likes/comments/restacks, **6 leaderboard tabs** & FREE `count` (`$1.50 / 1,000`) | [`yannabadie/substack-api-mcp`](https://apify.com/yannabadie/substack-api-mcp) |
| **Website Contacts & Tech Stack** | Direct polite async HTTP crawl (homepage + `/contact`, `/mentions-legales`, `/about`) | Role-ranked emails, EU/US phones, 7 socials, **54 structural tech-stack signatures**, SSRF guard & FREE `count` (`$1.50 / 1,000`) | [`yannabadie/website-contact-tech-enricher-mcp`](https://apify.com/yannabadie/website-contact-tech-enricher-mcp) |
| **Google News & GDELT Sentiment** | Google News RSS (multi-country) + GDELT Project v2 DOC & `ToneChart` APIs | Deduplicated headlines, canonical URLs, article images, **media sentiment tone scores** & FREE `count` (`$2 / 1,000`) | [`yannabadie/google-news-gdelt-api-mcp`](https://apify.com/yannabadie/google-news-gdelt-api-mcp) |

> Prefer a **zero-API-key local stdio MCP server** (also live in the Official MCP Registry `io.github.yannabadie/eu-us-opendata-mcp`) for quick interactive lookups in Claude/Cursor? See [`yannabadie/eu-us-opendata-mcp`](https://github.com/yannabadie/eu-us-opendata-mcp).

*Free Apify accounts include `$5/month` of usage credits — enough to run ~800–3,000 records/month for free.*

---

## 1. Ready-to-Import n8n Templates (`workflows/` — 9 Creator-Ready JSONs)

Every workflow includes 2 canvas Sticky Notes (setup & deduplication notes), validation `Filter` / `Set` nodes, zero hardcoded secrets (`$env.APIFY_TOKEN` / `$env.SLACK_WEBHOOK_URL`), and idempotent Google Sheets `appendOrUpdate` matching keys:

1. **[`workflows/n8n_eu_public_tenders_slack_sheets.json`](workflows/n8n_eu_public_tenders_slack_sheets.json)**
   - Daily 08:00 trigger -> EU TED v3 + French BOAMP tenders (with `buyerEmail` & `buyerPhone`) -> Google Sheets (`tenderId` upsert) + Slack alerts.
2. **[`workflows/n8n_french_company_kyc_enrichment.json`](workflows/n8n_french_company_kyc_enrichment.json)**
   - Webhook taking a SIREN list -> enriches SIRENE/RNE + EU VAT + BODACC insolvency notices -> routes `high_risk` / `closed` entities to Slack compliance alerts.
3. **[`workflows/n8n_clinical_trials_sponsor_watch.json`](workflows/n8n_clinical_trials_sponsor_watch.json)**
   - Daily 08:00 trigger -> updated Phase 2/3 industry clinical trials -> Google Sheets (`nctId` upsert) + Slack pharma pipeline alerts.
4. **[`workflows/n8n_us_npi_healthcare_leads_sheets.json`](workflows/n8n_us_npi_healthcare_leads_sheets.json)**
   - U.S. CMS NPI Registry API v2.1 (`NPI-2` clinics & group practices with phone) -> `Filter` -> Google Sheets (`npi` upsert with phones, fax & Authorized Officials).
5. **[`workflows/n8n_pubmed_kol_literature_watch.json`](workflows/n8n_pubmed_kol_literature_watch.json)**
   - Weekly Monday 08:00 trigger -> PubMed & Europe PMC (`onlyWithEmail: true`, `hasFreePdf: true`) -> Google Sheets (`PMID` upsert) + Slack KOL alerts.
6. **[`workflows/n8n_multi_ats_jobs_hiring_signals.json`](workflows/n8n_multi_ats_jobs_hiring_signals.json)**
   - Daily 08:00 trigger -> queries 7 public ATS engines (`multi-ats-jobs-api-mcp`) -> formats B2B hiring signals -> Google Sheets (`recordKey` upsert) + Slack alerts.
7. **[`workflows/n8n_substack_newsletter_intelligence.json`](workflows/n8n_substack_newsletter_intelligence.json)**
   - Daily 08:00 trigger -> monitors target Substack publications (`substack-api-mcp`) -> computes engagement score -> Google Sheets (`recordKey` upsert) + Slack alerts.
8. **[`workflows/n8n_website_contact_tech_enrichment.json`](workflows/n8n_website_contact_tech_enrichment.json)**
   - POST Webhook taking a domain list -> enriches emails, phones, socials & 54 tech-stack signatures (`website-contact-tech-enricher-mcp`) -> flattens arrays -> Google Sheets (`domain` upsert).
9. **[`workflows/n8n_google_news_gdelt_brand_monitor.json`](workflows/n8n_google_news_gdelt_brand_monitor.json)**
   - Daily 08:00 trigger -> merges Google News RSS + GDELT v2 sentiment (`google-news-gdelt-api-mcp`) -> tags sentiment tone -> Google Sheets (`recordKey` upsert) + Slack brand alerts.

### Import into n8n (60 seconds)
1. Download any `.json` file from `workflows/` and click **Import from File** in n8n.
2. Add `APIFY_TOKEN` (and optional `SLACK_WEBHOOK_URL`) to your n8n environment variables.
3. Replace `REPLACE_WITH_GOOGLE_SHEET_ID`, customize filters, run a manual test, and activate.

---

## 2. Connect All 9 Actors to Claude Code, Cursor, or Antigravity via MCP (`mcp/mcp.json`)

Drop [`mcp/mcp.json`](mcp/mcp.json) into your MCP client configuration (set `APIFY_TOKEN`):

```json
{
  "mcpServers": {
    "apify-official-opendata": {
      "url": "https://mcp.apify.com/?actors=yannabadie/french-company-intelligence-mcp,yannabadie/eu-public-tenders-ted-boamp,yannabadie/clinical-trials-api-mcp,yannabadie/npi-healthcare-providers-mcp,yannabadie/pubmed-europepmc-api-mcp,yannabadie/multi-ats-jobs-api-mcp,yannabadie/substack-api-mcp,yannabadie/website-contact-tech-enricher-mcp,yannabadie/google-news-gdelt-api-mcp",
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
