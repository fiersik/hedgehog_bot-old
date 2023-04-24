from vkbottle import VKAPIError
from vkbottle.bot import BotLabeler, Message, rules
from modules import Mykeyboard as MK
from config import api, db


new_chat_labeler = BotLabeler()
new_chat_labeler.vbml_ignore_case = True


@new_chat_labeler.chat_message((rules.ChatActionRule("chat_invite_user")))
async def user_joined(m: Message) -> None:
    if m.action.member_id == -m.group_id:

        db.create_table(f"chat_{m.peer_id}")
        if not db.object_exists(m.peer_id, "chat_stat"):
            db.add_object(m.peer_id, "chat_stat")

        await m.answer(
            "Привет\n"
            "Пожалуйста дайте мне права админестратора.",
            keyboard=MK.start_keyboard
        )
    elif m.action.member_id > 0:

        vk_id = m.action.member_id

        users_info = await api.users.get(vk_id)
        first_name = users_info[0].first_name
        last_name = users_info[0].last_name

        await m.answer(
            f"Привет {first_name} {last_name}"
        )

        if not db.object_exists(vk_id, f"chat_{m.peer_id}"):
            db.add_object(vk_id, f"chat_{m.peer_id}")
        if not db.object_exists(vk_id, "user_stat"):
            db.add_object(vk_id, "user_stat")


@new_chat_labeler.chat_message((rules.ChatActionRule("chat_invite_user_by_link")))
async def user_joined_by_link(m: Message) -> None:

    vk_id = m.action.member_id

    users_info = await api.users.get(vk_id)
    first_name = users_info[0].first_name
    last_name = users_info[0].last_name

    await m.answer(
        f"Привет {first_name} {last_name}"
    )

    if not db.object_exists(vk_id, f"chat_{m.peer_id}"):
        db.add_object(vk_id, f"chat_{m.peer_id}")
    if not db.object_exists(vk_id, "user_stat"):
        db.add_object(vk_id, "user_stat")


@new_chat_labeler.message(payload = {"admin": "check"})
async def admin_check(m: Message):
    try:
        members = await api.messages.get_conversation_members(m.peer_id)
        for member in members.items:
            vk_id = member.member_id
            if vk_id > 0:
                if not db.object_exists(vk_id, f"chat_{m.peer_id}"):
                    db.add_object(vk_id, f"chat_{m.peer_id}")
                if not db.object_exists(vk_id, "user_stat"):
                    db.add_object(vk_id, "user_stat")

        await m.answer("спасибо, я готов к работе")

    except VKAPIError[917]:
        await m.answer("Права админестратора не получены")
