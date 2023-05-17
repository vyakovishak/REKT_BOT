import asyncio
import math
import re
from datetime import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import db
from utils.ExchangeApi import BinancePairFinder


async def asMinutes(bot: Bot, scheduler: AsyncIOScheduler, minute, user_id):
    scheduler.add_job(checkUserBalance, 'interval', minutes=minute, args=(bot, user_id))


async def asHour(bot: Bot, scheduler: AsyncIOScheduler, hour, user_id):
    scheduler.add_job(checkUserBalance, 'interval', hours=hour, args=(bot, user_id))


async def asDay(bot: Bot, scheduler: AsyncIOScheduler, day, user_id):
    scheduler.add_job(checkUserBalance, 'interval', days=day, args=(bot, user_id))


async def checkUserBalance(bot: Bot):
    userProfiles = db.select_all_users()
    for user in userProfiles:
        userBalance = Chain.get_coin_balance(contractAddress="0x7fC009aDC0B7A5E9C81F2e0E7a14c6c281ABb99C", userAddress=user[3])
        if userBalance > 100:
            await bot.kick_chat_member(chat_id="-1001858981980", user_id=user[0],revoke_messages=False)

async def on_startup(scheduler):
    scheduler.start()


async def on_shutdown(scheduler):
    scheduler.shutdown


async def updateTradingData(bot: Bot, scheduler: AsyncIOScheduler):
    try:
        userTime = re.split('(\d+)', user[4])
        number = int(userTime[1])
        timeFormat = 'd'
        if timeFormat.lower() == "m":
            await asMinutes(bot, scheduler, number, user[0])
        elif timeFormat.lower() == "h":
            await asHour(bot, scheduler, number, user[0])
        elif timeFormat.lower() == "d":
            await asDay(bot, scheduler, number, user[0])
    except:
        pass
