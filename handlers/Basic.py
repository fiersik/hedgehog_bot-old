from vkbottle.bot import BotLabeler, Message
from config import db

Basic_labeler = BotLabeler()
Basic_labeler.vbml_ignore_case = True


@Basic_labeler.chat_message(text = "мой ёжик")
async def hello(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog") is None:
        await m.answer(
            "У вас нет ёжика"
        )
        return

    await m.answer(
        "Ваш ёжик",
        attachment = db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog")
    )
