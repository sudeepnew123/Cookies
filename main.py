from flask import Flask, request
import requests
import time
import threading

app = Flask(__name__)

BOT_TOKEN = "7595186215:AAGESt6D3MSw5bMi4hqLE71pd4j7kt6GZEs"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
CATBOX_URL = "https://files.catbox.moe/81o4p9.txt"
WELCOME_PHOTO = "https://i.ibb.co/HTG8zXnm/IMG-20250516-095810-290.jpg"

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

def edit_message(chat_id, message_id, text):
    requests.post(f"{URL}/editMessageText", json={
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
    })

def delete_message(chat_id, message_id):
    requests.post(f"{URL}/deleteMessage", json={
        "chat_id": chat_id,
        "message_id": message_id
    })

def send_document(chat_id, file_url, caption=""):
    requests.post(f"{URL}/sendDocument", json={
        "chat_id": chat_id,
        "document": file_url,
        "caption": caption
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
        msg_id = query["message"]["message_id"]
        user = query["from"]["first_name"]

        if query["data"] == "generate":
            edit_message(chat_id, msg_id, f"⏳ Generating cookies for {user}...")

            def delayed_send():
                time.sleep(4)
                delete_message(chat_id, msg_id)
                send_document(chat_id, CATBOX_URL, caption="🍪 Here are your cookies!")

            threading.Thread(target=delayed_send).start()

    return "ok"

@app.route("/", methods=["GET"])
def root():
    return "Bot is running."
