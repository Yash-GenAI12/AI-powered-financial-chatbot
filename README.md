# BCG GenAI Virtual Internship

**10-K financial analysis and a rule-based financial chatbot for Apple, Microsoft, and Tesla.**

This repository is my submission for the [BCG GenAI job simulation on Forage](https://www.theforage.com/). It includes:

1. **Task 1** — pandas analysis of selected 10-K metrics (FY 2023–2025)
2. **Task 2** — an interactive chatbot that answers a defined set of financial questions from that dataset

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-data%20analysis-150458?logo=pandas&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-web%20UI-000000?logo=flask&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-notebook-F37626?logo=jupyter&logoColor=white)

> Amounts are in **US$ millions**. The chatbot is **rule-based** (not an LLM). It maps predefined queries to values in `financial_data.csv` so answers stay consistent and auditable.

---

## Table of contents

- [Features](#features)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [Task 1: 10-K financial analysis](#task-1-10-k-financial-analysis)
- [Task 2: Financial chatbot](#task-2-financial-chatbot)
- [Supported questions](#supported-questions)
- [Tests](#tests)
- [Limitations](#limitations)

---

## Features

- Structured 10-K dataset for **Apple**, **Microsoft**, and **Tesla**
- Year-over-year percentage changes for revenue, net income, assets, liabilities, and operating cash flow
- Web chatbot (Flask) and command-line chatbot
- Intents: metric lookup, YoY change, company comparison, profit margin, liabilities-to-assets ratio, company summary
- Fallback help text when a question is outside the supported set
- Automated tests for the main query types

---

## Project structure

```text
.
├── README.md
├── 10K_Financial_Analysis_Microsoft_Tesla_Apple_Executed.ipynb
└── financial_chatbot/
    ├── app.py                      # Flask web app
    ├── chatbot.py                  # Rule-based engine
    ├── chatbot_documentation.md    # Task 2 write-up
    ├── financial_data.csv          # Analyzed metrics (US$ millions)
    ├── requirements.txt
    ├── templates/
    │   └── index.html
    └── tests/
        └── test_chatbot.py
```

---

## Getting started

### Prerequisites

- Python 3.10 or later
- pip

### Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

Replace `<your-username>` and `<your-repo-name>` with your GitHub username and repository name.

### Install chatbot dependencies

```bash
cd financial_chatbot
pip install -r requirements.txt
```

`requirements.txt` includes `pandas`, `flask`, and `pytest`. For the analysis notebook, also install Jupyter if needed:

```bash
pip install jupyter pandas
```

---

## Task 1: 10-K financial analysis

Notebook: [`10K_Financial_Analysis_Microsoft_Tesla_Apple_Executed.ipynb`](10K_Financial_Analysis_Microsoft_Tesla_Apple_Executed.ipynb)

The notebook:

- Loads the supplied 10-K metrics into a pandas DataFrame
- Calculates year-over-year changes **within each company**
- Reviews aggregate reported totals across the three companies
- Documents methodology and observations

Open it with:

```bash
jupyter notebook "10K_Financial_Analysis_Microsoft_Tesla_Apple_Executed.ipynb"
```

**Fiscal year-ends differ** (Apple: September, Microsoft: June, Tesla: December). Combined-year totals are a reporting summary, not a synchronized calendar period.

---

## Task 2: Financial chatbot

The user asks a question in the web UI or CLI. The engine extracts company, year, and metric keywords, classifies the intent, looks up values in [`financial_chatbot/financial_data.csv`](financial_chatbot/financial_data.csv), and returns a plain-language answer.

### Web UI

From the `financial_chatbot` folder:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

### Command line

```bash
python chatbot.py
```

---

## Supported questions

| Type | Example |
|------|---------|
| Metric lookup | What is Apple's total revenue in 2025? |
| Default latest year | What is the total revenue? |
| Year-over-year change | How has Tesla's net income changed over the last year? |
| Comparison | Compare the revenue of Apple, Microsoft, and Tesla |
| Profit margin | What is the profit margin for Apple in 2025? |
| Ratio | What is the average liabilities/assets ratio? |
| Summary | Summarize Tesla's financial performance |

Unrecognized questions receive a fallback that lists supported query types.

---

## Tests

From the `financial_chatbot` folder:

```bash
python -m pytest tests/test_chatbot.py -q
```

Tests cover revenue lookup, YoY net income change, company comparison, profit margin, liabilities/assets ratio, help text, and unknown-query handling.

---

## Limitations

- Answers only the companies, years, and metrics in the Task 1 dataset
- Does not call an external large language model
- Fiscal year-ends are not aligned across companies
- This is a **prototype** for the Forage simulation, not a production product

For a fuller Task 2 write-up, see [`financial_chatbot/chatbot_documentation.md`](financial_chatbot/chatbot_documentation.md).

---

## Acknowledgement

Built as part of the **BCG — Introduction to Generative AI** job simulation on [Forage](https://www.theforage.com/).
