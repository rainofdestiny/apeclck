from aiogram_dialog import Dialog
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd import Row
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.text import Format

from bot.config import settings
from bot.states import ShortenerSG
from bot.widgets import name_input
from bot.widgets import on_name_entered
from bot.widgets import on_random_name
from bot.widgets import on_ttl_selected
from bot.widgets import set_logger_no
from bot.widgets import set_logger_yes


dialog = Dialog(
    Window(
        Format("Оригинал: {original_url}\n\nУкажи короткое имя или жми кубик."),
        Row(
            Button(Const("🎲 Кубик"), id="roll", on_click=on_random_name),
        ),
        name_input,
        Format("Текущее имя: {name}"),
        state=ShortenerSG.ENTER_NAME,
        getter=lambda **data: {"name": data["dialog_data"].get("name", "")},  # type: ignore
        on_success=on_name_entered,
    ),
    Window(
        Const("Включить логер для ссылки?"),
        Row(
            Button(Const("Да"), id="logger_yes", on_click=set_logger_yes),
            Button(Const("Нет"), id="logger_no", on_click=set_logger_no),
        ),
        state=ShortenerSG.ENABLE_LOGGER,
    ),
    Window(
        Const("Срок жизни ссылки:"),
        Select(
            Format("{item[0]}"),
            id="ttl_select",
            item_id_getter=lambda x: x[1],
            items=settings.ttl_choices,
            on_click=on_ttl_selected,
        ),
        state=ShortenerSG.TTL,
    ),
)
