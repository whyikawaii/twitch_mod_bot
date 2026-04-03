import os
import random
import asyncio
from twitchio.ext import commands

# ----------------- ENVIRONMENT VARIABLES -----------------
ACCESS_TOKEN = os.environ["TWITCH_ACCESS_TOKEN"]
CLIENT_ID = os.environ["TWITCH_CLIENT_ID"]
CLIENT_SECRET = os.environ["TWITCH_CLIENT_SECRET"]
BOT_ID = os.environ["TWITCH_BOT_ID"]
BROADCASTER_ID = os.environ["TWITCH_BROADCASTER_ID"]
TARGET_CHANNEL = os.environ.get("TWITCH_TARGET_CHANNEL", "solo")
PREFIX = os.environ.get("TWITCH_PREFIX", "!")
DURATIONS = [32, 322, 3222, 223, 2223]
# ---------------------------------------------------------

class ModBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=ACCESS_TOKEN,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            prefix=PREFIX,
            initial_channels=[TARGET_CHANNEL]
        )

    async def event_ready(self):
        print(f"✅ БОТ ЗАПУЩЕН! Аккаунт: {self.nick}, Канал: {TARGET_CHANNEL}")

    async def event_message(self, message):
        if message.echo:
            return

        author = message.author.name
        content = message.content.strip().lower()
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

        try:
            await message.channel.timeout_user(message.author, duration, reason="!ttt")
            print(f"⚡️ Таймаут {user} на {duration} сек. через EventSub 🎯")
        except Exception as e:
            print(f"❌ Ошибка таймаута {user}: {e}")


async def main():
    bot = ModBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
