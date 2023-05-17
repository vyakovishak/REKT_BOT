from aiogram import types
from loader import dp, db


@dp.message_handler()
async def bot_echo(message: types.Message):
    userProfile = db.select_user(ids=message.from_user.id)
    print(userProfile[12])
    await message.answer(message.chat.id)
    if userProfile[12] >= 3:
        await message.answer("Sorry u baned, suck a dick")
