import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = "8771131700:AAEauoHEPmXfU0nxR5NaAl1gE3MXJxaIdWQ"

# ССЫЛКИ НА ФОТО (ЗАМЕНИТЕ НА СВОИ)
PHOTO_START = "https://kappa.lol/v03Ziu"           # Фото для команды /start
PHOTO_BUY_PASS = "https://kappa.lol/SZivBN"        # Фото для покупки проходки
PHOTO_SUBMIT_REQUEST = "https://kappa.lol/CqVnrk"  # Фото для заявки
PHOTO_BUILD = "https://kappa.lol/hv65Ql"      # Фото для сборки (ЗАМЕНИТЕ!)
PHOTO_SUPPORT = "https://kappa.lol/pVzeH4"    # 🆕 Фото для тех-поддержки (ЗАМЕНИТЕ!)

# Текст для сообщений
TEXT_BUY_PASS = "🔴 https://www.donationalerts.com/r/slimehook 🔴"
TEXT_SUBMIT_REQUEST = "🔴 https://docs.google.com/forms/d/e/1FAIpQLSdLCYNJj8xVunkZKKnMeJkKUG4k1nHYEo8J1l9qHoDX18JO3g/viewform?usp=dialog 🔴"
TEXT_BUILD = "🔴 https://workupload.com/file/eVWN7cH3m7R 🔴"
TEXT_SUPPORT = "🔴 https://t.me/SLIMEHOOK 🔴"  # 🆕 Текст для тех-поддержки

# ========== ЛОГИРОВАНИЕ ==========
logging.basicConfig(level=logging.INFO)

# ========== ИНИЦИАЛИЗАЦИЯ ==========
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== КЛАВИАТУРЫ ==========
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎟 Купить проходку", callback_data="buy_pass")],
        [InlineKeyboardButton(text="📝 Подать заявку", callback_data="submit_request")],
        [InlineKeyboardButton(text="📎 Сборка", callback_data="build")],
        [InlineKeyboardButton(text="📲 Тех-поддержка", callback_data="support")]  # 🆕 Новая кнопка
    ])

def back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀ Назад в меню", callback_data="back_to_main")]
    ])

# ========== ОБРАБОТЧИКИ ==========

# Старт с фото
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer_photo(
        photo=PHOTO_START,
        caption="✨ Добро пожаловать!\nВыберите нужное действие:",
        reply_markup=main_menu()
    )

# Покупка проходки
@dp.callback_query(F.data == "buy_pass")
async def buy_pass(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=PHOTO_BUY_PASS,
        caption=TEXT_BUY_PASS,
        reply_markup=back_menu()
    )
    await callback.answer()

# Подача заявки
@dp.callback_query(F.data == "submit_request")
async def submit_request(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=PHOTO_SUBMIT_REQUEST,
        caption=TEXT_SUBMIT_REQUEST,
        reply_markup=back_menu()
    )
    await callback.answer()

# Сборка
@dp.callback_query(F.data == "build")
async def build_info(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=PHOTO_BUILD,
        caption=TEXT_BUILD,
        reply_markup=back_menu()
    )
    await callback.answer()

# 🆕 Тех-поддержка
@dp.callback_query(F.data == "support")
async def support_info(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=PHOTO_SUPPORT,
        caption=TEXT_SUPPORT,
        reply_markup=back_menu()
    )
    await callback.answer()

# Назад в главное меню
@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=PHOTO_START,
        caption="✨ Добро пожаловать!\nВыберите нужное действие:",
        reply_markup=main_menu()
    )
    await callback.answer()

# ========== ЗАПУСК ==========
async def main():
    print("✅ Бот успешно запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
