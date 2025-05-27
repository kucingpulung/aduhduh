from bot.base import database
from bot.utils import BOT_ID

CAPTION_KEY = "CUSTOM_CAPTION"

async def set_custom_caption(template: str) -> None:
    await database.add_value(int(BOT_ID), CAPTION_KEY, template)

async def get_custom_caption() -> str:
    doc = await database.get_doc(int(BOT_ID))
    return doc.get(CAPTION_KEY, ["{original_caption}"])[0]

async def reset_custom_caption() -> None:
    await database.clear_value(int(BOT_ID), CAPTION_KEY)
