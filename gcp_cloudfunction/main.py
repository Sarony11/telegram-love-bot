from flask import Flask, request
import os
import json
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from openai import OpenAI
from datetime import datetime

# Flask app object, required by Gunicorn in Cloud Run
app = Flask(__name__)

# Load environment variables
load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
openai_api_key = os.getenv("OPENAI_API_KEY")
target_name = os.getenv("TELEGRAM_TARGET")

# Initialize clients
client = TelegramClient("saul_session", api_id, api_hash)
client_openai = OpenAI(api_key=openai_api_key)

# File paths
HISTORY_PATH = os.path.join(os.path.dirname(__file__), "message_history.json")
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.txt")

# Load last messages
def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    return []

# Save new message to history
def save_to_history(message):
    history = load_history()
    history.insert(0, message)
    history = history[:15]
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Load prompt text
def load_prompt():
    if not os.path.exists(PROMPT_PATH):
        raise FileNotFoundError("The prompt.txt file does not exist.")
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

# Generate new message using OpenAI
def generate_message():
    history = load_history()
    base_prompt = load_prompt()
    complete_prompt = f"{base_prompt}\n\nEvita repetir ideas recientemente usadas. Aquí tienes una lista de los últimos 15 mensajes utilizados:\n{json.dumps(history, ensure_ascii=False)}"

    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": complete_prompt}],
        max_tokens=250
    )
    return response.choices[0].message.content.strip()

# Cloud Run HTTP endpoint (called via POST)
@app.route("/", methods=["POST"])
def send_message():
    with client:
        message = generate_message()
        print("Mensaje generado:\n", message)

        contact = client.get_entity(target_name)
        client.send_message(contact, message)
        print(f"Mensaje enviado a {target_name} a las {datetime.now()}")

        save_to_history(message)

    return "Mensaje enviado correctamente", 200