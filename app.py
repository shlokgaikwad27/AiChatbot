from flask import Flask, request, jsonify, render_template, redirect, session
from chatbot_core import get_response, log_chat
import sqlite3
from collections import deque   # STEP 3 memory

app = Flask(__name__)
app.secret_key = "secret123"  # session security

# ---------------- CHAT MEMORY (LAST 5 MESSAGES) ----------------
chat_memory = deque(maxlen=5)

# ---------------- DB connection ----------------
conn = sqlite3.connect("chatbot.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"].strip()

        # Read password safely
        with open("password.txt") as f:
            real_pass = f.read().strip().split("=")[-1].strip()

        if password == real_pass:
            session["admin"] = True
            return redirect("/admin_panel")
        else:
            return render_template("wrong_password.html")

    return render_template("admin_login.html")

# ---------------- ADMIN PANEL ----------------
@app.route("/admin_panel")
def admin_panel():
    if not session.get("admin"):
        return redirect("/admin")

    cursor.execute("SELECT * FROM chat_logs")
    logs = cursor.fetchall()
    return render_template("admin_panel.html", logs=logs)

# ---------------- CLEAR CHAT HISTORY ----------------
@app.route("/clear_history")
def clear_history():
    if not session.get("admin"):
        return redirect("/admin")

    cursor.execute("DELETE FROM chat_logs")
    conn.commit()
    return redirect("/admin_panel")

# ---------------- CHAT PAGE ----------------
@app.route("/chat_page")
def chat_page():
    return render_template("chat.html")

# ---------------- CHAT API (WITH MEMORY) ----------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data["message"]
    user = data.get("username", "Guest")

    # Save user message
    chat_memory.append(f"User: {msg}")

    # Get bot reply
    reply = get_response(msg)

    # Save bot reply
    chat_memory.append(f"Bot: {reply}")

    # Log in DB
    log_chat(user, msg, reply)

    return jsonify({
        "reply": reply,
        "memory": list(chat_memory)
    })
# ---------------- CHAT HISTORY API ----------------
@app.route("/history")
def history():
    cursor.execute("SELECT username, user_message, bot_reply, time FROM chat_logs ORDER BY id DESC LIMIT 20")
    rows = cursor.fetchall()
    return jsonify(rows[::-1])  # reverse to show oldest first


# ---------------- LOGOUT ADMIN ----------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
