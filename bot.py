import os
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
    def log_message(self, *args):
        pass

def run_health():
    port = int(os.environ.get("PORT", 8000))
    HTTPServer(("0.0.0.0", port), Health).serve_forever()

threading.Thread(target=run_health, daemon=True).start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ekta wallpaper-er idea likhun, ami baniye dibo.")

async def make_wallpaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("Banacchi, ektu opekkha korun...")

    full_prompt = f"{prompt}, mobile phone wallpaper, vertical, high quality"
    url = (
        "https://image.pollinations.ai/prompt/"
        + urllib.parse.quote(full_prompt)
        + "?width=1080&height=1920&nologo=true"
    )

    try:
        async with httpx.AsyncClient(timeout=120, follow_redirects=True) as client:
            r = await client.get(url)
            r.raise_for_status()
        await update.message.reply_document(
            document=r.content,
            filename="wallpaper.jpg",
            caption="Apnar wallpaper ready!",
        )
    except Exception:
        await update.message.reply_text("Kothao ekta somossa hoyeche, abar try korun.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, make_wallpaper))
app.run_polling()
