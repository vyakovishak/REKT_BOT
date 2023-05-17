from pprint import pprint

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callBack_data import callBack_button

def list_buttons(buttonNum :dict) :
     inner_list = []
     for index, key in enumerate(buttonNum):
             inner_list.append(InlineKeyboardButton(text=key, callback_data=callBack_button.new(choice_name=buttonNum.get(key)[0], value=buttonNum.get(key)[1])))
     keyboard = InlineKeyboardMarkup()
     for row in separate_list(inner_list, 3):
         keyboard.row(*row)
     return keyboard

def separate_list(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

def one_button(name: str, value: str):
    return InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(
                                            text=name,
                                            callback_data=callBack_button.new(choice_name=name, value=value)
                                        )
                                    ]
                                ])


