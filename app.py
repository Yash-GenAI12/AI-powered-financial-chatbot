"""Flask UI for the BCG Forage financial chatbot."""

from flask import Flask, jsonify, render_template, request

from chatbot import FinancialChatbot

app = Flask(__name__)
bot = FinancialChatbot()


@app.get("/")
def index():
    return render_template(
        "index.html",
        companies=", ".join(bot.companies),
        years=f"{bot.years[0]}-{bot.years[-1]}",
        examples=bot.supported_queries(),
    )


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")
    result = bot.respond(message)
    return jsonify({"reply": result.reply, "intent": result.intent})


if __name__ == "__main__":
    app.run(debug=True)
