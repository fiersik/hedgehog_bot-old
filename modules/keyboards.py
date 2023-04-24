from vkbottle import Keyboard, KeyboardButtonColor, Text


class Mykeyboard:

    start_keyboard = {
        Keyboard(inline=True)
        .add(Text("Проверить", payload = {"admin": "check"}), color = KeyboardButtonColor.POSITIVE, )
    }
