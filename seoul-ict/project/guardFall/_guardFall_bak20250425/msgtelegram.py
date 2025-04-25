import asyncio
import streamlit as st
import util as ut
from telegram import Bot
import toml
import os

TELEGRAM_TOKEN = st.secrets['telegram']['TELEGRAM_TOKEN']
CHAT_ID = st.secrets['telegram']['CHAT_ID']

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(text: str):
    await bot.send_message(chat_id=CHAT_ID, text=text)

# 필요 시 main에서 비동기 호출용 래퍼 함수
def send_message(text: str):
    asyncio.run(send_telegram_message(text))
