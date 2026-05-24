from vkbottle import PhotoMessageUploader,Bot

async def send_photo(name:str, bot:Bot):
    photo_uploader = PhotoMessageUploader(bot.api)
    image = await photo_uploader.upload(f"images/{name}.jpeg")
    return image
