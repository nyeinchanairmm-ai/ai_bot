from flask import Flask, render_template, request, jsonify
from db import get_db_connection, init_db
from openai_client import get_bot_response

import os

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/messages", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    conn = get_db_connection()
    conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_message))
    conn.commit()

    ai_response = get_bot_response(user_message)

    conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("bot", ai_response))
    conn.commit()
    conn.close()

    return jsonify({"role": "bot", "content": ai_response})

@app.route("/api/messages", methods=["GET"])
def get_messages():
    conn = get_db_connection()
    rows = conn.execute("SELECT role, content FROM messages ORDER BY timestamp").fetchall()
    conn.close()
    messages = [{"role": row["role"], "content": row["content"]} for row in rows]
    return jsonify(messages)

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT, debug=True)


# from flask import Flask, render_template, request, jsonify
# from db import get_db_connection, init_db
# from openai_client import get_bot_response

# app = Flask(__name__)
# init_db()

# @app.route("/")
# def index():
#     return render_template("index.html")

# # ✅ POST route
# @app.route("/api/messages", methods=["POST"])
# def chat():
#     user_message = request.json.get("message")

#     conn = get_db_connection()
#     conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_message))
#     conn.commit()

#     ai_response = get_bot_response(user_message)

#     conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("bot", ai_response))
#     conn.commit()
#     conn.close()

#     return jsonify({"role": "bot", "content": ai_response})

# # ✅ GET route (for history)
# @app.route("/api/messages", methods=["GET"])
# def get_messages():
#     conn = get_db_connection()
#     rows = conn.execute("SELECT role, content FROM messages ORDER BY timestamp").fetchall()
#     conn.close()
#     return jsonify([{"role": row["role"], "content": row["content"]} for row in rows])

# if __name__ == "__main__":
#     app.run(debug=True)
