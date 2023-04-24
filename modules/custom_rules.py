from vkbottle import API
from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import Message
from typing import Union, List


api = API("vk1.a.UOuZDDtuLeOAde3haH3WPOZ3V2Z7Mbp-FE3apBCQZyyjXmGLnc5u5ikVVwUa8pd6fLBj_3m0HnCaZsYes8Gp70bHpTMXw_hsEUHh_UZGwPuAovSjeapZnrR5REVfwtKVSlVM1sGnGzt6GjTDdw7VPpRXSBoXsDnrBa1KhNhYOptWps8AOi6QB9fq3PbbVa2_jl-8ZltmItuj2jk0LN99Dw")


class admin_rule(ABCRule[Message]):

    async def check(self, event: Message) -> bool:

        members = await api.messages.get_conversation_members(event.peer_id)

        admins = []

        for member in members.items:
            if member.is_admin:
                admins.append(member.member_id)

        return event.from_id in admins


class creator_rule(ABCRule[Message]):

    async def check(self, event: Message) -> bool:
        return event.from_id == 603843114
