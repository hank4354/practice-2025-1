import os
import json
import telebot
from telebot import types

# Создаем экземпляр бота
bot = telebot.TeleBot("8014461297:AAH4iKyUIzLv97LQpdBDPidDBjH-z9M_U4E")

# Путь к файлу данных
data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "users.json")
os.makedirs(os.path.dirname(data_file), exist_ok=True)

# Словарь для хранения состояний пользователей
user_states = {}
user_data = {}

# Константы состояний
ADD_BOOK_TITLE = 1
ADD_BOOK_AUTHOR = 2
ADD_BOOK_YEAR = 3
ADD_BOOK_RATING = 4
ADD_BOOK_REVIEW = 5

# Загрузка данных
def load_data():
    try:
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return {}

# Сохранение данных
def save_data(data):
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

# Получение книг пользователя
def get_user_books(user_id):
    data = load_data()
    user_id_str = str(user_id)
    if user_id_str not in data:
        data[user_id_str] = {"books": []}
        save_data(data)
    return data[user_id_str]["books"]

# Добавление книги
def add_book(user_id, title, author, year, rating, review):
    data = load_data()
    user_id_str = str(user_id)
    
    if user_id_str not in data:
        data[user_id_str] = {"books": []}
    
    book_id = len(data[user_id_str]["books"])
    
    book = {
        "id": book_id,
        "title": title,
        "author": author,
        "year": year,
        "rating": rating,
        "review": review
    }
    
    data[user_id_str]["books"].append(book)
    save_data(data)
    return True

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш бот для учета прочитанных книг.\n\nВы можете добавлять книги, которые прочитали, оценивать их и писать краткие отзывы. Для начала работы воспользуйтесь командами из меню или отправьте /help для получения справки.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = "Доступные команды:\n"
    help_text += "/start - Начать работу с ботом\n"
    help_text += "/help - Показать эту справку\n"
    help_text += "/addbook - Добавить книгу в список прочитанных\n"
    help_text += "/mybooks - Показать список прочитанных книг\n"
    help_text += "/cancel - Отменить текущее действие"
    bot.reply_to(message, help_text)

# Обработчик команды /cancel
@bot.message_handler(commands=['cancel'])
def cancel(message):
    user_id = message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    if user_id in user_data:
        del user_data[user_id]
    bot.reply_to(message, "Действие отменено.")

# Обработчик команды /addbook
@bot.message_handler(commands=['addbook'])
def add_book_start(message):
    user_id = message.from_user.id
    user_states[user_id] = ADD_BOOK_TITLE
    user_data[user_id] = {}
    bot.reply_to(message, "Введите название книги:")

# Обработчик команды /mybooks
@bot.message_handler(commands=['mybooks'])
def my_books(message):
    user_id = message.from_user.id
    books = get_user_books(user_id)
    
    if not books:
        bot.reply_to(message, "У вас пока нет добавленных книг.")
        return
    
    response = "Ваши книги:\n\n"
    for book in books:
        stars = "⭐" * book["rating"]
        response += f"📚 {book['title']} ({book['author']}, {book['year']}) - {stars}\n"
    
    bot.reply_to(message, response)

# Обработчик для всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    
    # Если пользователь не находится в процессе добавления книги
    if user_id not in user_states:
        bot.reply_to(message, "Я не понимаю эту команду. Отправьте /help для получения списка доступных команд.")
        return
    
    state = user_states[user_id]
    
    # Процесс добавления книги
    if state == ADD_BOOK_TITLE:
        user_data[user_id]['title'] = message.text
        user_states[user_id] = ADD_BOOK_AUTHOR
        bot.reply_to(message, "Введите автора книги:")
    
    elif state == ADD_BOOK_AUTHOR:
        user_data[user_id]['author'] = message.text
        user_states[user_id] = ADD_BOOK_YEAR
        bot.reply_to(message, "Введите год издания книги:")
    
    elif state == ADD_BOOK_YEAR:
        try:
            year = int(message.text)
            user_data[user_id]['year'] = year
            user_states[user_id] = ADD_BOOK_RATING
            
            # Создаем клавиатуру для оценки
            markup = types.InlineKeyboardMarkup(row_width=5)
            buttons = [types.InlineKeyboardButton(f"{i} ⭐", callback_data=f"rating_{i}") for i in range(1, 6)]
            markup.add(*buttons)
            
            bot.reply_to(message, "Оцените книгу от 1 до 5:", reply_markup=markup)
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите корректный год издания (число).")
    
    elif state == ADD_BOOK_RATING:
        try:
            rating = int(message.text)
            if 1 <= rating <= 5:
                user_data[user_id]['rating'] = rating
                user_states[user_id] = ADD_BOOK_REVIEW
                bot.reply_to(message, "Напишите краткий отзыв о книге:")
            else:
                bot.reply_to(message, "Пожалуйста, оцените книгу от 1 до 5.")
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите число от 1 до 5.")
    
    elif state == ADD_BOOK_REVIEW:
        user_data[user_id]['review'] = message.text
        
        # Добавляем книгу
        add_book(
            user_id,
            user_data[user_id]['title'],
            user_data[user_id]['author'],
            user_data[user_id]['year'],
            user_data[user_id]['rating'],
            user_data[user_id]['review']
        )
        
        del user_states[user_id]
        del user_data[user_id]
        
        bot.reply_to(message, "Книга успешно добавлена в ваш список!")

# Обработчик нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: call.data.startswith('rating_'))
def handle_rating_callback(call):
    user_id = call.from_user.id
    
    if user_id in user_states and user_states[user_id] == ADD_BOOK_RATING:
        rating = int(call.data.split('_')[1])
        user_data[user_id]['rating'] = rating
        user_states[user_id] = ADD_BOOK_REVIEW
        
        # Редактируем сообщение и убираем клавиатуру
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Ваша оценка: {rating} ⭐"
        )
        
        # Отправляем новое сообщение с запросом отзыва
        bot.send_message(call.message.chat.id, "Напишите краткий отзыв о книге:")

print("Запускаем бота...")
print("Бот запущен, нажмите Ctrl+C для остановки")

# Запускаем бота
bot.polling()