from chatbot import FinancialChatbot


def test_revenue_lookup():
    bot = FinancialChatbot()
    reply = bot.ask("What is Apple's total revenue in 2025?")
    assert "Apple" in reply
    assert "394,320" in reply
    assert "FY 2025" in reply


def test_net_income_change():
    bot = FinancialChatbot()
    reply = bot.ask("How has Tesla's net income changed over the last year?")
    assert "Tesla" in reply
    assert "16.13%" in reply
    assert "17,420" in reply


def test_company_comparison():
    bot = FinancialChatbot()
    reply = bot.ask("Compare the revenue of Apple, Microsoft, and Tesla")
    assert "Apple" in reply and "Microsoft" in reply and "Tesla" in reply
    assert "highest" in reply.lower()


def test_profit_margin():
    bot = FinancialChatbot()
    reply = bot.ask("What is the profit margin for Apple in 2025?")
    assert "profit margin" in reply.lower()
    assert "Apple" in reply


def test_liabilities_assets_ratio():
    bot = FinancialChatbot()
    reply = bot.ask("What is the average liabilities/assets ratio?")
    assert "Average ratio" in reply
    assert "Apple" in reply


def test_unknown_query():
    bot = FinancialChatbot()
    result = bot.respond("What is the weather in Boston?")
    assert result.intent == "unknown"
    assert "help" in result.reply.lower() or "supported" in result.reply.lower()


def test_help_lists_examples():
    bot = FinancialChatbot()
    reply = bot.ask("help")
    assert "What is the total revenue?" in reply
