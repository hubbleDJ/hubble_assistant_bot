import json

from vars.GlobalVars import TG_TOKEN
from modules.GlobalModules.TgApi import Bot

bot = Bot(TG_TOKEN)

while True:
    updates = bot.get_updates()
    for message in updates.messages:
        bot.send_message(
            chat_id=message.chat_id,
            text=message.text,
        )