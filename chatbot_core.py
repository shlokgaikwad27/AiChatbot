import random
import sqlite3
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Load NLP data
nltk.download("punkt")
nltk.download("stopwords")

stop_words = set(stopwords.words("english"))

# Load FAQ data
qa_dict = {}

with open("Chat_data.txt", "r") as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            qa_dict[key.lower()] = value

# Fallback replies
fallback = [
    "I am still learning. Can you ask something else?",
    "Can you rephrase that?",
    "Interesting question! Tell me more."
]

# -------- NLP PREPROCESSING --------
def preprocess(text):
    words = word_tokenize(text.lower())
    clean_words = [w for w in words if w.isalpha() and w not in stop_words]
    return clean_words

# -------- CHATBOT LOGIC --------
def get_response(user_input):
    user_words = preprocess(user_input)

    for key in qa_dict:
        key_words = preprocess(key)

        # If any keyword matches
        for w in key_words:
            if w in user_words:
                return qa_dict[key]

    return random.choice(fallback)

# -------- DATABASE LOGGING --------
def log_chat(username, msg, reply):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    time = datetime.now()
    cursor.execute("INSERT INTO chat_logs (username,user_message,bot_reply,time) VALUES (?,?,?,?)",
                   (username, msg, reply, time))
    conn.commit()
    conn.close()
