import os
import random
import json
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from openai import OpenAI

# Load environment variables
load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
openai_api_key = os.getenv("OPENAI_API_KEY")
target_name = os.getenv("TELEGRAM_TARGET")

# Create Telegram and OpenAI clients
client = TelegramClient("saul_session", api_id, api_hash)
client_openai = OpenAI(api_key=openai_api_key)

# Path to the message history and prompt files
HISTORY_PATH = os.path.join(os.path.dirname(__file__), "message_history.json")
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.txt")

# Load previous message history (last 15 messages)
def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    return []

def save_to_history(message):
    history = load_history()
    history.insert(0, message)
    history = history[:15]  # Keep only the last 15 messages
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Load the prompt from an external file
def load_prompt():
    if not os.path.exists(PROMPT_PATH):
        raise FileNotFoundError("The prompt.txt file does not exist. Create one with the message instructions.")
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

# Generate the message
def generate_message():
    history = load_history()
    base_prompt = load_prompt()
    complete_prompt = f"{base_prompt}\n\nAvoid repeating ideas recently used. Here is a list of the last 15 messages used:\n{json.dumps(history, ensure_ascii=False)}"

    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": complete_prompt}],
        max_tokens=250
    )
    return response.choices[0].message.content.strip()

# Function to send the message
async def send_message():
    await client.start()
    message = generate_message()
    print("Generated message:\n", message)

    contact = await client.get_entity(target_name)
    await client.send_message(contact, message)
    print(f"Message sent to {target_name} at {datetime.now()}")

    save_to_history(message)
    await client.disconnect()

# Daily scheduler with a random time window
def schedule_sending():
    scheduler = BlockingScheduler()

    def schedule_random_time():
        base_hour = 9  # 9:00 AM
        random_minutes = random.randint(0, 120)  # up to 11:00 AM
        send_time = datetime.now().replace(hour=base_hour, minute=0, second=0, microsecond=0) + timedelta(minutes=random_minutes)
        scheduler.add_job(
            lambda: client.loop.run_until_complete(send_message()),
            trigger='cron',
            hour=send_time.hour,
            minute=send_time.minute
        )
        print(f"Message scheduled for {send_time.strftime('%H:%M')}")

    schedule_random_time()
    scheduler.start()

if __name__ == "__main__":
    import asyncio

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(send_message())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()