import random
import sqlite3
from datetime import datetime
# cursor.execute("Drop Table chat_logs ")
try:
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        user_message TEXT,
        bot_reply TEXT,
        time Text)""")
    conn.commit()
except sqlite3.Error as e:
    print("Database connection failed:", e)


l=["I am still learning. Can you ask something else?","I didn’t understand, can you rephrase?"]
qa_dict = {}
try:
    with open("Chat_data.txt", "r") as txt:
        for line in txt:
            line = line.strip()
            if "=" in line:
                keys, value = line.split("=", 1)  # safer
                qa_dict[keys.lower()] = value
except FileNotFoundError:
    print("Chat data file missing! Using empty FAQ dictionary.")
except Exception as e:
    print("Error loading chat data:", e)



def get_response(user_input):               
    user_input = user_input.lower()
    for key in qa_dict:
        words = user_input.split()
        if key in words:
            return qa_dict[key]
    else:
        return random.choice(l)

with open("password.txt","r") as t:
    passw=t.read().split("=")[1].strip()

try:
    while True:
        u=input("1.ADMIN LOGIN\n2.CHAT\n3.EXIT\n")
        print("\n")
        if u.lower() in ["admin", "admin login", "login","1"]:
            p=input("Enter password\n")
            if p==passw:
                print("logged in")
                print("what accsess do u need???\n")
                ch=input("1.chat history\n2.clear database\n3.alter data \n\n")
                if ch.lower() in ["chat history", "history", "chat","1"]:
                    cursor.execute("SELECT * FROM chat_logs")
                    rows = cursor.fetchall()
                    cursor.execute("SELECT COUNT(*) FROM chat_logs")
                    count = cursor.fetchone()[0]
                    print("Rows in table:", count)
                    if count==0:
                        print("DATABASE is empty")
                    else:
                        for row in rows:
                            print(row)
                    print("THANKS!!!!!!!!!")
                elif ch.lower() in ["clear","clear database","delete","2"]:
                    cursor.execute("DELETE FROM chat_logs")
                    conn.commit()
                    print("chat history cleared")
                    print("THANKS!!!!!!!!!")
                elif ch.lower() in ["alter","alter data","update","update data","3"]:
                    try:
                        print("we are working on it........")
                    except:
                        print("failed to alter data")
                    print("THANKS!!!!!!!!!")
                else:
                    print("Incorrect function try again...")
            else:
                print("incorect password")
        elif u.lower() in ["chat","2"]:
            c=0
            print("*************TYPE exit to end the chat***************\n")
            name=input("ENTER YOUR NAME:\n")
            while True: 
                user = input("You: ")
                time = datetime.now()
                if user.lower()=="exit":
                    print("Bot:Goodbye! Have a nice day.")
                    print("Total questions asked:",c)
                    break
                else:
                    c+=1
                    r=get_response(user)
                    print("Bot:",r )
                    cursor.execute("INSERT INTO chat_logs (username,user_message, bot_reply,time) VALUES (?, ?, ?, ?)",(name,user,r,time))
                    conn.commit()
            print("chat saved")
        elif u.lower() in ["stop","exit","3"]:
            break
        else:
            print("Incorrect function try again...")

except Exception as e:
    print("System Error:", e)
finally:
    conn.close()

