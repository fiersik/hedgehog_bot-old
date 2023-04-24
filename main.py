from vkbottle import Bot
from config import db, api, labeler
from handlers import (
    new_chat_labeler,
    Basic_labeler,
    creator_labeler,
    admin_labeler
)


labeler.load(new_chat_labeler)
labeler.load(Basic_labeler)
labeler.load(creator_labeler)
labeler.load(admin_labeler)


bot = Bot(
    api=api,
    labeler=labeler
)


if __name__ == "__main__":
    db.start_db()
    bot.run_forever()
