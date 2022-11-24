from aiogram import Bot, Dispatcher #, executor, types
import config


bot = Bot(token = config.TOKEN)
# storage = MemoryStorage()
dp = Dispatcher(bot)

print("Запуск")