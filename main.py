import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = "8771131700:AAEauoHEPmXfU0nxR5NaAl1gE3MXJxaIdWQ"

# ССЫЛКИ НА ФОТО
PHOTO_START = "https://kappa.lol/v03Ziu"           # Фото для команды /start
PHOTO_BUY_PASS = "https://kappa.lol/SZivBN"        # Фото для покупки проходки
PHOTO_SUBMIT_REQUEST = "https://kappa.lol/CqVnrk"  # Фото для заявки
PHOTO_BUILD = "https://kappa.lol/hv65Ql"           # Фото для сборки
PHOTO_SUPPORT = "https://kappa.lol/pVzeH4"         # Фото для тех-поддержки

# ССЫЛКИ
LINK_BUY_PASS = "https://www.donationalerts.com/r/slimehook"
LINK_SUBMIT_REQUEST = "https://docs.google.com/forms/d/e/1FAIpQLSdLCYNJj8xVunkZKKnMeJkKUG4k1nHYEo8J1l9qHoDX18JO3g/viewform?usp=dialog"
LINK_BUILD_MAIN = "https://workupload.com/file/eVWN7cH3m7R"
LINK_BUILD_MIRROR = "https://drive.google.com/file/d/1OPbJKM47RcvVt1InJj1FX81yz0HJKhz1/view?usp=sharing"
LINK_SUPPORT = "https://t.me/SLIMEHOOK"

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
        [InlineKeyboardButton(text="📲 Тех-поддержка", callback_data="support")]
    ])

def back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀ Назад в меню", callback_data="back_to_main")]
    ])

def build_menu():
    """Меню выбора внутри раздела Сборка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 Скачать", url=LINK_BUILD_MAIN)],  # Прямая ссылка
        [InlineKeyboardButton(text="🪞 Зеркало", callback_data="build_mirror")],
        [InlineKeyboardButton(text="◀ Назад в меню", callback_data="back_to_main")]
    ])

def mirror_menu():
    """Меню для зеркала"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 Скачать", url=LINK_BUILD_MIRROR)],  # Прямая ссылка
        [InlineKeyboardButton(text="◀ Назад в сборку", callback_data="build")]
    ])

# ========== ОБРАБОТЧИКИ ==========

# Старт
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
        caption="💵 Нажмите на кнопку ниже, чтобы купить:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💵 Купить", url=LINK_BUY_PASS)],
            [InlineKeyboardButton(text="◀ Назад в меню", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

# Подача заявки
@dp.callback_query(F.data == "submit_request")
async def submit_request(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=PHOTO_SUBMIT_REQUEST,
        caption="📜 Нажмите на кнопку ниже, чтобы подать заявку:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📜 Подать заявку", url=LINK_SUBMIT_REQUEST)],
            [InlineKeyboardButton(text="◀ Назад в меню", callback_data="back_to_main")]
        ])
    )
    await callback.answer()

# Сборка - показываем меню выбора
@dp.callback_query(F.data == "build")
async def build_info(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=PHOTO_BUILD,
        caption="📦 Выберите вариант скачивания:",
        reply_markup=build_menu()
    )
    await callback.answer()

# Зеркало сборки
@dp.callback_query(F.data == "build_mirror")
async def build_mirror_link(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=PHOTO_BUILD,
        caption="🪞 Скачайте файл по ссылке ниже:",
        reply_markup=mirror_menu()
    )
    await callback.answer()

# Тех-поддержка
@dp.callback_query(F.data == "support")
async def support_info(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=PHOTO_SUPPORT,
        caption="📲 Нажмите на кнопку ниже, чтобы связаться с поддержкой:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📲 Тех-поддержка", url=LINK_SUPPORT)],
            [InlineKeyboardButton(text="◀ Назад в меню", callback_data="back_to_main")]
        ])
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
