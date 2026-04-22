import asyncio
import logging
from typing import Optional

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = "8771131700:AAEauoHEPmXfU0nxR5NaAl1gE3MXJxaIdWQ"

# Ссылки
DONATION_LINK = "https://www.donationalerts.com/r/slimehook"
FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdLCYNJj8xVunkZKKnMeJkKUG4k1nHYEo8J1l9qHoDX18JO3g/viewform?usp=dialog"

# Тексты сообщений
WELCOME_TEXT = """
✨ <b>Добро пожаловать в бота!</b> ✨

Здесь вы можете:
🎟 <b>Купить проходку</b> на закрытые мероприятия
📝 <b>Подать заявку</b> на участие

Выберите действие ниже 👇
"""

BUY_PASS_TEXT = """
💎 <b>Покупка проходки</b> 💎

Для приобретения проходки перейдите по ссылке:

➡️ <a href="{link}"><b>Оплатить через DonationAlerts</b></a> ⬅️

После оплаты вы получите доступ к закрытому каналу с материалами.
"""

REQUEST_TEXT = """
📋 <b>Подача заявки</b> 📋

Для подачи заявки заполните форму:

➡️ <a href="{link}"><b>Открыть форму заявки</b></a> ⬅️

Наши менеджеры свяжутся с вами в ближайшее время!
"""

# ========== ЛОГИРОВАНИЕ ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== ИНИЦИАЛИЗАЦИЯ ==========
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ========== КЛАВИАТУРЫ ==========
def get_main_menu() -> InlineKeyboardMarkup:
    """Главное меню с красивыми кнопками"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎟 Купить проходку",
                callback_data="buy_pass"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Подать заявку",
                callback_data="submit_request"
            )
        ],
        [
            InlineKeyboardButton(
                text="❓ Помощь",
                callback_data="help"
            )
        ]
    ])


def get_back_button() -> InlineKeyboardMarkup:
    """Кнопка возврата в главное меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_menu")]
    ])


# ========== ОБРАБОТЧИКИ ==========

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    try:
        # Приветственное сообщение с красивым форматированием
        await message.answer(
            WELCOME_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu()
        )
        
        # Логируем действие
        logger.info(f"Пользователь {message.from_user.id} ({message.from_user.username}) запустил бота")
        
    except TelegramAPIError as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        await message.answer("❌ Произошла ошибка. Пожалуйста, попробуйте позже.")


@dp.callback_query(F.data == "buy_pass")
async def buy_pass(callback: CallbackQuery):
    """Обработчик покупки проходки"""
    try:
        await callback.answer("🔄 Открываю страницу оплаты...")
        
        await callback.message.edit_text(
            BUY_PASS_TEXT.format(link=DONATION_LINK),
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_button(),
            disable_web_page_preview=False
        )
        
        logger.info(f"Пользователь {callback.from_user.id} перешел к покупке проходки")
        
    except TelegramAPIError as e:
        logger.error(f"Ошибка при обработке покупки: {e}")
        await callback.answer("❌ Произошла ошибка", show_alert=True)


@dp.callback_query(F.data == "submit_request")
async def submit_request(callback: CallbackQuery):
    """Обработчик подачи заявки"""
    try:
        await callback.answer("📝 Открываю форму заявки...")
        
        await callback.message.edit_text(
            REQUEST_TEXT.format_link=FORM_LINK,
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_button(),
            disable_web_page_preview=False
        )
        
        logger.info(f"Пользователь {callback.from_user.id} перешел к подаче заявки")
        
    except TelegramAPIError as e:
        logger.error(f"Ошибка при обработке заявки: {e}")
        await callback.answer("❌ Произошла ошибка", show_alert=True)


@dp.callback_query(F.data == "help")
async def show_help(callback: CallbackQuery):
    """Обработчик помощи"""
    help_text = """
❓ <b>Помощь и информация</b> ❓

<b>Как купить проходку?</b>
1. Нажмите кнопку "🎟 Купить проходку"
2. Перейдите по ссылке для оплаты
3. После оплаты вы получите доступ

<b>Как подать заявку?</b>
1. Нажмите кнопку "📝 Подать заявку"
2. Заполните форму
3. Дождитесь ответа менеджера

<b>Другие вопросы?</b>
Свяжитесь с нами: @support_username
"""
    
    await callback.answer()
    await callback.message.edit_text(
        help_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_button()
    )


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """Возврат в главное меню"""
    try:
        await callback.answer("🏠 Возврат в главное меню")
        
        await callback.message.edit_text(
            WELCOME_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu()
        )
        
    except TelegramAPIError as e:
        logger.error(f"Ошибка при возврате в меню: {e}")
        # Если не удалось отредактировать, отправляем новое сообщение
        await callback.message.answer(
            WELCOME_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu()
        )


# ========== ОБРАБОТКА ОШИБОК ==========
@dp.errors()
async def error_handler(update, exception):
    """Глобальный обработчик ошибок"""
    logger.error(f"Произошла ошибка: {exception}", exc_info=True)
    
    # Уведомляем пользователя об ошибке, если возможно
    if isinstance(update, CallbackQuery):
        await update.answer("❌ Произошла техническая ошибка", show_alert=True)
    elif isinstance(update, Message):
        await update.answer("❌ Произошла техническая ошибка. Попробуйте позже.")


# ========== ЗАПУСК ==========
async def on_startup():
    """Действия при запуске бота"""
    logger.info("🤖 Бот запускается...")
    logger.info(f"✅ Бот успешно запущен! (токен: {BOT_TOKEN[:10]}...)")


async def on_shutdown():
    """Действия при остановке бота"""
    logger.info("🛑 Бот останавливается...")
    await bot.session.close()
    logger.info("✅ Бот успешно остановлен")


async def main():
    """Главная функция запуска"""
    try:
        # Запускаем бота
        await on_startup()
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        await on_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
