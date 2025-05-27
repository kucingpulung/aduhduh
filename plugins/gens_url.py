from hydrogram import Client, filters
from hydrogram.helpers import ikb
from hydrogram.types import Message

from bot import authorized_users_only, config, helper_handlers, logger, url_safe
from plugins import list_available_commands
from db_func import get_custom_caption  # Tambahan

@Client.on_message(
    filters.private & ~filters.me & ~filters.command(list_available_commands)
)
@authorized_users_only
async def generate_handler(client: Client, message: Message) -> None:
    if not helper_handlers.generate_status:
        return

    try:
        database_chat_id = config.DATABASE_CHAT_ID
        message_db = await message.copy(database_chat_id)

        encoded_data = url_safe.encode_data(
            f"id-{message_db.id * abs(database_chat_id)}"
        )
        encoded_data_url = f"https://t.me/{client.me.username}?start={encoded_data}"
        share_encoded_data_url = f"https://t.me/share/url?url={encoded_data_url}"

        # Ambil custom caption
        custom_caption = await get_custom_caption()
        final_caption = custom_caption.replace("{original_caption}", encoded_data_url)

        await message.reply_text(
            final_caption,
            quote=True,
            reply_markup=ikb([[("Share", share_encoded_data_url, "url")]]),
            disable_web_page_preview=True,
        )
    except Exception as exc:
        logger.error(f"Generator: {exc}")
        await message.reply_text("<b>An Error Occurred!</b>", quote=True)
