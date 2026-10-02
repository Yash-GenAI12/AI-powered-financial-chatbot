from chatbot import FinancialChatbot

QUERIES = [
    "What is the total revenue?",
    "What is Apple's total revenue in 2025?",
    "How has net income changed over the last year?",
    "How has Tesla's net income changed over the last year?",
    "Compare the revenue of Apple, Microsoft, and Tesla",
    "What is the profit margin for Apple in 2025?",
    "What is the average liabilities/assets ratio?",
    "Summarize Tesla's financial performance",
    "What is the weather in Boston?",
]


def main() -> None:
    bot = FinancialChatbot()
    blocks = [f"You: {query}\nBot: {bot.ask(query)}" for query in QUERIES]
    with open("test_results.txt", "w", encoding="utf-8") as handle:
        handle.write("\n\n".join(blocks) + "\n")


if __name__ == "__main__":
    main()
