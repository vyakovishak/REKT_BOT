from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import BOT_TOKEN
from utils.Blockchain.ConnectToChain import BlockChainConnect
from utils.db_api.sqlDatabase import Database

bot: Bot = Bot(token="API_Key", parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
Chain = BlockChainConnect(chainName="DOGE")
