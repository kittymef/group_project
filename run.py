import asyncio
import logging 

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import router 
from training import router as training_router
from app.database.models import async_main


bot = Bot(token=TOKEN)
dp = Dispatcher() 


# Этапы разговора
LANG_SELECT, WORD_INPUT, TRANSLATION_INPUT = range(3)


#запуск бота
async def main():
    await async_main()
    dp.include_router(router)
    dp.include_router(training_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')