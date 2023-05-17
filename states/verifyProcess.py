from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileSetup(StatesGroup):
    userTime = State()
    userWallet = State()
    userTransaction = State()
    verificationStep = State()
