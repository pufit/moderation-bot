from pyrogram import Client, filters
from pyrogram.types import Message

from antigrisha.censor import run_moderation
from antigrisha.config import Config

app = Client('stop_grisha_gay', api_id=Config.API_ID, api_hash=Config.API_HASH)


@app.on_message(filters=filters.photo | filters.sticker)
async def censor(_: Client, message: Message):
    is_animated = False
    if message.sticker is not None:
        file_id = message.sticker.file_id
        is_animated = message.sticker.is_animated
    else:
        file_id = message.photo.file_id

    file = await app.download_media(file_id, in_memory=True)

    # noinspection PyUnresolvedReferences
    results = await run_moderation(bytes(file.getbuffer()), is_animated=is_animated)
    print(f'Got img from {message.from_user.username}, results: {results}')

    if results.adult > 0.1:
        await message.forward('me')
        await message.reply('Никакого гейства в чате!')

        await message.delete()

    if results.gruesome > 0.4:
        await message.reply('Партия не гордится тобой!')
        await message.delete()
