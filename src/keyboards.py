from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_rating_keyboard():
    """Создает клавиатуру для оценки книги.
    
    Returns:
        InlineKeyboardMarkup: клавиатура с кнопками оценок 1-5
    """
    keyboard = [
        [
            InlineKeyboardButton("⭐", callback_data="rating_1"),
            InlineKeyboardButton("⭐⭐", callback_data="rating_2"),
            InlineKeyboardButton("⭐⭐⭐", callback_data="rating_3"),
            InlineKeyboardButton("⭐⭐⭐⭐", callback_data="rating_4"),
            InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="rating_5"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirm_keyboard():
    """Создает клавиатуру для подтверждения добавления книги.
    
    Returns:
        InlineKeyboardMarkup: клавиатура с кнопками подтверждения и отмены
    """
    keyboard = [
        [
            InlineKeyboardButton("✅ Подтвердить", callback_data="confirm"),
            InlineKeyboardButton("❌ Отмена", callback_data="cancel"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_books_keyboard(books, page=0, page_size=5):
    """Создает клавиатуру со списком книг и пагинацией.
    
    Args:
        books: список книг
        page: текущая страница
        page_size: количество книг на странице
        
    Returns:
        InlineKeyboardMarkup: клавиатура со списком книг
    """
    # Расчет пагинации
    total_books = len(books)
    total_pages = (total_books + page_size - 1) // page_size
    
    # Пустая клавиатура, если книг нет
    if not books:
        return InlineKeyboardMarkup([])
    
    # Получение книг на текущей странице
    start_idx = page * page_size
    end_idx = min(start_idx + page_size, total_books)
    current_books = books[start_idx:end_idx]
    
    # Создание кнопок для каждой книги
    keyboard = []
    for book in current_books:
        rating_stars = "⭐" * book["rating"]
        button_text = f"{book['title']} - {rating_stars}"
        callback_data = f"book_details_{book['id']}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    # Добавление кнопок навигации, если есть несколько страниц
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"page_{page-1}"))
        
        nav_buttons.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data="noop"))
        
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"page_{page+1}"))
        
        keyboard.append(nav_buttons)
    
    return InlineKeyboardMarkup(keyboard)

def get_back_to_list_keyboard():
    """Создает клавиатуру для возврата к списку книг.
    
    Returns:
        InlineKeyboardMarkup: клавиатура с кнопкой возврата
    """
    keyboard = [[InlineKeyboardButton("◀️ Назад к списку", callback_data="back_to_list")]]
    return InlineKeyboardMarkup(keyboard)
