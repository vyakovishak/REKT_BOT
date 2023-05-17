from utils.db_api.sqlDatabase import Database
from utils.set_bot_commands import set_default_commands
from loader import db, bot


async def on_startup(dp):
    import filters
    import middlewares
    db.create_table_users()
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)

    try:
            scheduler.start()
            await dp.start_polling()
    finally:
            await dp.storage.close()
            await dp.storage.wait_closed()
            await bot.session.close()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
