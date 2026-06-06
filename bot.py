"""
ربات تلگرام ارجاعات - نسخه ساده و پایدار
pip install flask flask-cors requests
python bot.py
"""
import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

BOT_TOKEN      = "8307425369:AAGKTObF6DP1_B5nMLUHBp89PK47A_STI5M"
GROUP_ID       = "-1003905577485"
WEBHOOK_SECRET = "Haj_ali_piry"

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

def send_to_group(text):
    """ارسال پیام به گروه تلگرام - بدون async"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": GROUP_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        res = requests.post(url, json=payload, timeout=15)
        data = res.json()
        if not data.get("ok"):
            logging.error(f"Telegram error: {data}")
            return False
        return True
    except Exception as e:
        logging.error(f"Send error: {e}")
        return False

@app.route("/submit", methods=["POST", "OPTIONS"])
def submit():
    if request.method == "OPTIONS":
        return jsonify({"ok": True})

    if request.headers.get("X-Secret", "") != WEBHOOK_SECRET:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    data = request.get_json(force=True)
    if not data:
        return jsonify({"ok": False, "error": "No data"}), 400

    message = data.get("message", "")
    if not message:
        return jsonify({"ok": False, "error": "پیامی دریافت نشد"}), 400

    success = send_to_group(message)
    if success:
        return jsonify({"ok": True})
    else:
        return jsonify({"ok": False, "error": "خطا در ارسال به تلگرام"}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("✅ ربات در حال اجراست...")
    print("🌐 آدرس webhook: http://localhost:5000/submit")
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=False)
