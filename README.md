# 💌 Telegram Love Bot

Un bot en Python que manda un mensaje de amor diario generado con inteligencia artificial (OpenAI GPT-4o) a tu pareja a través de Telegram.

Este proyecto nace del deseo de mantener viva la conexión emocional incluso en la distancia. Cada día, el bot genera un mensaje nuevo, único, tierno, divertido o pícaro... pero siempre cargado de intención.

---

## 🧠 ¿Qué hace?

- Usa un prompt personalizado para generar mensajes con GPT-4o.
- Envía el mensaje automáticamente por Telegram a tu pareja.
- Guarda los últimos 15 mensajes para evitar repeticiones.
- Se puede ejecutar localmente o subir a una Cloud Function.
- ¡Todo el sistema es privado y personalizable!

---

## 📦 Requisitos

- Python 3.10+
- Una cuenta en [OpenAI](https://platform.openai.com/)
- Una cuenta en [Telegram](https://my.telegram.org) con acceso a la API
- Librerías Python necesarias (ver `requirements.txt`)

---

## ⚙️ Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tuusuario/telegram-love-bot.git
cd telegram-love-bot
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Crea tu archivo `.env` con tus claves de Telegram y OpenAI:

```dotenv
TELEGRAM_API_ID=tu_api_id_de_telegram
TELEGRAM_API_HASH=tu_api_hash_de_telegram
OPENAI_API_KEY=tu_api_key_openai
TELEGRAM_TARGET=@usuario_o_nombre_contacto
```

4. Crea el archivo `prompt.txt` (puedes partir de `prompt.txt.example`) y personalízalo según tu relación:

```bash
cp prompt.txt.example prompt.txt
```

5. Ejecuta el bot manualmente:

```bash
python3 main.py
```

---

## 🕒 Automatización

### En local (cronjob)

Puedes usar `cron` para que se ejecute cada día a las 10:00, incluso si el ordenador estuvo apagado (ver `check_and_run.sh` si lo incluyes).

### En Google Cloud

1. Sube la función como Cloud Function con trigger de Pub/Sub.
2. Usa Cloud Scheduler para invocar la función cada día.
3. No necesitas servidores, se ejecuta solo cuando toca.

---

## 🔐 Seguridad

- El prompt personalizado no se sube por defecto (ver `.gitignore`).
- Solo se guarda el historial en un archivo local.
- No se usan tokens de bots: el bot actúa como usuario autenticado (Telethon).

---

## ❤️ ¿Para qué sirve esto?

Este bot es un recordatorio diario de amor, complicidad y conexión.  
Ideal para parejas a distancia, relaciones con mucha historia, o simplemente para quienes no quieren dejar pasar un solo día sin decir “te quiero”.

---

## ✨ Autor

Proyecto creado por [Saúl Fernández](https://github.com/tuusuario), con amor y mucha intención.

¿Quieres mejorarlo? Haz un fork, mándame un PR o inspírate para hacer tu propia versión 💘

