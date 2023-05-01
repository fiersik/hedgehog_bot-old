import asyncio
import codecs

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import BotLabeler, Message
from config import api, db
from modules import Mykeyboard as MK
from datetime import datetime, timedelta
import ast

Basic_labeler = BotLabeler()
Basic_labeler.vbml_ignore_case = True


# basic commands


@Basic_labeler.chat_message(text="взять ёжика")
async def take_a_hedgehog(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog") is None and db.get_info(m.peer_id, "chat_stat", "new_hedgehog") is not None:

        hedgehog = db.get_info(m.peer_id, "chat_stat", "new_hedgehog")
        db.update_info(m.from_id, f"chat_{m.peer_id}", "hedgehog", hedgehog)
        db.update_info(m.peer_id, "chat_stat", "new_hedgehog", None)

        await m.answer(
            "Вы взяли ёжика"
        )

    elif db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog") is not None:
        await m.answer("У вас уже есть ёжик")
    else:
        await m.answer("В вашей беседе нет свободного ёжика")


@Basic_labeler.chat_message(text=["мой ёжик", "[club219000856|@myhedgehog_bot] мой ёжик"])
async def my_hedgehog(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog") is None:
        await m.answer(
            "У вас нет ёжика"
        )
        return

    name = db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog_name")
    state = db.get_info(m.from_id, f"chat_{m.peer_id}", "state")
    hunger = db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger")
    apples = db.get_info(m.from_id, f"chat_{m.peer_id}", "apples")

    await m.answer(
        "Ваш ёжик:\n"
        f"Имя: {name}.\n"
        f"Cостояние: {state}.\n"
        f"Сытость: {hunger}.\n"
        f"Яблочки: {apples}.\n",
        attachment=db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog"),
    )


@Basic_labeler.chat_message(text=["ёжик инфо", "[club219000856|@myhedgehog_bot] ёжик инфо"])
async def hedgehog_information(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "state") != "мёртв":

        feeding_time = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "feeding_time")
        working_time = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "working_time")

        keyboard = Keyboard(inline=True)

        if not feeding_time is None:
            low_f_time = datetime(*ast.literal_eval(feeding_time))
        if not working_time is None:
            low_w_time = datetime(*ast.literal_eval(working_time))

        if feeding_time is None or low_f_time < datetime.now():
            feeding_info = "Ёжика можно покормить.\n"
            keyboard.add(Text("Покормить ёжика"),
                         color=KeyboardButtonColor.POSITIVE)
            keyboard.row()
        else:
            time_f = low_f_time - datetime.now()
            time_f = time_f.seconds
            hour_f = time_f / 60 // 60
            minutes_f = time_f - hour_f*60*60
            minutes_f = minutes_f // 60

            feeding_info = f"Можно покормить через {int(hour_f)} ч. {int(minutes_f)} м.\n"

        if working_time is None or low_w_time < datetime.now():
            if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog_at_work") != 1:
                working_info = "Ёжика можно отправить на работу.\n"
                keyboard.add(Text("Отправить на работу"),
                             color=KeyboardButtonColor.POSITIVE)
                keyboard.row()
            else:
                working_info = "Ёжика можно забрать с работы.\n"
                keyboard.add(Text("Завершить работу"),
                             color=KeyboardButtonColor.POSITIVE)
                keyboard.row()
        else:
            if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog_at_work"):

                time_w = low_w_time - datetime.now()
                time_w = time_w.seconds
                hour_w = time_w / 60 // 60
                minutes_w = time_w - hour_w*60*60
                minutes_w = minutes_w // 60

                working_info = f"Можно забрать с работы через {int(hour_w)} ч. {int(minutes_w)} м.\n"

        info = feeding_info + working_info
        keyboard.add(Text("Мой ёжик"))

        await m.answer(
            info,
            keyboard=keyboard
        )

    else:
        await m.answer(
            "Ваш ёжик мёртв :("
        )

@Basic_labeler.chat_message(text=["покормить ёжика", "[club219000856|@myhedgehog_bot] покормить ёжика"])
async def feed_the_hedgehog(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "state") != "мёртв":

        if db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger") == 24:
            await m.answer(
                "Ваш ёжик не хочет есть."
            )
            return

        feeding_time = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "feeding_time")

        if feeding_time is None:

            hunger = db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger")
            hunger += 1
            db.update_info(m.from_id, f"chat_{m.peer_id}", "hunger", hunger)

            now_time = datetime.now()
            now_time += timedelta(hours=4)
            feeding_time = f"[{now_time.year}, {now_time.month}, {now_time.day}, {now_time.hour}, {now_time.minute}, {now_time.second}]"

            db.update_info(
                m.from_id, f"chat_{m.peer_id}", "feeding_time", feeding_time)
            db.update_info(
                m.from_id, f"chat_{m.peer_id}", "state", "жив")

            await m.answer(
                "Вы успешно покормили ежа.\n"
                f"Сытость: {hunger}/24"
            )

            return

        low_time = datetime(*ast.literal_eval(feeding_time))

        if low_time < datetime.now():

            hunger = db.get_info(m.from_id, f"chat_{m.peer_id}", "hunger")
            hunger += 1
            db.update_info(m.from_id, f"chat_{m.peer_id}", "hunger", hunger)

            now_time = datetime.now()
            now_time += timedelta(hours=4)
            feeding_time = f"[{now_time.year}, {now_time.month}, {now_time.day}, {now_time.hour}, {now_time.minute}, {now_time.second}]"

            db.update_info(
                m.from_id, f"chat_{m.peer_id}", "feeding_time", feeding_time)
            db.update_info(
                m.from_id, f"chat_{m.peer_id}", "state", "жив")

            await m.answer(
                "Вы успешно покормили ежа.\n"
                f"Сытость: {hunger}/24"
            )

        else:
            time = low_time - datetime.now()
            time = time.seconds
            hour = time / 60 // 60
            minutes = time - hour*60*60
            minutes = minutes // 60

            await m.answer(
                "Кормить ежа можно раз в 4 часа\n"
                f"Следующий раз через {int(hour)} ч. {int(minutes)} мин."
            )

    else:
        await m.answer(
            "Ваш ёжик мёртв :("
        )


@Basic_labeler.chat_message(text=["Отправить ёжика на работу", "Отправить на работу", "[club219000856|@myhedgehog_bot] Отправить на работу"])
async def hedgehog_work(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "state") != "мёртв":

        if db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog_at_work"):

            low_working_time = db.get_info(
                m.from_id, f"chat_{m.peer_id}", "working_time")
            low_time = datetime(*ast.literal_eval(low_working_time))

            if low_time < datetime.now():
                await m.answer(
                    "Сначала заберите ёжика с работы."
                )
            else:
                time = low_time - datetime.now()
                time = time.seconds
                hour = time / 60 // 60
                minutes = time - hour*60*60
                minutes = minutes // 60

                await m.answer(
                    "Ваш ёжик ещё работает.\n"
                    f"Можно будет забрать через {int(hour)} ч. {int(minutes)} м."
                )

            return

        low_working_time = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "working_time")

        if low_working_time is None:

            db.update_info(
                m.from_id, f"chat_{m.peer_id}", "hedgehog_at_work", 1)

            now_time = datetime.now()
            now_time += timedelta(hours=2)
            working_time = f"[{now_time.year}, {now_time.month}, {now_time.day}, {now_time.hour}, {now_time.minute}, {now_time.second}]"

            db.update_info(
                m.from_id, f"chat_{m.peer_id}", "working_time", working_time)

            await m.answer(
                "Вы отправили ёжика на работу.\n"
                "Забрать его можно будет через 2 часа"
            )

            return

        low_time = datetime(*ast.literal_eval(low_working_time))

        if low_time < datetime.now():

            db.update_info(
                m.from_id, f"chat_{m.peer_id}", "hedgehog_at_work", 1)

            now_time = datetime.now()
            now_time += timedelta(hours=2)
            working_time = f"[{now_time.year}, {now_time.month}, {now_time.day}, {now_time.hour}, {now_time.minute}, {now_time.second}]"

            db.update_info(
                m.from_id, f"chat_{m.peer_id}", "working_time", working_time)

            await m.answer(
                "Вы отправили ёжика на работу.\n"
                "Забрать его можно будет через 2 часа"
            )

    else:
        await m.answer(
            "Ваш ёжик мёртв :("
        )

@Basic_labeler.chat_message(text=["Завершить работу", "[club219000856|@myhedgehog_bot] Завершить работу"])
async def to_finish_work(m: Message):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "state") != "мёртв":
        if not db.get_info(m.from_id, f"chat_{m.peer_id}", "hedgehog_at_work"):

            await m.answer(
                "Ваш ёжик сейчас не на работе"
            )
            return

        working_time = db.get_info(
            m.from_id, f"chat_{m.peer_id}", "working_time")
        low_time = datetime(*ast.literal_eval(working_time))

        if low_time < datetime.now():

            db.update_info(
                m.from_id, f"chat_{m.peer_id}", "hedgehog_at_work", 0)
            apples = db.get_info(m.from_id, f"chat_{m.peer_id}", "apples")
            apples += 20
            db.update_info(m.from_id, f"chat_{m.peer_id}", "apples", apples)

            await m.answer(
                "Вы забрали ёжика с работы.\n\n"
                "+ 20 яблочек"
            )

        else:
            time = low_time - datetime.now()
            time = time.seconds
            hour = time / 60 // 60
            minutes = time - hour*60*60
            minutes = minutes // 60

            await m.answer(
                "Ваш ёжик ещё работает.\n"
                f"Можно будет забрать через {int(hour)} ч. {int(minutes)} м."
            )

    else:
        await m.answer(
            "Ваш ёжик мёртв :("
        )


@Basic_labeler.chat_message(text=["дать ёжику имя", "дать ёжику имя <name>"])
async def my_hedgehog(m: Message, name=None):

    if db.get_info(m.from_id, f"chat_{m.peer_id}", "state") != "мёртв":
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

    else:
        await m.answer(
            "Ваш ёжик мёртв :("
        )


@Basic_labeler.chat_message(text="выкинуть ёжика")
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
        db.update_info(m.from_id, f"chat_{m.peer_id}", "state", "жив")
        db.update_info(m.from_id, f"chat_{m.peer_id}", "Date_of_death", None)
        db.update_info(m.from_id, f"chat_{m.peer_id}", "hunger", 24)
        db.update_info(m.from_id, f"chat_{m.peer_id}", "is_starving", 0)
        db.update_info(m.from_id, f"chat_{m.peer_id}", "remove_hedgehog", 0)
        db.update_info(m.from_id, f"chat_{m.peer_id}", "feeding_time", None)
        db.update_info(m.from_id, f"chat_{m.peer_id}", "working_time", None)
        db.update_info(m.from_id, f"chat_{m.peer_id}", "apples", 0)
        db.update_info(m.from_id, f"chat_{m.peer_id}", "hedgehog_at_work", 0)

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
