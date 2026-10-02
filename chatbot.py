"""Rule-based financial chatbot for the BCG Forage GenAI simulation.

Answers predefined questions about Apple, Microsoft, and Tesla using the
10-K metrics analyzed in Task 1. Amounts are US$ millions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).with_name("financial_data.csv")

METRIC_COLUMNS = {
    "revenue": "Total Revenue ($mm)",
    "total revenue": "Total Revenue ($mm)",
    "sales": "Total Revenue ($mm)",
    "net income": "Net Income ($mm)",
    "profit": "Net Income ($mm)",
    "earnings": "Net Income ($mm)",
    "assets": "Total Assets ($mm)",
    "total assets": "Total Assets ($mm)",
    "liabilities": "Total Liabilities ($mm)",
    "total liabilities": "Total Liabilities ($mm)",
    "cash flow": "Operating Cash Flow ($mm)",
    "operating cash flow": "Operating Cash Flow ($mm)",
    "operating cash": "Operating Cash Flow ($mm)",
}

METRIC_LABELS = {
    "Total Revenue ($mm)": "total revenue",
    "Net Income ($mm)": "net income",
    "Total Assets ($mm)": "total assets",
    "Total Liabilities ($mm)": "total liabilities",
    "Operating Cash Flow ($mm)": "operating cash flow",
}

COMPANY_ALIASES = {
    "apple": "Apple",
    "apples": "Apple",
    "aapl": "Apple",
    "microsoft": "Microsoft",
    "microsofts": "Microsoft",
    "msft": "Microsoft",
    "tesla": "Tesla",
    "teslas": "Tesla",
    "tsla": "Tesla",
}


@dataclass
class ChatResponse:
    reply: str
    intent: str


def load_financial_data(path: Path | None = None) -> pd.DataFrame:
    data = pd.read_csv(path or DATA_PATH)
    data["Fiscal Year"] = data["Fiscal Year"].astype(int)
    return data.sort_values(["Company", "Fiscal Year"]).reset_index(drop=True)


class FinancialChatbot:
    def __init__(self, data: pd.DataFrame | None = None) -> None:
        self.data = data if data is not None else load_financial_data()
        self.years = sorted(self.data["Fiscal Year"].unique())
        self.latest_year = max(self.years)
        self.companies = sorted(self.data["Company"].unique())

    def ask(self, message: str) -> str:
        return self.respond(message).reply

    def respond(self, message: str) -> ChatResponse:
        text = (message or "").strip()
        if not text:
            return ChatResponse(self._help_text("Please enter a question."), "empty")

        lowered = text.lower()
        companies = self._extract_companies(lowered)
        year = self._extract_year(lowered)
        metric = self._extract_metric(lowered)

        if self._is_greeting(lowered):
            return ChatResponse(self._greeting(), "greeting")
        if self._is_help(lowered):
            return ChatResponse(self._help_text(), "help")
        if "who are you" in lowered or "what can you" in lowered:
            return ChatResponse(self._help_text(), "help")
        if self._is_ratio(lowered):
            return ChatResponse(self._ratio_answer(companies, year), "ratio")
        if self._is_margin(lowered):
            return ChatResponse(self._margin_answer(companies, year), "margin")
        if self._is_compare(lowered):
            return ChatResponse(self._compare_answer(companies, year, metric), "compare")
        if self._is_change(lowered):
            return ChatResponse(self._change_answer(companies, year, metric), "yoy")
        if self._is_summary(lowered):
            return ChatResponse(self._summary_answer(companies), "summary")
        if metric:
            return ChatResponse(self._metric_answer(companies, year, metric), "metric")

        return ChatResponse(self._unknown(), "unknown")

    def supported_queries(self) -> list[str]:
        return [
            "What is the total revenue?",
            "What is Apple's total revenue in 2025?",
            "How has net income changed over the last year?",
            "How has Tesla's net income changed over the last year?",
            "What are Microsoft's total assets?",
            "Compare the revenue of Apple, Microsoft, and Tesla",
            "What is the profit margin for Apple in 2025?",
            "What is the average liabilities/assets ratio?",
            "Summarize Tesla's financial performance",
            "What is operating cash flow for Microsoft in 2024?",
        ]

    def _extract_companies(self, text: str) -> list[str]:
        found = []
        for alias, name in COMPANY_ALIASES.items():
            if re.search(rf"\b{re.escape(alias)}\b", text) and name not in found:
                found.append(name)
        if "all companies" in text or "all three" in text:
            return list(self.companies)
        return found

    def _extract_year(self, text: str) -> int | None:
        match = re.search(r"\b(20[0-9]{2})\b", text)
        if not match:
            return None
        year = int(match.group(1))
        return year if year in self.years else None

    def _extract_metric(self, text: str) -> str | None:
        for key in sorted(METRIC_COLUMNS, key=len, reverse=True):
            if key in text:
                return METRIC_COLUMNS[key]
        return None

    def _is_greeting(self, text: str) -> bool:
        return bool(re.fullmatch(r"(hi|hello|hey|good morning|good afternoon)[!?.]*", text))

    def _is_help(self, text: str) -> bool:
        return any(token in text for token in ("help", "example", "what can you do", "supported"))

    def _is_ratio(self, text: str) -> bool:
        return "ratio" in text or ("liabilit" in text and "asset" in text and "ratio" in text) or "liabilities/assets" in text

    def _is_margin(self, text: str) -> bool:
        return "margin" in text or "profitability" in text

    def _is_compare(self, text: str) -> bool:
        return any(token in text for token in ("compare", "comparison", "versus", " vs ", "highest", "lowest", "which company"))

    def _is_change(self, text: str) -> bool:
        return any(token in text for token in ("changed", "change", "growth", "grew", "increase", "decrease", "yoy", "year-over-year", "over the last year", "last year"))

    def _is_summary(self, text: str) -> bool:
        return any(token in text for token in ("summar", "overview", "trend", "insight", "performance"))

    def _greeting(self) -> str:
        return (
            "Hello. I am a financial analysis chatbot covering Apple, Microsoft, and Tesla "
            f"for fiscal years {self.years[0]}-{self.years[-1]}. "
            "Ask about revenue, net income, assets, liabilities, operating cash flow, "
            "year-over-year changes, profit margins, or comparisons. Type 'help' for examples."
        )

    def _help_text(self, prefix: str | None = None) -> str:
        examples = "\n".join(f"- {query}" for query in self.supported_queries())
        body = (
            "I answer predefined financial questions using the Task 1 10-K dataset "
            f"(Apple, Microsoft, Tesla; FY {self.years[0]}-{self.years[-1]}; figures in US$ millions).\n\n"
            f"Example questions:\n{examples}"
        )
        return f"{prefix}\n\n{body}" if prefix else body

    def _unknown(self) -> str:
        return (
            "I could not map that question to a supported financial query. "
            "Try asking about total revenue, net income, assets, liabilities, "
            "operating cash flow, year-over-year change, profit margin, or a company comparison. "
            "Type 'help' to see examples."
        )

    def _resolve_companies(self, companies: list[str]) -> list[str]:
        return companies or list(self.companies)

    def _resolve_year(self, year: int | None) -> int:
        return year or self.latest_year

    def _value(self, company: str, year: int, metric: str) -> float:
        row = self.data[(self.data["Company"] == company) & (self.data["Fiscal Year"] == year)]
        if row.empty:
            raise KeyError(f"No data for {company} in {year}")
        return float(row.iloc[0][metric])

    def _prior_year(self, year: int) -> int | None:
        earlier = [item for item in self.years if item < year]
        return max(earlier) if earlier else None

    def _format_amount(self, value: float) -> str:
        return f"${value:,.0f} million"

    def _format_pct(self, value: float) -> str:
        return f"{value:+.2f}%"

    def _yoy(self, company: str, year: int, metric: str) -> float | None:
        prior = self._prior_year(year)
        if prior is None:
            return None
        current = self._value(company, year, metric)
        previous = self._value(company, prior, metric)
        if previous == 0:
            return None
        return (current / previous - 1) * 100

    def _metric_answer(self, companies: list[str], year: int | None, metric: str) -> str:
        companies = self._resolve_companies(companies)
        year = self._resolve_year(year)
        label = METRIC_LABELS[metric]
        lines = [f"{company}'s {label} in FY {year} was {self._format_amount(self._value(company, year, metric))}." for company in companies]
        if len(companies) > 1:
            total = sum(self._value(company, year, metric) for company in companies)
            lines.append(f"Combined {label} in FY {year} was {self._format_amount(total)}.")
        return " ".join(lines)

    def _change_answer(self, companies: list[str], year: int | None, metric: str | None) -> str:
        companies = self._resolve_companies(companies)
        year = self._resolve_year(year)
        metric = metric or "Net Income ($mm)"
        label = METRIC_LABELS[metric]
        prior = self._prior_year(year)
        if prior is None:
            return f"FY {year} is the first year in the dataset, so a year-over-year change is not available."

        parts = []
        for company in companies:
            change = self._yoy(company, year, metric)
            current = self._value(company, year, metric)
            previous = self._value(company, prior, metric)
            if change is None:
                parts.append(f"{company}: year-over-year {label} change is unavailable.")
                continue
            direction = "increased" if change > 0 else "decreased" if change < 0 else "was unchanged"
            parts.append(
                f"{company}'s {label} {direction} from {self._format_amount(previous)} in FY {prior} "
                f"to {self._format_amount(current)} in FY {year} ({self._format_pct(change)})."
            )
        return " ".join(parts)

    def _compare_answer(self, companies: list[str], year: int | None, metric: str | None) -> str:
        companies = self._resolve_companies(companies)
        year = self._resolve_year(year)
        metric = metric or "Total Revenue ($mm)"
        label = METRIC_LABELS[metric]
        ranked = sorted(
            ((company, self._value(company, year, metric)) for company in companies),
            key=lambda item: item[1],
            reverse=True,
        )
        ranking = ", ".join(f"{company} {self._format_amount(value)}" for company, value in ranked)
        leader, leader_value = ranked[0]
        return (
            f"FY {year} {label} comparison: {ranking}. "
            f"{leader} reported the highest {label} at {self._format_amount(leader_value)}."
        )

    def _margin_answer(self, companies: list[str], year: int | None) -> str:
        companies = self._resolve_companies(companies)
        year = self._resolve_year(year)
        parts = []
        for company in companies:
            revenue = self._value(company, year, "Total Revenue ($mm)")
            income = self._value(company, year, "Net Income ($mm)")
            margin = (income / revenue) * 100
            parts.append(
                f"{company}'s net profit margin in FY {year} was {margin:.2f}% "
                f"(net income {self._format_amount(income)} on revenue {self._format_amount(revenue)})."
            )
        return " ".join(parts)

    def _ratio_answer(self, companies: list[str], year: int | None) -> str:
        year = self._resolve_year(year)
        selected = self._resolve_companies(companies)
        ratios = []
        parts = []
        for company in selected:
            assets = self._value(company, year, "Total Assets ($mm)")
            liabilities = self._value(company, year, "Total Liabilities ($mm)")
            ratio = liabilities / assets
            ratios.append(ratio)
            parts.append(f"{company}: {ratio:.2%} ({self._format_amount(liabilities)} liabilities / {self._format_amount(assets)} assets)")
        average = sum(ratios) / len(ratios)
        intro = (
            f"Liabilities-to-assets ratios in FY {year}: {'; '.join(parts)}. "
            f"Average ratio across {', '.join(selected)}: {average:.2%}."
        )
        return intro

    def _summary_answer(self, companies: list[str]) -> str:
        companies = self._resolve_companies(companies)
        first, last = self.years[0], self.years[-1]
        metric = "Total Revenue ($mm)"
        parts = []
        for company in companies:
            start = self._value(company, first, metric)
            end = self._value(company, last, metric)
            growth = (end / start - 1) * 100
            latest_income = self._value(company, last, "Net Income ($mm)")
            latest_cf = self._value(company, last, "Operating Cash Flow ($mm)")
            parts.append(
                f"{company}: revenue moved from {self._format_amount(start)} in FY {first} "
                f"to {self._format_amount(end)} in FY {last} ({self._format_pct(growth)}). "
                f"FY {last} net income was {self._format_amount(latest_income)} and operating cash flow was {self._format_amount(latest_cf)}."
            )
        return " ".join(parts)


def run_cli() -> None:
    bot = FinancialChatbot()
    print(bot._greeting())
    print("Type 'help' for examples or 'exit' to quit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        print(f"Bot: {bot.ask(user_input)}\n")


if __name__ == "__main__":
    run_cli()
