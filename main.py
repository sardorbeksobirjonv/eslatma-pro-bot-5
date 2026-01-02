# bot.py
import os
import asyncio
from telethon import TelegramClient, events

# ================== TELEGRAM API MA'LUMOTLARI ==================
# Railway yoki boshqa serverda .env fayldan olamiz
api_id = int(os.environ.get("API_ID", "29199084"))
api_hash = os.environ.get("API_HASH", "32b0c3f696a54816c7fffe4c513b042a")
session_name = os.environ.get("SESSION_NAME", "userbot")  # session nomi

client = TelegramClient(session_name, api_id, api_hash)

# ================== FOYDALANUVCHI HOLATI ==================
user_state = {}
# user_state[user_id] = {
#     "auto_replied": True/False,
#     "unanswered_count": int
# }

# ================== XABAR QABUL QILISH ==================
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # Faqat shaxsiy chatlar
    if not event.is_private:
        return

    user_id = event.sender_id

    # Agar foydalanuvchi hali yo‘q bo‘lsa, boshlang‘ich holat
    if user_id not in user_state:
        user_state[user_id] = {
            "auto_replied": False,
            "unanswered_count": 0
        }

    state = user_state[user_id]

    # 1️⃣ Birinchi xabar → darhol javob
    if not state["auto_replied"]:
        await event.reply(
            "Assalomu alaykum 😊\n\n"
            "Xabaringiz uchun rahmat.\n"
            "Hozir bandman, bo‘shaganimda albatta javob beraman.\n\n"
            "Savolingiz bo‘lsa yozib qoldirishingiz mumkin ✍️\n"
            "Hozircha avtomatik yordamchi (userbot) javob bermoqda."
        )
        state["auto_replied"] = True
        state["unanswered_count"] = 0
        return

    # 2️⃣ Keyingi xabarlar — sanaymiz
    state["unanswered_count"] += 1

    # 3️⃣ Agar 8 ta xabar yig‘ilsa → yana javob
    if state["unanswered_count"] >= 8:
        await event.reply(
            "Xabaringizni ko‘rdim 😊\n"
            "Hozircha javob bera olmayapman.\n"
            "Iltimos, biroz sabr qiling 🙏"
        )
        state["unanswered_count"] = 0  # qayta sanash boshlanadi

# ================== ASOSIY RUN ==================
async def main():
    await client.start()
    print("Userbot ishga tushdi...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
