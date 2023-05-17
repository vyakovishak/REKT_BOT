from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Begin')
        ]
    ]
)

done = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='DONE')
        ]
    ]
)