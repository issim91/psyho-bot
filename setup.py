from setuptools import setup, find_packages

setup(
    name="psychobot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "aiogram==3.3.0",
        "python-dotenv==1.0.0",
        "openai>=1.76.2",
        "sqlalchemy==2.0.25",
        "asyncpg==0.29.0",
        "aiohttp==3.9.3",
        "python-dateutil==2.8.2",
        "greenlet>=3.0.0",
    ],
) 