# MLE Take-Home: Merchant Underwriting Pipeline & Risk Report

**Time budget:** ~8 hours  
**Role:** Machine Learning Engineer (BNPL / Merchant Underwriting)

---

## Context

Our team underwrites merchants for BNPL (Buy Now Pay Later). We need to (a) pull data from several sources, (b) turn it into a consistent questionnaire-style input for underwriting, (c) estimate dispute/counterparty risk with a small model, and (d) produce a concise report for the risk team.

**Philosophy:** Risk is acceptable if it is **priced**—i.e. understood and quantified. We care about merchant shortchanging the customer (leading to dispute loss) and counterparty risk on the full portfolio.

---

## Your Task

Build a **minimal but production-style** pipeline that:

1. **Ingests** all data sources below (with validation and basic governance).
2. **Collates** them into a single structured view (questionnaire-style input for underwriting).
3. **Trains** a simple risk model (e.g. high dispute risk or expected dispute count).
4. **Aggregates** to a portfolio-level risk view (e.g. expected high-risk count or simple expected loss).
5. **Uses an LLM** to generate a short underwriting report for the risk team from the collated data and model outputs.

Document how you used AI (prompts, models, conversations) and be ready to **walk through your solution live** (30–45 min).

---

## Data Sources (all required)

### 1. Simulated API (you implement)

Implement at least one small **mock API** (e.g. Flask or FastAPI) that returns merchant-like data. The contract you must satisfy is in [`data/simulated_api_contract.json`](data/simulated_api_contract.json). Your pipeline must call this API (you run it locally) and consume the response. The API should return data such as internal risk flags or transaction summary per merchant.

### 2. Real public API(s) (you integrate)

- **REST Countries** (keyless): `https://restcountries.com/v3.1/name/{country}` or `/alpha/{code}` — use this to enrich merchant **country/region** (e.g. region, subregion). Handles rate limits and errors.
- **Companies House (UK), optional:** If you have time, register for a free API key at [Companies House](https://developer.company-information.service.gov.uk/get-started) and, for merchants with a UK `registration_number`, fetch company profile (e.g. company name, status, incorporation date). If you cannot obtain a key in time, document a fallback (e.g. mock response or skip with a clear note).

Use **at least one** real public API (REST Countries is sufficient; Companies House is optional).

### 3. CSV (we provide)

Ingest [`data/merchants.csv`](data/merchants.csv). Validate its schema (columns: `merchant_id`, `name`, `country`, `registration_number`, `monthly_volume`, `dispute_count`, etc.). Reject or log invalid rows.

### 4. PDF (async)

We provide a sample PDF: [`data/sample_merchant_summary.pdf`](data/sample_merchant_summary.pdf) (short merchant terms/summary). You must:

- Ingest and process it **asynchronously** (e.g. background job, queue, or `async` function with a comment that in production this would be a proper job).
- Extract text (and optionally structure) and include it in the collated view or report context.

### 5. Scrape: claritypay.com

Scrape **claritypay.com** (real public site). Scope:

- Extract into a **structured format** (e.g. JSON or dict):
  - Main value propositions (e.g. “Pay over time”, “Clear terms”).
  - Partner names (e.g. from logos or “Proud Partner” sections).
  - Any public stats (e.g. “1900+ Merchants”, “$1.2B+ Credit Issued”, “305K Monthly Transactions”).

Be **respectful**: rate limit requests, set a clear User-Agent, do not hammer the site. If the site structure changes, document what you attempted and any fallbacks.

---

## Pipeline and governance requirements

- **Ingestion:** Clear separation of fetch → parse → validate for each source.
- **Collation:** One structured dataset (e.g. one row per merchant) with normalized fields from all sources.
- **Governance / checks:**
  - **Schema validation** (e.g. Pydantic, JSON Schema, or pandas schema) on ingested and collated data.
  - **Idempotency:** Document how you would make this pipeline idempotent in production.
  - **Logging:** Log when a source fails, when validation fails, and key pipeline steps.
  - **Tests:** At least a few unit tests (e.g. validation logic, one ingestion path).
- **Features:** From collated data, derive features for the risk model (e.g. dispute rate, volume band, geography). Document assumptions.
- **Model:** Train a simple model (e.g. logistic regression or small tree) to predict a risk target (e.g. high dispute risk or expected dispute count). Clear train/eval split; no heavy tuning required.
- **Portfolio:** One portfolio-level step (e.g. expected number of high-risk merchants or simple expected loss).
- **LLM report:** Use an LLM (OpenAI, Anthropic, local, etc.) to **generate** a short underwriting report (1–2 pages) for the risk team: summary of merchants, key risk factors, model-based risk bands, red flags. The report must be produced by the LLM from pipeline outputs, not a static template. Document the prompts you use.

---

## Deliverables

1. **Code**
   - Repo with a clear structure (e.g. `ingestion/`, `features/`, `model/`, `reporting/`, `tests/`).
   - README: how to run the pipeline, required env vars, and how to run tests.

2. **Short written report**
   - Assumptions, trade-offs, and what you would do next for production (monitoring, retraining, governance).

3. **Live walkthrough**
   - 30–45 min: run the pipeline, show data flow, model, and LLM report; discuss design choices and how you’d harden it.

4. **AI usage document**
   - How you used AI: which models, which prompts (paste key prompts), which conversations (e.g. “Used Claude to design the schema”), and for what (coding, report drafting, debugging). We want transparency and thoughtful use.

---

## Suggested repo structure (optional)

```
data/           # merchants.csv, sample PDF, simulated API contract
ingestion/      # clients for CSV, PDF, APIs, scrape; validation
features/       # feature construction from collated data
model/          # training script, portfolio aggregation
reporting/      # LLM prompt + report generation
tests/          # unit tests
docs/ or root   # AI_USAGE.md (or similar)
```

---

## Evaluation (what we look at)

- **Code quality:** Structure, naming, minimal tech debt.
- **Governance / checks:** Schema validation, logging, tests, idempotency consideration.
- **Data pipeline:** All five sources wired; PDF processed asynchronously.
- **Model:** Simple but correct; clear features and target; portfolio aggregation.
- **LLM report:** Generated by an LLM from pipeline outputs; prompts documented.
- **Ecosystem:** Understanding of BNPL/underwriting, dispute risk, and “risk is ok if priced”.
- **AI usage:** Honest, detailed documentation; sensible and ethical use.

Good luck. We’re excited to see your solution.
