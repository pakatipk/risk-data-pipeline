# risk-data-pipeline
 Automated risk ticket extractor and cleaner for Jira and Airtable. Includes QA logic and Looker Studio integration-ready output.

## 📦 Features

- 🔗 Pulls risk tickets from **Jira Cloud API** (historical tickets)
- 📥 Supports **Airtable API** integration for current assessments
- 🧹 Includes data QA logic to flag:
  - Missing/resolved date mismatches
  - Incomplete resolutions
  - Invalid or inconsistent status values
- 🔁 Merges both datasets with standardized schema
- 📤 Outputs to `CSV` or `Google Sheets` for use in **Looker Studio**
- ⚙️ Fully automated with **GitHub Actions** scheduler
