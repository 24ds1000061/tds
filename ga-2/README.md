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

## Question 9: Docker Hub
**Task:** Build and push a Docker image tagged with `24ds1000061`.
- **Dockerfile:** Created in `ga-2/q-9/`.
- **Workflow:** `.github/workflows/docker_q9.yml`.
- **Image URL:** [https://hub.docker.com/repository/docker/parasuramaniitm/tds-q9/general](https://hub.docker.com/repository/docker/parasuramaniitm/tds-q9/general)

## Question 10: Hugging Face Spaces (Docker SDK)
**Task:** Deploy a containerized API to Hugging Face Spaces.
- **Space Name:** `ga2-a34366`
- **SDK:** Docker
- **Config:** Port 7007, UID 1000 user.
- **Description:** Included `deployment-ready-ga2-a34366`.
- **URL:** [https://huggingface.co/spaces/ParasuramanIITM/ga2-a34366](https://huggingface.co/spaces/ParasuramanIITM/ga2-a34366)

## Question 11: Codespaces
**Task:** Create a devcontainer configuration.
- **Repo:** [https://github.com/24ds1000061/tds-ga-2-q-11](https://github.com/24ds1000061/tds-ga-2-q-11)
- **Status:** Configured with UV and Python.

## Question 12: GitHub Gist
**Task:** Publish a showcase using GitHub Gist with email verification.
- **Email Bypass:** Used `<!--email_off-->` tags in Markdown.
- **Status:** Prepared in `ga-2/q-12/showcase.md`.

## Question 13: FastAPI Student API
**Task:** Create a FastAPI server to serve student data from a CSV file with filtering and CORS.
- **Endpoint:** `/api`
- **Filtering:** Supports multi-class filtering via query params (e.g., `?class=1A&class=1B`).
- **Data Source:** `q-fastapi.csv`
- **Implementation:** `ga-2/q-13/main.py`
- **URL:** [http://127.0.0.1:8000/api](http://127.0.0.1:8000/api)

## Question 14: eShopCo Latency API (Vercel)
**Task:** Deploy a Python FastAPI endpoint on Vercel to process telemetry data.
- **Endpoint:** `POST /api`
- **Functionality:** Computes `avg_latency`, `p95_latency`, `avg_uptime`, and `breaches` for specified regions.
- **Implementation:** `ga-2/q-14/main.py`
- **Vercel Config:** `None (Auto-detect)`
- **URL:** [https://tds-ga2-q14-final.vercel.app/api/latency](https://tds-ga2-q14-final.vercel.app/api/latency) (Placeholder - please deploy from ga-2/q-14/)
