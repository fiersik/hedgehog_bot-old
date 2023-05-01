from datetime import datetime, timedelta
from time import time
import random
import ast
import re
import math

from vkbottle.bot import BotLabeler, Message, rules
import asyncio

from modules import creator_rule
from config import api, db


creator_labeler = BotLabeler()
creator_labeler.vbml_ignore_case = True

# Bot creator commands


@creator_labeler.message(creator_rule(), text="Включить рассылку")
async def start_news(m: Message):

    await m.answer(
        "Вы включили рассылку ёжиков."
    )

    while True:
        if datetime.now().hour % 2 != 0 and datetime.now().minute == 0:

            members = db.get_full_info("news_sub", "chat_stat", "object_id", 1)
            members = [x for l in members for x in l]

            if len(members) != 0:
                rand = random.randint(9019, 9034)
                message = "Вам ёжик"
                attachment = f"photo-219000856_45723{rand}"

                for member in members:
                    db.update_info(member, "chat_stat",
                                   "new_hedgehog", attachment)

                if len(members) < 100:
                    await api.messages.send(
                        peer_ids=members,
                        message=message,
                        attachment=attachment,
                        random_id=m.random_id
                    )
                else:
                    for member in members:
                        await api.messages.send(
                            peer_id=member,
                            message=message,
                            attachment=attachment,
                            random_id=m.random_id
                        )

        await asyncio.sleep(60)


@creator_labeler.message(creator_rule(), text=["Запустить рассылку", "Запустить рассылку <text>"])
async def urgent_mailing(m: Message, text=None):

    start_time = time()

    if text is None:
        await m.answer("Укажите текст рассылки.")
        return

    members = db.get_chats("chat_stat", "object_id")
    members = [x for l in members for x in l]

    if len(members) != 0:
        if len(members) < 100:
            await api.messages.send(
                peer_ids=members,
                message=text,
                random_id=m.random_id
            )
        else:
            for member in members:
                await api.messages.send(
                    peer_id=member,
                    message=text,
                    random_id=m.random_id
                )

    end_time = time()

    await m.answer(
        "Рассылка закончена.\n"
        f"Завершена за {round(end_time-start_time, 1)} сек."
    )


@creator_labeler.message(creator_rule(), text="Рассылка инфо")
async def mailing_information(m: Message):

    members = db.get_full_info("news_sub", "chat_stat", "object_id", 1)
    members = [x for l in members for x in l]

    await m.answer(
        f"Бесед подписано на рассылку: {len(members)}\n"
        "Срочная рассылка доступна во всех беседах."
    )


@creator_labeler.message(creator_rule(), text="Включить голод")
async def turn_on_hunger(m: Message):

    await m.answer(
        "Теперь все ёжики начнут голодать."
    )

    while True:
        await asyncio.sleep(60*60*6)

        members = db.get_chats("chat_stat", "object_id")
        members = [x for l in members for x in l]

        for chat in members:

            name = f"chat_{chat}"

            db.update_all(name, "is_starving", 1)
            db.increase_all(name, "hunger", 1)

            hungry = db.get_full_info("hunger", name, "object_id", 0)
            hungry = [x for l in hungry for x in l]

            if len(hungry) != 0:

                for member in hungry:
                    Date_of_death = db.get_info(member, name, "Date_of_death")
                    if Date_of_death is None:
                        users_info = await api.users.get(member)
                        first_name = users_info[0].first_name
                        last_name = users_info[0].last_name

                        await api.messages.send(
                            peer_id=chat,
                            message=f"[id{member}|{first_name} {last_name}], Ваш ёжик сильно проголодался :(\nПокормите его или он может умереть.",
                            random_id=m.random_id
                        )
                        db.update_info(member, name, "state", "слаб")
                        now_time = datetime.now()
                        now_time += timedelta(hours=6)
                        Date_of_death = f"[{now_time.year}, {now_time.month}, {now_time.day}, {now_time.hour}, {now_time.minute}, {now_time.second}]"

                        db.update_info(
                            member, name, "Date_of_death", Date_of_death)


@creator_labeler.message(creator_rule(), text="Включить смерти")
async def turn_on_death(m: Message):

    await m.answer(
        "Теперь голодные ёжики будут умирать."
    )

    while True:

        members = db.get_chats("chat_stat", "object_id")
        members = [x for l in members for x in l]

        for chat in members:

            name = f"chat_{chat}"

            dead = db.get_full_info("state", name, "object_id", "слаб")
            dead = [x for l in dead for x in l]

            for member in dead:

                users_info = await api.users.get(member)
                first_name = users_info[0].first_name
                last_name = users_info[0].last_name

                Date_of_death = db.get_info(member, name, "Date_of_death")
                low_time = datetime(*ast.literal_eval(Date_of_death))

                if low_time < datetime.now():

                    db.update_info(member, name, "state", "мёртв")
                    await api.messages.send(
                        peer_id=chat,
                        message=f"[id{member}|{first_name} {last_name}], твой ёжик умер.",
                        random_id=m.random_id
                    )


@creator_labeler.message(creator_rule(), text=["SQL-debug", "SQL-debug <user>"])
async def SQL_debug(m: Message, user=None):
    if user is None:
        id = db.get_info(m.from_id, f"chat_{m.peer_id}", "id")
        object_id = db.get_info(m.from_id, f"chat_{m.peer_id}", "object_id")
        hedgehog = db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog")
        hedgehog_name = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "hedgehog_name")
        state = db.get_info(m.from_id, f"chat_{m.peer_id}", "state")
        Date_of_death = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "Date_of_death")
        hunger = db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger")
        is_starving = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "is_starving")
        remove_hedgehog = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "remove_hedgehog")
        feeding_time = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "feeding_time")
        working_time = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "working_time")
        apples = db.get_info(m.from_id, f"chat_{m.peer_id}", "apples")
        hedgehog_at_work = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "hedgehog_at_work")

        await m.answer(
            f"id: {id}\n"
            f"object_id: {object_id}\n"
            f"hedgehog: {hedgehog}\n"
            f"hedgehog_name: {hedgehog_name}\n"
            f"state: {state}\n"
            f"Date_of_death: {Date_of_death}\n"
            f"hunger: {hunger}\n"
            f"is_starving: {is_starving}\n"
            f"remove_hedgehog: {remove_hedgehog}\n"
            f"feeding_time: {feeding_time}\n"
            f"working_time: {working_time}\n"
            f"apples: {apples}\n"
            f"hedgehog_at_work: {hedgehog_at_work}\n"
        )

    else:
        user = re.findall(r"[0-9]+", user)[0]

        id = db.get_info(user, f"chat_{m.peer_id}", "id")
        object_id = db.get_info(user, f"chat_{m.peer_id}", "object_id")
        hedgehog = db.get_info(user, f"chat_{m.peer_id}", "hedgehog")
        hedgehog_name = db.get_info(user, f"chat_{m.peer_id}", "hedgehog_name")
        state = db.get_info(user, f"chat_{m.peer_id}", "state")
        Date_of_death = db.get_info(user, f"chat_{m.peer_id}", "Date_of_death")
        hunger = db.get_info(user, f"chat_{m.peer_id}", "hunger")
        is_starving = db.get_info(user, f"chat_{m.peer_id}", "is_starving")
        remove_hedgehog = db.get_info(
            user, f"chat_{m.peer_id}", "remove_hedgehog")
        feeding_time = db.get_info(user, f"chat_{m.peer_id}", "feeding_time")
        working_time = db.get_info(user, f"chat_{m.peer_id}", "working_time")
        apples = db.get_info(user, f"chat_{m.peer_id}", "apples")
        hedgehog_at_work = db.get_info(
            user, f"chat_{m.peer_id}", "hedgehog_at_work")

        await m.answer(
            f"id: {id}\n"
            f"object_id: {object_id}\n"
            f"hedgehog: {hedgehog}\n"
            f"hedgehog_name: {hedgehog_name}\n"
            f"state: {state}\n"
            f"Date_of_death: {Date_of_death}\n"
            f"hunger: {hunger}\n"
            f"is_starving: {is_starving}\n"
            f"remove_hedgehog: {remove_hedgehog}\n"
            f"feeding_time: {feeding_time}\n"
            f"working_time: {working_time}\n"
            f"apples: {apples}\n"
            f"hedgehog_at_work: {hedgehog_at_work}\n"
        )
