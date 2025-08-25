from flask import Flask, render_template, request, jsonify
from db import get_db_connection, init_db
from openai_client import get_gpt_response

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    # Save user message
    conn = get_db_connection()
    conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_message))
    conn.commit()

    # Get AI response
    ai_response = get_gpt_response(user_message)

    # Save AI response
    conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", ai_response))
    conn.commit()
    conn.close()

    return jsonify({"reply": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
