from vkbottle.bot import BotLabeler, Message
from config import db

Basic_labeler = BotLabeler()
Basic_labeler.vbml_ignore_case = True


@Basic_labeler.chat_message(text = "взять ёжика")
async def take_a_hedgehog(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog") is None and db.get_info(m.peer_id, "chat_stat", "new_hedgehog") is not None:
        hedgehog = db.get_info(m.peer_id, "chat_stat", "new_hedgehog")
        db.update_info(m.from_id, f"chat_{m.peer_id}", "hedgehog", hedgehog)
        db.update_info(m.peer_id, "chat_stat", "new_hedgehog", None)

        await m.answer(
            "Вы взяли ёжика"
        )

    elif db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog") is  not None:
        await m.answer("У вас уже есть ёжик")
    else:
        await m.answer("В вашей беседе нет свободного ёжика")


@Basic_labeler.chat_message(text = "мой ёжик")
async def my_hedgehog(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog") is None:
        await m.answer(
            "У вас нет ёжика"
        )
        return

    await m.answer(
        "Ваш ёжик",
        attachment = db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog")
    )
