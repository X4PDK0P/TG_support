import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from aiogram.methods.forward_message import ForwardMessage


API_TOKEN = 'TOKEN'
TARGET_CHAT_ID = -1001234567890

dp = Dispatcher()


@dp.message(Command("start"), F.chat.type == "private")
async def start_command(message: types.Message) -> None:
    await message.reply("Привет! Я бот службы поддержки [Проект]."
                        "Просто напиши нам свой вопрос или сообщение, и тебе ответит оператор!")


@dp.message(F.chat.type == "private")
async def message_handler(message: types.Message) -> None:
    await bot(ForwardMessage(chat_id=TARGET_CHAT_ID, from_chat_id=message.chat.id, message_id=message.message_id))


@dp.message(F.chat.id == TARGET_CHAT_ID)
async def support_message_handler(message: types.Message) -> None:
    try:
        await bot(ForwardMessage(chat_id=message.reply_to_message.forward_from.id, from_chat_id=TARGET_CHAT_ID,
                                message_id=message.message_id))
    except:
        pass


async def main() -> None:
    global bot
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Завершение работы SUPPORT бота")
