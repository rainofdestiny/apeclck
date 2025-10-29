import httpx
from aiogram import types
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd import Select

from bot.config import settings
from bot.models import CreateRequest
from bot.utils import random_code


name_input = TextInput(id="name_input", type_factory=str)


async def on_random_name(c: types.CallbackQuery, b: Button, dm: DialogManager):
    dm.dialog_data["name"] = random_code()
    await dm.update({"name": dm.dialog_data["name"]})


async def on_name_entered(m: Message, w: TextInput, dm: DialogManager, value: str):
    value = value.strip()
    if not value:
        await m.answer("Укажи непустое имя или нажми кубик.")
        return
    dm.dialog_data["name"] = value
    await dm.next()


async def set_logger_yes(c: types.CallbackQuery, b: Button, dm: DialogManager):
    dm.dialog_data["enable_logger"] = True
    await dm.next()


async def set_logger_no(c: types.CallbackQuery, b: Button, dm: DialogManager):
    dm.dialog_data["enable_logger"] = False
    await dm.next()


async def on_ttl_selected(
    c: types.CallbackQuery, w: Select, dm: DialogManager, item: int
):
    dm.dialog_data["ttl"] = int(item)
    # call backend
    data = CreateRequest(
        url=dm.dialog_data["original_url"],
        name=dm.dialog_data["name"],
        enable_logger=dm.dialog_data["enable_logger"],
        ttl=dm.dialog_data["ttl"],
    ).model_dump()
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(f"{settings.api_url}/api", json=data)
        if r.status_code != 200:
            await c.message.answer(f"Ошибка API: {r.status_code} {r.text}")  # type: ignore
            await dm.done()
            return
        payload = (
            r.json()
        )  # ожидаем {"short_url": "https://apeclck.ru/xxxxxx"} или {"code": "xxxxxx"}
    short_url = payload.get("short_url")
    if not short_url:
        code = payload.get("code") or dm.dialog_data["name"]
        short_url = f"{settings.domain}/{code}"

    await c.message.answer(f"Готово: {short_url}")  # type: ignore
    await dm.done()
