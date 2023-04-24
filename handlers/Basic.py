import asyncio
from vkbottle.bot import BotLabeler, Message
from config import api, db

Basic_labeler = BotLabeler()
Basic_labeler.vbml_ignore_case = True


# basic commands


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

    name = db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog_name")

    await m.answer(
        "Ваш ёжик:\n"
        f"имя: {name}.",
        attachment = db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog")
    )

@Basic_labeler.chat_message(text = ["Дать ёжику имя", "Дать ёжику имя <name>"])
async def my_hedgehog(m: Message, name = None):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog") is None:
        await m.answer(
            "У вас нет ёжика"
        )
        return

    if name is None:
        await m.answer(
            "Укажите имя для вашего ёжика.\n"
            "Пример: Дать ёжику имя Рокси."
        )
        return

    db.update_info(m.from_id, f"chat_{m.peer_id}", "hedgehog_name", name)
    await m.answer(
        f"Поздравляем, теперь вашего ёжика зовут {name}"
    )


@Basic_labeler.chat_message(text = "покормить ёжика")
async def feed_the_hedgehog(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger") == 24:
        await m.answer(
            "Ваш ёжик не хочет есть."
        )
        return
    if not db.get_info(m.from_id, f"chat_{m.peer_id}", "can_eat"):
        await m.answer(
            "Кормить ежа можно раз в 4 часа, попробуйте позже"
        )
        return

    hunger = db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger")
    hunger += 1
    db.update_info(m.from_id, f"chat_{m.peer_id}", "hunger", hunger)

    await m.answer(
        "Вы успешно покормили ежа.\n"
        f"Сытость: {hunger}/24"
    )

    db.update_info(m.from_id, f"chat_{m.peer_id}", "can_eat", 0)
    await asyncio.sleep(60*60*4)
    db.update_info(m.from_id, f"chat_{m.peer_id}", "can_eat", 1)



@Basic_labeler.chat_message(text = "Выкинуть ёжика")
async def remove_hedgehog(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog") is None:
        await m.answer(
            "У вас нет ёжика"
        )
        return

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "remove_hedgehog"):

        vk_id = m.from_id

        users_info = await api.users.get(vk_id)
        first_name = users_info[0].first_name
        last_name = users_info[0].last_name

        db.update_info(m.from_id, f"chat_{m.peer_id}", "hedgehog", None)
        db.update_info(m.from_id, f"chat_{m.peer_id}", "hedgehog_name", "Мой ёжик")
        db.update_info(m.from_id, f"chat_{m.peer_id}", "hunger", 100)
        db.update_info(m.from_id, f"chat_{m.peer_id}", "remove_hedgehog", 0)

        await m.answer(
            f"[id{vk_id}|{first_name} {last_name}], "
            "Ну ты и негодяй\n"
            "У тебя больше нет ёжика."
        )
        return

    await m.answer(
        "Вы уверены?\n"
        "Для подтверждения повторите команду."
    )

    db.update_info(m.from_id, f"chat_{m.peer_id}", "remove_hedgehog", 1)




@Basic_labeler.chat_message()
async def start_background_processes(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog") is None:
        await m.answer(
            "У вас нет ёжика"
        )
        return

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger") > 0:
        if not db.get_info(m.from_id, f"chat_{m.peer_id}", "is_starving"):
            db.update_info(m.from_id, f"chat_{m.peer_id}", "is_starving", 1)
            while db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger") > 0:
                hunger = db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger") - 1
                db.update_info(m.from_id, f"chat_{m.peer_id}", "hunger", hunger)
                await asyncio.sleep(60*60*6)

            db.update_info(m.from_id, f"chat_{m.peer_id}", "is_starving", 0)

            await m.answer(
                "Ваш ёжик сильно проголодался :(\n"
                "Покормите его или он может умереть."
            )

            await asyncio.sleep(60*60*5)
            if db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger") > 0:
                pass
            else:
                db.update_info(m.from_id, f"chat_{m.peer_id}", "hedgehog", None)
                db.update_info(m.from_id, f"chat_{m.peer_id}", "hedgehog_name", "Мой ёжик")
                db.update_info(m.from_id, f"chat_{m.peer_id}", "hunger", 100)


                vk_id = m.from_id

                users_info = await api.users.get(vk_id)
                first_name = users_info[0].first_name
                last_name = users_info[0].last_name

                await m.answer(
                    "О нет!\n"
                    f"[id{vk_id}|{first_name} {last_name}], "
                    "твой ёжик умер"
                )
