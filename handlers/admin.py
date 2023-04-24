from vkbottle.bot import BotLabeler, Message, rules
from modules import admin_rule
import asyncio
from datetime import datetime
from config import db
import random


admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True


"""РАССЫЛКА ЕЖЕЙ"""
@admin_labeler.message(admin_rule(), text = "подписаться на рассылку")
async def news(m: Message):
    if db.get_info(m.peer_id, "chat_stat", "news_sub"):
        await m.answer(
            "Вы уже подписаны на рассылку."
        )
        return

    await m.answer(
        "Вы подписались на рассылку."
        "Каждые 2 часа вашей беседе будет приходить ёжик."
    )

    db.update_info(m.peer_id, "chat_stat", "news_sub", 1)

    while True:

        if not db.get_info(m.peer_id, "chat_stat", "news_sub"):
            return

        if datetime.now().hour%2 == 0 and datetime.now().minute == 0:

            rand = random.randint(9019, 9034)
            photo = f"photo-219000856_45723{rand}"

            if db.get_info(m.peer_id, "chat_stat", "news_sub"):

                db.update_info(m.peer_id, "chat_stat", "new_hedgehog", photo)

                await m.answer(
                    "Вам ёжик",
                    attachment=photo
                )
                await asyncio.sleep(60)
            else:
                return
        else:
            await asyncio.sleep(60)

@admin_labeler.message(admin_rule(), text = "Отписаться от рассылки")
async def no_news(m: Message):

    if not db.get_info(m.peer_id, "chat_stat", "news_sub"):
        await m.answer("вы не подписаны на рассылку.")
        return

    await m.answer(
        "Вы отписались от рассылки :("
    )

    db.update_info(m.peer_id, "chat_stat", "news_sub", 0)
