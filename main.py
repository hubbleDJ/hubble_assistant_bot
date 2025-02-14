import json

from vars.GlobalVars import TG_TOKEN
from modules.GlobalModules.TgApi import Bot

bot = Bot(TG_TOKEN)
bot.get_updates()