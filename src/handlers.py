import re
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from book_manager import BookManager
from keyboards import (
    get_rating_keyboard, 
    get_confirm_keyboard, 
    get_books_keyboard,
    get_back_to_list_keyboard
)
from states import TITLE, AUTHOR, YEAR, RATING, REVIEW, CONFIRM, SEARCH_QUERY

# Создание менеджера книг
book_manager = BookManager()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Привет, {user_first_name}! 📚\n\n"
        "Я бот для учета прочитанных книг. С моей помощью ты можешь:\n"
        "• Добавлять прочитанные книги\n"
        "• Ставить им оценки и писать отзывы\n"
        "• Просматривать список прочитанных книг\n"
        "• Искать информацию по своим книгам\n"
        "• Получать статистику о своих чтениях\n\n"
        "Используй команду /help чтобы увидеть список доступных команд."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help."""
    await update.message.reply_text(
        "📋 Список доступных команд:\n\n"
        "/addbook - Добавить новую прочитанную книгу\n"
        "/mybooks - Просмотреть список прочитанных книг\n"
        "/search - Поиск среди прочитанных книг\n"
        "/stats - Посмотреть статистику чтения\n"
        "/cancel - Отменить текущую операцию\n"
        "/help - Показать эту справку"
    )

async def add_book_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало диалога для добавления книги."""
    # Создаем словарь для хранения данных о книге
    context.user_data["book"] = {}
    
    await update.message.reply_text(
        "Давайте добавим новую прочитанную книгу! 📖\n\n"
        "Какое название у книги?"
    )
    return TITLE

async def add_book_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода названия книги."""
    context.user_data["book"]["title"] = update.message.text
    
    await update.message.reply_text(
        f"Название: {update.message.text}\n\n"
        "Теперь укажите автора книги:"
    )
    return AUTHOR

async def add_book_author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода автора книги."""
    context.user_data["book"]["author"] = update.message.text
    
    await update.message.reply_text(
        f"Автор: {update.message.text}\n\n"
        "Введите год издания книги (или 0, если не знаете):"
    )
    return YEAR

async def add_book_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода года издания книги."""
    text = update.message.text
    
    # Проверка валидности введенного года
    if not text.isdigit():
        await update.message.reply_text(
            "Пожалуйста, введите год в числовом формате (например, 2021)."
        )
        return YEAR
    
    year = int(text)
    if year < 0 or (year > 2100 and year != 0):
        await update.message.reply_text(
            "Укажите корректный год издания или 0, если не знаете."
        )
        return YEAR
    
    context.user_data["book"]["year"] = year
    
    # Отправка клавиатуры для выбора оценки
    await update.message.reply_text(
        f"Год издания: {year}\n\n"
        "Какую оценку вы бы поставили этой книге (от 1 до 5):",
        reply_markup=get_rating_keyboard()
    )
    return RATING

async def add_book_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода оценки книги."""
    # Проверяем, получена ли оценка через кнопку
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        
        # Извлекаем оценку из callback_data
        rating_data = query.data
        rating = int(rating_data.split("_")[1])
        
        # Обновляем сообщение
        await query.edit_message_text(f"Вы поставили оценку: {'⭐' * rating}")
    else:
        # Если пользователь ввел оценку текстом
        text = update.message.text
        
        # Проверка валидности оценки
        if not text.isdigit() or int(text) < 1 or int(text) > 5:
            await update.message.reply_text(
                "Пожалуйста, укажите оценку от 1 до 5.", 
                reply_markup=get_rating_keyboard()
            )
            return RATING
        
        rating = int(text)
        await update.message.reply_text(f"Вы поставили оценку: {'⭐' * rating}")
    
    context.user_data["book"]["rating"] = rating
    
    # Переходим к отзыву
    if update.callback_query:
        await update.callback_query.message.reply_text(
            "Напишите краткий отзыв о книге (или отправьте '-', если не хотите оставлять отзыв):"
        )
    else:
        await update.message.reply_text(
            "Напишите краткий отзыв о книге (или отправьте '-', если не хотите оставлять отзыв):"
        )
    return REVIEW

async def add_book_review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка ввода отзыва о книге."""
    review = update.message.text
    
    # Если пользователь не хочет оставлять отзыв
    if review == "-":
        review = ""
    
    context.user_data["book"]["review"] = review
    
    # Формируем сообщение для подтверждения
    book = context.user_data["book"]
    
    confirmation_text = (
        "📚 Проверьте информацию о книге:\n\n"
        f"Название: {book['title']}\n"
        f"Автор: {book['author']}\n"
        f"Год издания: {book['year']}\n"
        f"Оценка: {'⭐' * book['rating']}\n"
    )
    
    if review:
        confirmation_text += f"Отзыв: {review}\n\n"
    else:
        confirmation_text += "Отзыв: отсутствует\n\n"
    
    confirmation_text += "Всё верно?"
    
    await update.message.reply_text(
        confirmation_text,
        reply_markup=get_confirm_keyboard()
    )
    return CONFIRM

async def add_book_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка подтверждения добавления книги."""
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    
    if choice == "confirm":
        book = context.user_data["book"]
        user_id = update.effective_user.id
        
        # Добавление книги в хранилище
        book_manager.add_book(
            user_id,
            book["title"],
            book["author"],
            book["year"],
            book["rating"],
            book["review"]
        )
        
        await query.edit_message_text(
            "✅ Книга успешно добавлена в вашу библиотеку!\n\n"
            "Используйте /addbook, чтобы добавить ещё одну книгу, или "
            "/mybooks, чтобы просмотреть свой список прочитанных книг."
        )
    else:
        await query.edit_message_text(
            "❌ Добавление книги отменено.\n\n"
            "Используйте /addbook, чтобы начать заново."
        )
    
    # Очищаем данные
    context.user_data.clear()
    return ConversationHandler.END

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена текущей операции."""
    # Очищаем данные
    context.user_data.clear()
    
    await update.message.reply_text(
        "❌ Операция отменена.\n\n"
        "Используйте /help, чтобы увидеть список доступных команд."
    )
    return ConversationHandler.END

async def my_books_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отображение списка прочитанных книг."""
    user_id = update.effective_user.id
    books = book_manager.get_user_books(user_id)
    
    if not books:
        await update.message.reply_text(
            "📚 Ваша библиотека пуста.\n\n"
            "Используйте команду /addbook, чтобы добавить свою первую книгу!"
        )
        return
    
    # Сохраняем список книг в контекст для пагинации
    context.user_data["books_list"] = books
    context.user_data["current_page"] = 0
    
    await update.message.reply_text(
        f"📚 Ваша библиотека ({len(books)} книг):",
        reply_markup=get_books_keyboard(books, page=0)
    )

async def search_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало поиска книг."""
    await update.message.reply_text(
        "🔍 Введите название книги или имя автора для поиска:"
    )
    return SEARCH_QUERY

async def search_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка поискового запроса."""
    user_id = update.effective_user.id
    query = update.message.text
    
    # Поиск книг
    found_books = book_manager.search_books(user_id, query)
    
    if not found_books:
        await update.message.reply_text(
            f"🔍 По запросу '{query}' ничего не найдено.\n\n"
            "Попробуйте изменить запрос или используйте /mybooks, "
            "чтобы просмотреть все свои книги."
        )
    else:
        # Сохраняем список книг в контекст для пагинации
        context.user_data["books_list"] = found_books
        context.user_data["current_page"] = 0
        
        await update.message.reply_text(
            f"🔍 Результаты поиска по запросу '{query}' ({len(found_books)} книг):",
            reply_markup=get_books_keyboard(found_books, page=0)
        )
    
    return ConversationHandler.END

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отображение статистики чтения."""
    user_id = update.effective_user.id
    stats = book_manager.calculate_stats(user_id)
    
    if stats["total_books"] == 0:
        await update.message.reply_text(
            "📊 У вас пока нет прочитанных книг для составления статистики.\n\n"
            "Используйте команду /addbook, чтобы добавить свою первую книгу!"
        )
        return
    
    # Формирование сообщения со статистикой
    stats_message = (
        "📊 Ваша статистика чтения:\n\n"
        f"📚 Всего прочитано книг: {stats['total_books']}\n"
        f"⭐ Средняя оценка: {stats['average_rating']}\n\n"
    )
    
    # Добавление топ книг
    if stats["top_rated_books"]:
        stats_message += "🏆 Книги с наивысшей оценкой:\n"
        for i, book in enumerate(stats["top_rated_books"], 1):
            stats_message += f"{i}. {book['title']} - {'⭐' * book['rating']}\n"
        stats_message += "\n"
    
    # Добавление последних прочитанных книг
    if stats["recent_books"]:
        stats_message += "🕒 Последние добавленные книги:\n"
        for i, book in enumerate(stats["recent_books"], 1):
            stats_message += f"{i}. {book['title']} - {book['author']}\n"
    
    await update.message.reply_text(stats_message)

async def book_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отображение детальной информации о книге."""
    query = update.callback_query
    await query.answer()
    
    # Извлечение ID книги из callback_data
    book_id = int(query.data.split("_")[2])
    user_id = update.effective_user.id
    
    # Получение информации о книге
    book = book_manager.get_book_by_id(user_id, book_id)
    
    if not book:
        await query.edit_message_text("❌ Книга не найдена.")
        return
    
    # Формирование сообщения с деталями
    details_message = (
        f"📖 {book['title']}\n\n"
        f"👤 Автор: {book['author']}\n"
        f"📅 Год издания: {book['year']}\n"
        f"⭐ Оценка: {'⭐' * book['rating']}\n"
    )
    
    if book['review']:
        details_message += f"💬 Ваш отзыв: {book['review']}\n"
    
    details_message += f"\n📆 Добавлено: {book['date_added']}"
    
    await query.edit_message_text(
        details_message,
        reply_markup=get_back_to_list_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # Обработка кнопок пагинации
    if data.startswith("page_"):
        page = int(data.split("_")[1])
        context.user_data["current_page"] = page
        
        books = context.user_data.get("books_list", [])
        
        await query.edit_message_text(
            f"📚 Ваши книги:",
            reply_markup=get_books_keyboard(books, page=page)
        )
    
    # Кнопка возврата к списку
    elif data == "back_to_list":
        books = context.user_data.get("books_list", [])
        page = context.user_data.get("current_page", 0)
        
        await query.edit_message_text(
            f"📚 Ваши книги:",
            reply_markup=get_books_keyboard(books, page=page)
        )
    
    # Заглушка для кнопки с номером страницы
    elif data == "noop":
        pass
