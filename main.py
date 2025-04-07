import os
import random
import json
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from openai import OpenAI

# Cargar variables del entorno
load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
openai_api_key = os.getenv("OPENAI_API_KEY")
target_name = os.getenv("TELEGRAM_TARGET")

# Crear cliente de Telegram y OpenAI
client = TelegramClient("saul_session", api_id, api_hash)
client_openai = OpenAI(api_key=openai_api_key)

# Ruta al archivo de registro de mensajes e instrucciones
HISTORIAL_PATH = os.path.join(os.path.dirname(__file__), "historial_mensajes.json")
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.txt")

# Cargar historial de mensajes previos (últimos 15)
def cargar_historial():
    if os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, "r") as f:
            return json.load(f)
    return []

def guardar_en_historial(mensaje):
    historial = cargar_historial()
    historial.insert(0, mensaje)
    historial = historial[:15]  # Mantener solo los últimos 15
    with open(HISTORIAL_PATH, "w") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

# Cargar el prompt desde archivo externo
def cargar_prompt():
    if not os.path.exists(PROMPT_PATH):
        raise FileNotFoundError("El archivo prompt.txt no existe. Crea uno con las instrucciones del mensaje.")
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()

# Prompt para crear el mensaje
def generar_mensaje():
    historial = cargar_historial()
    prompt_base = cargar_prompt()
    prompt_completo = f"{prompt_base}\n\nEvita repetir ideas ya utilizadas recientemente. Aquí tienes una lista de los últimos 15 mensajes usados:\n{json.dumps(historial, ensure_ascii=False)}"

    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt_completo}],
        max_tokens=250
    )
    return response.choices[0].message.content.strip()

# Función para mandar el mensaje
async def enviar_mensaje():
    await client.start()
    mensaje = generar_mensaje()
    print("Mensaje generado:\n", mensaje)

    contacto = await client.get_entity(target_name)
    await client.send_message(contacto, mensaje)
    print(f"Mensaje enviado a {target_name} a las {datetime.now()}")

    guardar_en_historial(mensaje)
    await client.disconnect()

# Programador diario con franja aleatoria
def planificar_envio():
    scheduler = BlockingScheduler()

    def programar_hora_aleatoria():
        hora_base = 9  # 9:00
        minutos_random = random.randint(0, 120)  # hasta las 11:00
        hora_envio = datetime.now().replace(hour=hora_base, minute=0, second=0, microsecond=0) + timedelta(minutes=minutos_random)
        scheduler.add_job(
            lambda: client.loop.run_until_complete(enviar_mensaje()),
            trigger='cron',
            hour=hora_envio.hour,
            minute=hora_envio.minute
        )
        print(f"Mensaje programado para las {hora_envio.strftime('%H:%M')}")

    programar_hora_aleatoria()
    scheduler.start()

if __name__ == "__main__":
    import asyncio

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(enviar_mensaje())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()