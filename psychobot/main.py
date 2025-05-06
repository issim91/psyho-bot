import asyncio
import logging
from aiogram import Bot, Dispatcher
from psychobot.settings import API_TOKEN
from psychobot.db.database import init_db
from psychobot.bot.handlers import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
)

async def main():
    # Initialize database
    await init_db()
    
    # Initialize bot and dispatcher
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    
    # Include router
    dp.include_router(router)
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 
