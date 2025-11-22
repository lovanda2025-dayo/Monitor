import logging
from flask import Flask
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import get_last_post

# Configuração de Logging
logging.basicConfig(level=logging.INFO)

# Credenciais e informações internas
TELEGRAM_TOKEN = "7854248730:AAHrqEurKkDAQFEFqCfWRfIh9miuk4m9mn8"
CHAT_ID = "6237551288"  # ID do grupo ou pessoa
FB_PAGE_URL = "https://www.facebook.com/profile.php?id=61584207986823"

bot = Bot(token=TELEGRAM_TOKEN)

app = Flask(__name__)

# Mantém histórico para evitar duplicados
ultimo_post = None

def verificar_facebook():
    global ultimo_post

    logging.info("🔎 Verificando página do Facebook...")

    novo_post = get_last_post(FB_PAGE_URL)

    if not novo_post:
        logging.warning("⚠️ Nenhum post encontrado.")
        return

    if novo_post != ultimo_post:
        bot.send_message(chat_id=CHAT_ID, text=f"📢 Novo post encontrado:\n\n{novo_post}")
        ultimo_post = novo_post
        logging.info("📨 Post enviado ao Telegram.")
    else:
        logging.info("⏳ Nada novo.")


# Rota para manter o Render acordado
@app.route("/")
def home():
    return "Bot ativo ✔️"


def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(verificar_facebook, "interval", minutes=2)
    scheduler.start()
    logging.info("⏳ Scheduler iniciado (2 minutos).")


if __name__ == "__main__":
    iniciar_scheduler()
    app.run(host="0.0.0.0", port=10000)