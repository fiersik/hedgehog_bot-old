from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import Message
from typing import Union, List


class admin_rule(ABCRule[Message]):

    async def check(self, event: Message) -> bool:

        members = await event.ctx_api.messages.get_conversation_members(event.peer_id)
        admins = []

        for member in members.items:
            if member.is_admin:
                admins.append(member.member_id)

        return event.from_id in admins


class creator_rule(ABCRule[Message]):

    async def check(self, event: Message) -> bool:
        return event.from_id == 603843114
