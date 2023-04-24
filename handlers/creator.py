from vkbottle.bot import BotLabeler, Message, rules
from modules import creator_rule


creator_labeler = BotLabeler()
creator_labeler.vbml_ignore_case = True


#Bot creator commands

#creator_labeler.message(creator_rule(), text = "")
#creator_labeler.chat_message(creator_rule(), text = "")
