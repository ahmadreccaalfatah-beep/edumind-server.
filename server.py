
import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

@app.route("/")
def home():
    return "EduMind AI Server is running!"

@app.route("/chat", methods=["POST"])
def chat():
    key = os.getenv("GEMINI_API_KEY")

    if not key:
        return jsonify({"error": "API Key belum dipasang"}), 503

    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Pesan kosong"}), 400

    try:
        client = genai.Client(api_key=key)
        result = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "Kamu adalah EduMind, tutor AI. "
                    "Ajarkan pelajaran dengan sederhana dan bertahap."
                )
            )
        )
        return jsonify({"reply": result.text})

    except Exception:
        app.logger.exception("Gemini error")
        return jsonify({"error": "Terjadi kesalahan pada AI"}), 502
