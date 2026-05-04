# Hockey Teams Scraper (Playwright)

## Overview

This project is a **web scraper** built using Playwright (Python).

It extracts hockey team statistics from:
   https://www.scrapethissite.com/pages/

### Workflow:

1. Navigate to **Hockey Teams: Forms, Searching and Pagination**
2. Search for **New York Rangers**
3. Scrape data across **all pages (pagination supported)**
4. Compute:
   * Total Wins
   * Total Losses
   * Total Goals Scored
   * Total Goals Against
5. Generate **year-wise performance**
6. Save structured output as **JSON**
   
---

##  Features

* Handles **single-page & multi-page** scenarios automatically
* **Pagination support** (Next button detection)
* **Graceful error handling** (no crashes)
* **Step-wise screenshots** (for proof/debugging)
* **Detailed logging**
* Clean, modular **class-based design**

---

## Tech Stack

* Python
* Playwright (Sync API)
* Logging module
* JSON

---

##  Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/hockey-scraper.git
cd hockey-scraper
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

---

## ▶️ Run the Scraper

```bash
python HockeyScraper.py
```

---

## Output

### Result JSON

```bash
output/result.json
```

### Example:

```json
{
  "team": "New York Rangers",
  "totals": {
    "wins": 1800,
    "losses": 1500,
    "goals_scored": 8634,
    "goals_against": 8200
  },
  "yearly_performance": [
    {
      "year": 2001,
      "wins": 36,
      "losses": 38,
      "goals_scored": 227,
      "goals_against": 258
    },
    .
    .
    .
  ],
  "status": "success"
}
```

---

## Screenshots (Proof)

All screenshots are stored in:

```bash
output/screenshots/
```

### Captured at each step:

* Homepage load
* Navigation to hockey page
* Search execution
* Each pagination page
* Error states (if any)

 Useful for:

* Debugging
* Proof of execution
* UI change tracking

---

## Logging

Logs are stored in:

```bash
output/scraper.log
```

### Example logs:

```
2026-05-04 10:20:11 [INFO] STEP: 01_home
2026-05-04 10:20:14 [INFO] Processing Page: 1
2026-05-04 10:20:18 [INFO] Processing Page: 2
```

### Benefits:

* Tracks execution flow
* Helps debug failures
* Captures errors and warnings

---

##  Error Handling

* Script **does not crash**
* Returns structured JSON even on failure

Example:

```json
{
  "status": "failed",
  "error": ""
}
```

---
