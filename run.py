import os
import sys

# Добавляем текущую директорию в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from psychobot.main import main
import asyncio

if __name__ == '__main__':
    asyncio.run(main()) 