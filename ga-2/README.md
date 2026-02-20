# TDS GA-2 Assignment Solutions

## Question 2: Git History Rewriting
**Task:** Purge a sensitive `.env` file from the entire Git history and implement best practices.
- **Identify:** Found `.env` added in commit `746a240`.
- **Purge:** Executed `git filter-branch --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --all`.
- **Cleanup:** Removed backup refs (`refs/original/`) and ran `git gc --prune=now --aggressive`.
- **Security:** Added `.gitignore` to block `.env` and created `.env.example` with placeholders.
- https://github.com/24ds1000061/tds-ga-2-git-revert-env

## Question 3: Git History Exploration
**Task:** Identify the 7-character short hash of the parent of the commit that set `timeout` to `90` in `config.json`.
- **Search:** Found the change in commit `c015716` ("Update timeout settings").
- **Parent:** Checked parent using `git log -1 --format=%P c015716`.
- **Answer:** The parent commit short hash is **`06d25d2`**.
## Question 4: Git page
**Task:** git pages
- **Result:** [GA-2 Showcase Page](https://24ds1000061.github.io/TDS/ga-2/q-4/)

## Question 5: Static API (StaticShop)
**Task:** Create a static JSON product catalog hosted on GitHub Pages.
- **Metadata:** Included email and version `3c99b79e`.
- **Products:** Populated 17 products with IDs, categories, and pricing.
- **Aggregations:** Computed category-level stats.
  - **Sports:** Count: 1, Inventory Value: **29180.97**.
- **URL:** [https://24ds1000061.github.io/TDS/ga-2/q-5/products.json](https://24ds1000061.github.io/TDS/ga-2/q-5/products.json)

## Question 6: GitHub Actions
**Task:** Create a GitHub action where a step name contains your email address.
- **Workflow:** Created `.github/workflows/verify_email.yml`.
- **Step Name:** `24ds1000061@ds.study.iitm.ac.in`.
- **Repo URL:** [https://github.com/24ds1000061/TDS](https://github.com/24ds1000061/TDS)

## Question 7: CI Caching
**Task:** Speed up CI with GitHub Actions caching using `actions/cache@v4`.
- **Workflow:** Created `.github/workflows/cache_check.yml`.
- **Cache Key:** `cache-5d24ba9`.
- **Step Name:** `prime-cache-5d24ba9` (echoes cache status).
- **Repo URL:** [https://github.com/24ds1000061/TDS](https://github.com/24ds1000061/TDS)

## Question 8: Dependabot
**Task:** Configure Dependabot for automatic dependency updates.
- **Project Type:** Python (pip).
- **Files:** Created `requirements.txt` and `.github/dependabot.yml`.
- **Config:** Weekly updates for the root directory with `deps` prefix.
- **Repo URL:** [https://github.com/24ds1000061/TDS](https://github.com/24ds1000061/TDS)
