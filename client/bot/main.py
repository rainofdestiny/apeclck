import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog import setup_dialogs
from redis.asyncio import from_url as redis_from_url

from bot.config import settings
from bot.dialog import dialog
from bot.states import ShortenerSG
from bot.utils import is_url


bot = Bot(
    settings.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode="html"),
)
dp = Dispatcher(storage=RedisStorage(redis_from_url(settings.redis_url)))
dp.include_router(dialog)


@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "The bot does not permanently store your data."
        "All created links and settings are automatically deleted after their expiration date."
    )


@dp.message(F.text)
async def text_entry(message: Message, dialog_manager: DialogManager):
    text = message.text.strip() if message.text else None

    if not is_url(text) or not text:
        await message.answer("Incorrect data")
        return
    await dialog_manager.start(
        ShortenerSG.ENTER_NAME,
        data={"original_url": text},
    )


async def main():
    setup_dialogs(dp)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
