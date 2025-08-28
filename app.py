from flask import Flask, render_template, request, jsonify
from bot import get_bot_response  # သင့် Gemini API function ကို import လုပ်
import sqlite3, os

app = Flask(__name__)
DB_PATH = 'chat.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/messages", methods=["GET"])
def get_messages():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    messages = [{"role": r[0], "content": r[1]} for r in rows]
    return jsonify(messages)

@app.route("/api/messages", methods=["POST"])
def post_message():
    data = request.json
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"content": "No message received"}), 400

    # Gemini API response ကိုယူ
    ai_response = get_bot_response(message)

    # DB မှာ save
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO messages(role, content) VALUES (?, ?)", ("user", message))
    c.execute("INSERT INTO messages(role, content) VALUES (?, ?)", ("bot", ai_response))
    conn.commit()
    conn.close()

    return jsonify({"content": ai_response})

@app.route("/api/clear", methods=["POST"])
def clear_chat():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
