# /usr/local/bin/python3 "/Users/chef_hank/Desktop/проектная практика/src/main_modified.py"

import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

from handlers import (
    start_command,
    help_command,
    add_book_start,
    add_book_title,
    add_book_author,
    add_book_year,
    add_book_rating,
    add_book_review,
    add_book_confirm,
    cancel_command,
    my_books_command,
    search_start,
    search_query,
    stats_command,
    button_handler,
    book_details,
)
from states import (
    TITLE, AUTHOR, YEAR, RATING, REVIEW, CONFIRM,
    SEARCH_QUERY
)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_bot():
    """Асинхронная функция для запуска бота."""
    
    # Здесь напрямую указываем токен бота
    TOKEN = "7567363652:AAGGhpwcJicTMOqj5u7W2GfURnfL7uZZQQw"
    
    if not TOKEN:
        logger.error("Не задан токен бота!")
        return

    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Обработчик команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("mybooks", my_books_command))

    # Обработчик для добавления книги
    add_book_conv = ConversationHandler(
        entry_points=[CommandHandler("addbook", add_book_start)],
        states={
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_book_title)],
            AUTHOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_book_author)],
            YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_book_year)],
            RATING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_book_rating),
                CallbackQueryHandler(add_book_rating, pattern="^rating_[1-5]$")
            ],
            REVIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_book_review)],
            CONFIRM: [
                CallbackQueryHandler(add_book_confirm, pattern="^(confirm|cancel)$")
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )
    application.add_handler(add_book_conv)

    # Обработчик для поиска книг
    search_conv = ConversationHandler(
        entry_points=[CommandHandler("search", search_start)],
        states={
            SEARCH_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_query)],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )
    application.add_handler(search_conv)

    # Обработчик кнопок
    application.add_handler(CallbackQueryHandler(book_details, pattern="^book_details_"))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запуск бота с отключением вебхуков и использованием поллинга
    await application.initialize()
    await application.start()
    await application.updater.start_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )
    
    # Логирование успешного запуска
    logger.info("Бот успешно запущен")
    
    # Ждем, пока бот не будет остановлен (Ctrl+C)
    await application.updater.stop()
    await application.stop()

def main():
    """Запуск бота."""
    import asyncio
    asyncio.run(start_bot())

if __name__ == "__main__":
    main()