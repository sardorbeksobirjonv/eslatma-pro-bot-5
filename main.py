# bot.py
import os
import asyncio
import time
from telethon import TelegramClient, events

# ================== TELEGRAM API ==================
api_id = int(os.environ.get("API_ID", "29199084"))
api_hash = os.environ.get("API_HASH", "32b0c3f696a54816c7fffe4c513b042a")
session_name = os.environ.get("SESSION_NAME", "userbot")

client = TelegramClient(session_name, api_id, api_hash)

# ================== FOYDALANUVCHI HOLATI ==================
user_state = {}
# user_state[user_id] = {
#     "auto_sent": False,
#     "last_my_reply": time,
#     "spam_count": 0
# }

AUTO_REPLY_TEXT = (
    "Assalomu alaykum 😊\n\n" "Xabaringiz uchun rahmat.\n" "Hozir bandman, bo‘shaganimda albatta javob beraman.\n\n" "Savolingiz bo‘lsa yozib qoldirishingiz mumkin ✍️\n" "Hozircha avtomatik yordamchi (userbot) javob bermoqda."
)

SPAM_REPLY_TEXT = (
    "Xabaringizni ko‘rdim 😊\n"
    "Hozircha javob bera olmayapman.\n"
    "Iltimos, biroz sabr qiling 🙏"
)

SPAM_LIMIT = 6          # nechta xabar yozsa
SILENCE_TIME = 300      # 5 daqiqa javob bermasang (soniyada)

# ================== FOYDALANUVCHI YOZGANDA ==================
@client.on(events.NewMessage(incoming=True))
async def incoming_handler(event):
    if not event.is_private:
        return

    user_id = event.sender_id
    now = time.time()

    if user_id not in user_state:
        user_state[user_id] = {
            "auto_sent": False,
            "last_my_reply": 0,
            "spam_count": 0
        }

    state = user_state[user_id]

    # 1️⃣ Birinchi xabar → 1 marta avtomatik javob
    if not state["auto_sent"]:
        await event.reply(AUTO_REPLY_TEXT)
        state["auto_sent"] = True
        state["spam_count"] = 0
        return

    # 2️⃣ Agar sen yaqinda javob bergan bo‘lsang → BOT JIM
    if now - state["last_my_reply"] < SILENCE_TIME:
        state["spam_count"] = 0
        return

    # 3️⃣ Agar sen javob bermayapsan va u yozaversa → sanaymiz
    state["spam_count"] += 1

    if state["spam_count"] >= SPAM_LIMIT:
        await event.reply(SPAM_REPLY_TEXT)
        state["spam_count"] = 0


# ================== SEN YOZGANDA ==================
@client.on(events.NewMessage(outgoing=True))
async def outgoing_handler(event):
    if not event.is_private:
        return

    user_id = event.chat_id
    now = time.time()

    if user_id not in user_state:
        user_state[user_id] = {
            "auto_sent": True,
            "last_my_reply": now,
            "spam_count": 0
        }
    else:
        user_state[user_id]["last_my_reply"] = now
        user_state[user_id]["spam_count"] = 0


# ================== RUN ==================
async def main():
    await client.start()
    print("✅ Userbot ishga tushdi...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())