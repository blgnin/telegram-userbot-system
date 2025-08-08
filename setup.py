from setuptools import setup, find_packages

setup(
    name="telegram-userbot-system",
    version="1.0.0",
    description="Telegram Userbot System for GOMINIAPP",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "telethon==1.34.0",
        "openai==1.3.0", 
        "python-dotenv==1.0.0",
        "aiohttp==3.9.1",
        "python-telegram-bot==20.7"
    ],
    entry_points={
        "console_scripts": [
            "shlyapa-bot=main:main",
        ],
    },
)
