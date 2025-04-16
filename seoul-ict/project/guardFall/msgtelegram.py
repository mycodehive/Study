import asyncio
import streamlit as st
import util as ut
from telegram import Bot
import toml
import os

# 로컬에서 원하는 경로로 지정하는 경우에만 -[------------------
"""
toml_path = os.path.join(ut.exedir("script"), "\\.streamlit\\secrets.toml")

print("exedir: ",ut.exedir("script"))
print("toml_path:", toml_path)

secrets = toml.load(toml_path)
"""

# -]-----------------------------------------------------

TELEGRAM_TOKEN = st.secrets['telegram']['TELEGRAM_TOKEN']
CHAT_ID = st.secrets['telegram']['CHAT_ID']

print("Telegram Token:", TELEGRAM_TOKEN)
print("Chat ID:", CHAT_ID)

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(text: str):
    await bot.send_message(chat_id=CHAT_ID, text=text)

# 필요 시 main에서 비동기 호출용 래퍼 함수
def send_message(text: str):
    asyncio.run(send_telegram_message(text))
