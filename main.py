from flask import Flask, request
import requests
import time
import threading

app = Flask(__name__)

BOT_TOKEN = "7595186215:AAGESt6D3MSw5bMi4hqLE71pd4j7kt6GZEs"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
WELCOME_PHOTO = "https://i.ibb.co/HTG8zXnm/IMG-20250516-095810-290.jpg"
COOKIES_FILE_URL = "https://raw.githubusercontent.com/hackelite01/test-files/main/cookies.txt"  # Change if needed

def send_photo(chat_id, photo_url, caption, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{URL}/sendPhoto", json=payload)

def send_message(chat_id, text):
    res = requests.post(f"{URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    }).json()
    return res.get("message_id")

def delete_message(chat_id, message_id):
    requests.post(f"{URL}/deleteMessage", json={
        "chat_id": chat_id,
        "message_id": message_id
    })

def send_document(chat_id, file_url, caption=""):
    requests.post(f"{URL}/sendDocument", json={
        "chat_id": chat_id,
        "document": file_url,
        "caption": caption,
        "parse_mode": "HTML"
    })

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("Received update:", data)

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]

        if "text" in message and message["text"] == "/start":
            caption = "Welcome! This is <b>Cookies Generator</b> by <b>Team Zeryo</b>."
            button = {
                "inline_keyboard": [[{"text": "🍪 Generate Your Cookies", "callback_data": "generate"}]]
            }
            send_photo(chat_id, WELCOME_PHOTO, caption, reply_markup=button)

    elif "callback_query" in data:
        query = data["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        user = query["from"]["first_name"]

        if query["data"] == "generate":
            loading_msg = f"⏳ Generating cookies for {user}..."
            loading_id = send_message(chat_id, loading_msg)

            def finish():
                time.sleep(4)
                delete_message(chat_id, loading_id)
                send_document(chat_id, COOKIES_FILE_URL, caption="🍪 Here are your cookies!")

            threading.Thread(target=finish).start()

    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Bot is live."
