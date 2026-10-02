# Task 2: AI-Powered Financial Chatbot

## Purpose

This prototype is the BCG Forage GenAI Task 2 deliverable. It turns the Task 1 10-K analysis for Apple, Microsoft, and Tesla into an interactive chatbot that answers a defined set of financial questions.

The Forage brief asks for a simple prototype, not a production large-language-model application. This chatbot is therefore **rule-based**: it classifies the user question, looks up values from the analyzed dataset, and returns a written insight.

## Data source

`financial_data.csv` contains the same Task 1 metrics (US$ millions):

- Total revenue
- Net income
- Total assets
- Total liabilities
- Operating cash flow

Coverage: Apple, Microsoft, and Tesla for fiscal years 2023, 2024, and 2025.

## How the chatbot works

1. The user submits a question in the web UI or CLI.
2. The engine extracts company names, fiscal year, and metric keywords.
3. It classifies the intent:
   - metric lookup
   - year-over-year change
   - company comparison
   - profit margin
   - liabilities-to-assets ratio
   - company summary
   - help / greeting / unknown
4. It calculates the answer from the pandas dataset and returns a plain-language response.
5. Unrecognized questions receive a fallback that lists supported query types.

This design matches the simulation's emphasis on mapping predefined financial queries to reliable, data-backed responses.

## Supported query examples

- What is the total revenue?
- What is Apple's total revenue in 2025?
- How has net income changed over the last year?
- How has Tesla's net income changed over the last year?
- What are Microsoft's total assets?
- Compare the revenue of Apple, Microsoft, and Tesla
- What is the profit margin for Apple in 2025?
- What is the average liabilities/assets ratio?
- Summarize Tesla's financial performance

## How to run

Install dependencies from this folder:

```bash
pip install -r requirements.txt
```

Web chatbot:

```bash
python app.py
```

Then open `http://127.0.0.1:5000`.

Command-line chatbot:

```bash
python chatbot.py
```

Tests:

```bash
python -m pytest tests/test_chatbot.py -q
```

## Testing notes

Automated tests check revenue lookup, year-over-year net income change, company comparison, profit margin, the liabilities/assets ratio, help text, and unknown-query handling.

Limitations to mention in the Forage write-up:

- The bot answers only the financial metrics and companies in the Task 1 dataset.
- It does not call an external LLM.
- Fiscal year-ends differ by company, so combined-year totals are a reporting summary, not a synchronized calendar period.
