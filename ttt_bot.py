import asyncio
import random
import aiohttp
from twitchio.ext import commands

# ---------- НАСТРОЙКИ ----------
ACCESS_TOKEN = "x8crcvq554c9ay037d3nichukbsk2i"
CLIENT_ID = "gp762nuuoqcoxypju8c569th9wz7q5"
TARGET_CHANNEL = "solo"
PREFIX = "!"
DURATIONS = [32, 322, 3222, 223, 2223]
# --------------------------------

HELIX_BANS = "https://api.twitch.tv/helix/moderation/bans"

class ModBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=f"oauth:{ACCESS_TOKEN}",
            client_id=CLIENT_ID,
            prefix=PREFIX,
            initial_channels=[TARGET_CHANNEL]
        )
        self.http_session = aiohttp.ClientSession()

    async def event_ready(self):
        print(f"✅ БОТ ЗАПУЩЕН! Аккаунт: {self.nick}, Канал: {TARGET_CHANNEL}")

    async def event_message(self, message):
        if message.echo:
            return

        content = message.content.strip().lower()
        author = message.author.name
        print(f"[{author}]: {message.content}")

        if content.startswith("!ttt") or content.startswith("!ттт"):
            await self.handle_ttt(message)

    async def handle_ttt(self, message):
        user = message.author.name

        if user.lower() == TARGET_CHANNEL.lower():
            print(f"⚠️ Нельзя таймить стримера {user}")
            return

        if message.author.is_mod:
            print(f"⚠️ Не таймим {user}, это модератор")
            return

        duration = random.choice(DURATIONS)

        # Получаем ID пользователя и канала
        user_id = message.author.id
        broadcaster = await self.fetch_users(names=[TARGET_CHANNEL])
        broadcaster_id = broadcaster[0].id

        # Получаем ID бота
        bot_user = await self.fetch_users(names=[self.nick])
        moderator_id = bot_user[0].id

        headers = {
            "Client-Id": CLIENT_ID,
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        body = {
            "data": {
                "user_id": user_id,
                "moderator_id": moderator_id,
                "duration": duration,
                "reason": "!ttt"
            }
        }

        try:
            async with self.http_session.post(
                f"{HELIX_BANS}?broadcaster_id={broadcaster_id}&moderator_id={moderator_id}",
                headers=headers,
                json=body
            ) as resp:
                if resp.status in (200, 204):
                    print(f"⚡️ Таймаут {user} на {duration} сек. выдан через API 🎯")
                else:
                    text = await resp.text()
                    print(f"❌ Ошибка таймаута {user}: {resp.status} — {text}")
        except Exception as e:
            print(f"❌ Исключение при таймауте {user}: {e}")

async def start_bot():
    bot = ModBot()
    try:
        await bot.start()
    finally:
        await bot.http_session.close()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        print("❌ Бот остановлен.")
