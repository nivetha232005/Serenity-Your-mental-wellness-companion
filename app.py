from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__, static_folder=".")

API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = ("https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_message = (data.get("message") or "").strip()
    user_name = (data.get("name") or "there").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."}), 400

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            f"You are Serenity, a caring mental wellness companion. "
                            f"Address the user by their name {user_name}. "
                            f"Respond warmly in 2-3 supportive sentences. "
                            f"User message: {user_message}"
                        )
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY,
    }

    try:
        response = requests.post(
            GEMINI_URL,
            headers=headers,
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        result = response.json()

        reply = (
            result["candidates"][0]["content"]["parts"][0]["text"]
            if result.get("candidates")
            else "I'm here with you 🌿"
        )

        return jsonify({"reply": reply})

    except requests.exceptions.HTTPError:
        return jsonify({
            "reply": f"HTTP Error: {response.status_code}"
        }), 500

    except requests.exceptions.RequestException as e:
        return jsonify({
            "reply": f"Network Error: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)


