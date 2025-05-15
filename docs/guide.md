# Отчет по созданию телеграм-бота "Уже прочитанные книги"
# 1. Исследование предметной области
1.1. Изучение Telegram Bot API
Telegram Bot API предоставляет интерфейс для программного взаимодействия с платформой Telegram. Боты могут обрабатывать сообщения, команды и отвечать пользователям, выполняя различные функции.

1.2. Выбор инструментов разработки
После изучения вариантов был выбран стек технологий:

Язык программирования: Python 3.11
Библиотека для работы с Telegram API: pyTelegramBotAPI (telebot)
Управление конфигурацией: python-dotenv
Хранение данных: In-memory хранилище (для MVP)
1.3. Планирование функциональности
Был определен следующий набор функций:

Добавить книгу в список прочитанных
Показать список прочитанных книг
Ставить оценки книгам
Оставлять отзывы на книги
# 2. Техническое руководство по созданию Telegram-бота "Уже прочитанные книги"
# Шаг 1: Подготовка среды разработки
1.1. Создание виртуального окружения
# Создание виртуального окружения
python3 -m venv venv
#Активация виртуального окружения
#Для Windows:
#venv\Scripts\activate
#Для macOS/Linux:
#source venv/bin/activate
1.2. Установка необходимых библиотек
pip install pyTelegramBotAPI python-dotenv
# Шаг 2: Получение токена для Telegram-бота
Откройте Telegram и найдите бота @BotFather
Отправьте команду /newbot
Следуйте инструкциям BotFather:
Укажите отображаемое имя бота (например, "Уже прочитанные книги")
Укажите уникальное имя пользователя (например, "AlrProchitBook_bot")
BotFather вернет токен вида 123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
Сохраните этот токен в файле .env:
TELEGRAM_BOT_TOKEN=ваш_токен_здесь
Шаг 3: Создание базового модуля для хранения данных
Создайте файл book_manager.py для управления данными пользователей:

	import json
    import os
    from datetime import datetime

    class BookManager:
        """Класс для управления данными о книгах пользователей."""

    def __init__(self, data_file=None):
        """Инициализация менеджера книг.
    
    Args:
        data_file: путь к JSON файлу для хранения данных
    """
    # Если путь не указан, используем текущую директорию
    if data_file is None:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(current_dir, "data", "users.json")
    
    self.data_file = data_file
    self.users = self._load_data()
    
    # Создать директорию, если она не существует
    os.makedirs(os.path.dirname(data_file), exist_ok=True)

    def _load_data(self):
        """Загрузка данных из JSON файла.
        
        Returns:
            dict: словарь с данными пользователей
        """
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_data(self):
        """Сохранение данных в JSON файл."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    def get_user_books(self, user_id):
        """Получение списка книг пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            list: список книг пользователя
        """
        user_id = str(user_id)  # Convert to string for JSON compatibility
        if user_id not in self.users:
            return []
        return self.users[user_id].get("books", [])

    def add_book(self, user_id, title, author, year, rating, review):
        """Добавление книги в список пользователя.
        
        Args:
            user_id: ID пользователя
            title: название книги
            author: автор книги
            year: год издания
            rating: оценка (1-5)
            review: краткий отзыв о книге
            
        Returns:
            bool: True если книга успешно добавлена
        """
        user_id = str(user_id)  # Convert to string for JSON compatibility
        
        # Создание записи для нового пользователя
        if user_id not in self.users:
            self.users[user_id] = {"books": []}
        
        # Создание записи о книге
        book = {
            "id": len(self.users[user_id]["books"]) + 1,  # Простой идентификатор
            "title": title,
            "author": author,
            "year": year,
            "rating": rating,
            "review": review,
            "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Добавление книги и сохранение данных
        self.users[user_id]["books"].append(book)
        self._save_data()
        return True

    def search_books(self, user_id, query):
        """Поиск книги по названию или автору.
        
        Args:
            user_id: ID пользователя
            query: поисковый запрос
            
        Returns:
            list: список найденных книг
        """
        user_id = str(user_id)
        if user_id not in self.users:
            return []
        
        books = self.users[user_id].get("books", [])
        query = query.lower()
        
        return [
            book for book in books 
            if query in book["title"].lower() or query in book["author"].lower()
        ]

    def get_book_by_id(self, user_id, book_id):
        """Получение книги по её идентификатору.
        
        Args:
            user_id: ID пользователя
            book_id: ID книги
            
        Returns:
            dict или None: информация о книге или None если книга не найдена
        """
        user_id = str(user_id)
        if user_id not in self.users:
            return None
        
        books = self.users[user_id].get("books", [])
        for book in books:
            if book["id"] == int(book_id):
                return book
        return None
        
    def calculate_stats(self, user_id):
        """Расчёт статистики пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            dict: словарь со статистикой
        """
        user_id = str(user_id)
        if user_id not in self.users or not self.users[user_id].get("books"):
            return {
                "total_books": 0,
                "average_rating": 0,
                "top_rated_books": [],
                "recent_books": []
            }
        
        books = self.users[user_id].get("books", [])
        
        # Расчет средней оценки
        total_ratings = sum(book["rating"] for book in books)
        avg_rating = total_ratings / len(books) if books else 0
        
        # Топ 3 книги по оценке
        top_rated_books = sorted(books, key=lambda x: x["rating"], reverse=True)[:3]
        
        # Последние 3 добавленные книги
        recent_books = sorted(books, key=lambda x: x["date_added"], reverse=True)[:3]
        
        return {
            "total_books": len(books),
            "average_rating": round(avg_rating, 1),
            "top_rated_books": top_rated_books,
            "recent_books": recent_books
        }

# Шаг 4: Создание основного файла бота
Создайте файл main.py с основной логикой бота:
```python
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
```
# Шаг 5: Создание примера конфигурационного файла
Создайте файл .env.example с примером настроек:

#Пример файла .env
#Скопируйте этот файл в .env и заполните значения
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
Шаг 6: Запуск бота
Убедитесь, что виртуальное окружение активировано и файл .env содержит правильный токен

python main.py
# 3. Объяснение работы бота
3.1. Обработка команд
В боте реализованы следующие обработчики команд:

   - `/start` - Начать работу с ботом
   - `/help` - список доступных команд
   - `/addbook` - Добавить книгу в список прочитанных
   - `/mybooks` - Показать список прочитанных книг
   - `/cancel` - Отменить текущее действие
3.2. Процесс игры
Пользователь вызывает команду `/addbook`
Бот просит ввести название книги
После ввода названия, бот просит ввести автора книги
После год издания книги
Далее оценить книгу от 1 до 5
После оценки оставить отзыв
Книга успешно добавлена в ваш список!
По команде `/mybooks` можете увидеть список введенных вами книг
3.3. Хранение данных
Данные пользователей (ID и Книги) хранятся в памяти программы в формате словаря:

```python
{
  "1275950804": {
    "books": [
      {
        "id": 0,
        "title": "мяу",
        "author": "гав",
        "year": 1990,
        "rating": 3,
        "review": "му"
      },
      {
        "id": 1,
        "title": "книга",
        "author": "автор",
        "year": 1234,
        "rating": 5,
        "review": "класс"
      }
    ]
  },
}
```
Это простой подход для MVP. 

# 4. Возможные улучшения
4.1. Улучшение хранения данных
Реализовать постоянное хранение данных с использованием базы данных (SQLite, PostgreSQL) для сохранения информации между перезапусками бота.


4.2. Улучшение пользовательского интерфейса
Более красочные и информативные сообщения

# 5. Выводы
В рамках проекта был успешно создан интерактивный телеграм-бот "Уже прочитанные книги" с простым и понятным интерфейсом, который позволяет пользователям иметь под рукой информацию о прочитанных книгах, чтобы потом советовать их другим.

Созданное решение демонстрирует базовые возможности Telegram Bot API и библиотеки pyTelegramBotAPI. Проект может быть использован как основа для более сложных ботов или как учебный пример для изучения разработки телеграм-ботов.