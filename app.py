from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'chat.db'

# Initialize database
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

# Get all messages
@app.route("/api/messages", methods=["GET"])
def get_messages():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM messages ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    messages = [{"role": r[0], "content": r[1]} for r in rows]
    return jsonify(messages)

# Add new message
@app.route("/api/messages", methods=["POST"])
def post_message():
    data = request.json
    message = data.get("message", "").strip()
    if message:
        # Here you would call your AI API for response
        ai_response = f"Echo: {message}"  # Placeholder
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO messages(role, content) VALUES (?,?)", ("user", message))
        c.execute("INSERT INTO messages(role, content) VALUES (?,?)", ("bot", ai_response))
        conn.commit()
        conn.close()
        return jsonify({"content": ai_response})
    return jsonify({"content": "No message received"}), 400

# Clear chat
@app.route("/api/clear", methods=["POST"])
def clear_chat():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, render_template, request, jsonify
# from db import get_db_connection, init_db
# from openai_client import get_bot_response

# import os

# app = Flask(__name__)
# init_db()

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/api/messages", methods=["POST"])
# def chat():
#     data = request.json
#     user_message = data.get("message")
#     if not user_message:
#         return jsonify({"error": "No message provided"}), 400

#     conn = get_db_connection()
#     conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_message))
#     conn.commit()

#     ai_response = get_bot_response(user_message)

#     conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("bot", ai_response))
#     conn.commit()
#     conn.close()

#     return jsonify({"role": "bot", "content": ai_response})

# @app.route("/api/messages", methods=["GET"])
# def get_messages():
#     conn = get_db_connection()
#     rows = conn.execute("SELECT role, content FROM messages ORDER BY timestamp").fetchall()
#     conn.close()
#     messages = [{"role": row["role"], "content": row["content"]} for row in rows]
#     return jsonify(messages)

# if __name__ == "__main__":
#     PORT = int(os.environ.get("PORT", 10000))
#     app.run(host="0.0.0.0", port=PORT, debug=True)

