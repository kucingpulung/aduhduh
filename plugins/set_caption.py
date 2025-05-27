from hydrogram import Client, filters
from hydrogram.types import Message

from bot import authorized_users_only
from db_func.caption import set_custom_caption, get_custom_caption, reset_custom_caption


@Client.on_message(filters.command("setcaption"))
@authorized_users_only
async def set_caption_handler(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.text:
        return await message.reply(
            "Balas pesan ini dengan template caption.\nGunakan <code>{original_caption}</code> sebagai placeholder.",
            parse_mode="html"
        )

    caption_template = message.reply_to_message.text
    await set_custom_caption(caption_template)
    await message.reply("✅ Custom caption berhasil diatur!")


@Client.on_message(filters.command("getcaption"))
@authorized_users_only
async def get_caption_handler(client: Client, message: Message):
    template = await get_custom_caption()
    await message.reply(f"📝 Caption saat ini:\n\n<code>{template}</code>", parse_mode="html")


@Client.on_message(filters.command("resetcaption"))
@authorized_users_only
async def reset_caption_handler(client: Client, message: Message):
    await reset_custom_caption()
    await message.reply("♻️ Custom caption berhasil direset ke default.")
