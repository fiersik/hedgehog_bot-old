from vkbottle import Bot
from config import api, labeler
from handlers import (
    admin_labeler,
    Basic_labeler,
    new_chat_labeler
)

labeler.load(admin_labeler)
labeler.load(Basic_labeler)
labeler.load(new_chat_labeler)


bot = Bot(
    api=api,
    labeler=labeler
)


bot.run_forever()
