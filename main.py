import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = "8771131700:AAEauoHEPmXfU0nxR5NaAl1gE3MXJxaIdWQ"

# Текст и фото для кнопки "Подать заявку"
text4 = "🔴 https://docs.google.com/forms/d/e/1FAIpQLSdLCYNJj8xVunkZKKnMeJkKUG4k1nHYEo8J1l9qHoDX18JO3g/viewform?usp=dialog 🔴"

# ССЫЛКИ НА ФОТО (ЗАМЕНИТЕ НА СВОИ)
PHOTO_START = "https://kappa.lol/v03Ziu"  # Фото для команды /start
PHOTO_BUY_PASS = "https://kappa.lol/SZivBN"  # Фото для покупки проходки
PHOTO_SUBMIT_REQUEST = "https://kappa.lol/CqVnrk"  # Фото для заявки

# ========== ЛОГИРОВАНИЕ ==========
logging.basicConfig(level=logging.INFO)

# ========== ИНИЦИАЛИЗАЦИЯ ==========
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== КЛАВИАТУРЫ ==========
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎟 Купить проходку", callback_data="buy_pass")],
        [InlineKeyboardButton(text="📝 Подать заявку", callback_data="submit_request")]
    ])

# ========== ОБРАБОТЧИКИ ==========

# Старт с фото
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer_photo(
        photo=PHOTO_START,  # Отправляем фото
        caption="👋 Добро пожаловать!\nВыберите действие:",
        reply_markup=main_menu()
    )

# Обработка нажатия на "Купить проходку" с фото
@dp.callback_query(F.data == "buy_pass")
async def buy_pass(callback: CallbackQuery):
    await callback.answer()
    
    await callback.message.answer_photo(
        photo=PHOTO_BUY_PASS,
        caption="🔴 https://www.donationalerts.com/r/slimehook 🔴"
    )

# Обработка нажатия на "Подать заявку" с фото
@dp.callback_query(F.data == "submit_request")
async def submit_request(callback: CallbackQuery):
    await callback.answer()
    
    await callback.message.answer_photo(
        photo=PHOTO_SUBMIT_REQUEST,
        caption=text4
    )

# ========== ЗАПУСК ==========
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
