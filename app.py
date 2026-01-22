from flask import Flask, render_template, request, jsonify
import os
import requests
import json

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))


@app.route("/")
def home():
    return render_template("ChatBot.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    bot_response = None
    last_error = None
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "model": "xiaomi/mimo-v2-flash:free",
                    "messages": [
                        {
                            "role": "user",
                            "content": str(user_input),
                        }
                    ],
                }
            ),
        )
        
        response_data = response.json()
        bot_response = response_data["choices"][0]["message"]["content"]
        print(f"User: {user_input}\nBot: {bot_response}")
    except Exception as e:
        last_error = str(e)
        print(f"Error occurred: {last_error}")

    if bot_response is None:
        bot_response = "Sorry, the chatbot service is temporarily unavailable. Please try again later."
        print(f"Request failed. Last error: {last_error}")

    return jsonify({"response": bot_response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
