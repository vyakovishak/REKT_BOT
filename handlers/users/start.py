import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from eth_account import Account
from keyboards.inline.callBackButtons import one_button
from keyboards.inline.callBack_data import callBack_button
from loader import dp, db, bot, Chain
from states.verifyProcess import ProfileSetup
from datetime import datetime, timedelta

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    fullName = message.from_user.full_name
    db.add_user(user_id, fullName, username)
    current_warnings_num = db.select_user(ids=message.from_user.id)[12]
    if current_warnings_num <= 3:
        await message.answer(f'Hello, <b>{message.from_user.full_name}</b>!\n\n '
                             f'Wellcome to VerifyBot!\n'
                             f'This bot will help you to verify your holding status and get access to a specific secret chat!\n'
                             f'Press <b>BIG FAT BUTTON</b> under this message to start the verification process',
                             reply_markup= one_button("BIG FAT BUTTON", "start"))
    else:
        await message.answer("Sorry, you been ban for not following rules.\n"
                             "To get second chance contact @dickhead")

@dp.callback_query_handler(callBack_button.filter(value='start'))
async def bot_verify(call: CallbackQuery):
    await rewrite_message(call=call, message="So there is couple steps to verify your holding status\n"
                                             "First send me your seed for your wallet")
    await ProfileSetup.userWallet.set()


@dp.message_handler(state=ProfileSetup.userWallet)
async def bot_verify(message: types, state: FSMContext):
    bad_answers = 0
    coinsLimit = 0
    answer = message.text.lower()
    if len(answer) == 42 and answer[:2] == '0x':
        userProfile = db.select_user(ids=message.from_user.id)
        if userProfile[12] <= 3:
            if userProfile[10] != "Done":
                if answer == str(userProfile[3]).lower():
                    userBalance = Chain.get_coin_balance(contractAddress="0x7fC009aDC0B7A5E9C81F2e0E7a14c6c281ABb99C", userAddress=answer)
                    if int(userBalance) >= coinsLimit:
                        await message.answer("Great! You have enough coins to get access to secret Chat!")
                        await state.update_data(verifyProcess="1")
                        await state.update_data(userWallet=answer)
                        await message.answer(f'Now send any  amount of native token to this address!')
                        await state.finish()
                        if userProfile[6] is not None:
                            await message.answer(f"<code>{userProfile[6]}</code>")
                        else:
                            Account.enable_unaudited_hdwallet_features()
                            acct, mnemonic = Account.create_with_mnemonic()
                            await message.answer(f"<code>{acct.address}</code>")
                            db.update_user_wallet(answer, message.from_user.id)
                            db.update_verification_wallet_address(acct.address, message.from_user.id)
                            db.update_verification_wallet_privet_seed(mnemonic, message.from_user.id)
                        await message.answer(f"Click Done when you finished",
                                             reply_markup=one_button("BIG FAT BUTTON 2", "verification"))
                    else:
                        await message.answer(f"You don't have enough coins to get access to secret Chat, inorder to get access to secret Chat buy this amount of coins {userBalance-coinsLimit}'")
                else:
                    current_warnings_num = userProfile[12]
                    print("Warnings: {}".format(current_warnings_num))
                    db.update_warnings(current_warnings_num+1, message.from_user.id)
                    if current_warnings_num <= 3:
                        await message.answer(f"Don't try to use someone else wallet! \n"
                                                f"You got {current_warnings_num} warning! {current_warnings_num-3} more warnings you will be ban!")
                    else:
                        await message.answer(f"You be banned!")
            else:
                await message.answer("You already verified")
        else:
            await message.answer("Sorry, you been ban for not following rules.\n"
                                 "To get second chance contact @dickhead")
    else:
        if 0 < bad_answers:
            await message.answer("Yo homi address that you send it incorrect, try again!")
            bad_answers += 1
            await ProfileSetup.verificationStep.set()
        else:
            await message.answer("Stop playing with me, send right address!!!")
            await ProfileSetup.verificationStep.set()


@dp.callback_query_handler(callBack_button.filter(value='verification'))
async def transaction_getter(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text("Now send me transaction",
                                call.message.chat.id,
                                call.message.message_id)

    await ProfileSetup.userTransaction.set()


@dp.message_handler(state=ProfileSetup.userTransaction)
async def bot_transaction(message: types.Message, state: FSMContext):
    answer = message.text
    tx_data = dict(Chain.get_transaction(answer))
    userData = db.select_user(ids=message.from_user.id)
    expiration_date = datetime.now() + timedelta(days=1)
    if userData[3] != tx_data["from"] and userData[6] != tx_data["to"]:
        invite = await bot.create_chat_invite_link(chat_id="-1001858981980",expire_date=expiration_date, member_limit=1, name="wellcome dickhead")
        await message.answer("Here is your invite link: "+ invite.invite_link)
        await message.answer("This link is only valid for one hour and only for one person!")
        await message.answer("Remember to have at lest this amount of coins in your wallet because if not, bot will remove you from group and you will get one warning!")
    else:
        await ProfileSetup.verificationStep.set()


async def rewrite_message(**kwargs):
    message = kwargs.get('message')
    callObject: CallbackQuery = kwargs.get('call')
    chat_id = callObject.message.chat.id
    message_id = callObject.message.message_id
    await bot.edit_message_text(text=message, chat_id=chat_id, message_id=message_id)
