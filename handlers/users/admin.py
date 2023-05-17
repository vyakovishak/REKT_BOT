import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from eth_account import Account
from keyboards.inline.callBackButtons import  one_button, list_buttons
from keyboards.inline.callBack_data import callBack_button
from loader import dp, db, bot, Chain
from states.verifyProcess import ProfileSetup


@dp.message_handler(commands="unban")
async def unban_user(message: types.Message):
    all_baned_users =  db.get_all_banned_users()
    banned_users = " ".join(f"\n<b>User Index</b> {all_baned_users.index(username)}\n"
                            f"\n<b>User ID:</b> <code>{username[0]}</code>\n"
                            f"<b>Name:</b> {username[1]}\n"
                            f"<b>Username:</b> {username[2]}\n"
                            f"-------------------------------"
                            for username in all_baned_users)
    users = [( all_baned_users.index(username), ("unban",username[0])) for username in all_baned_users]
    await message.answer(banned_users , reply_markup= await list_buttons(dict(users)))


@dp.callback_query_handler(callBack_button.filter(choice_name='unban'))
async def transaction_getter(call: CallbackQuery):
    user_id = call.data.split(":")[2]
    db.update_warnings(0,user_id)
    userdata = db.select_user(ids=user_id)[6]
    await call.answer(f"User '{userdata[2]}' is unban now!")


