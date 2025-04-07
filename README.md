# 💌 Telegram Love Bot

A Python bot that sends a daily AI-generated love message (using OpenAI GPT-4o) to your partner via Telegram.

This project was born from the desire to maintain an emotional connection even at a distance. Every day, the bot generates a new, unique message—tender, playful, or cheeky—but always full of intention.

---

## 🧠 What does it do?

- Uses a customized prompt to generate messages with GPT-4o.
- Automatically sends the message via Telegram to your partner.
- Saves the last 15 messages to avoid repetitions.
- Can be run locally or deployed to a Cloud Function.
- The entire system is private and customizable!

---

## 📦 Requirements

- Python 3.10+
- An account on [OpenAI](https://platform.openai.com/)
- A [Telegram](https://my.telegram.org) account with API access
- Necessary Python libraries (see `requirements.txt`)

---

## ⚙️ Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/telegram-love-bot.git
   cd telegram-love-bot

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Create your .env file
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_TARGET=@username_or_contact_name

4. Create the prompt.txt file (you can start from prompt.txt.example) and customize it according to your relationship:

    ```
    cp prompt.txt.example prompt.txt
    ```

5. Run the bot manually

    ```
    python3 main.py
    ```

# Automation
## Locally (cronjob)
You can use cron to run the script every day at 10:00, even if the computer was off (see check_and_run.sh if included).

## On Google Cloud
Deploy the function as a Cloud Function with a Pub/Sub trigger.

Use Cloud Scheduler to invoke the function daily.

No need for servers; it runs only when scheduled.

# Security
The customized prompt is not uploaded by default (see .gitignore).

The history is only saved in a local file.

No bot tokens are used: the bot acts as an authenticated user (Telethon).

# What is this for?
This bot is a daily reminder of love, complicity, and connection.
Ideal for long-distance couples, relationships with a rich history, or simply for those who don't want to let a single day pass without saying "I love you."

# Author
Project created by Saúl Fernández, with love and much intention.

Want to improve it? Fork it, send me a PR, or get inspired to create your own version 💘