from vkbottle import API
from vkbottle.bot import BotLabeler
from modules import BotDB


db = BotDB("modules\hedgehog.db")

api = API("токен")

labeler = BotLabeler()
