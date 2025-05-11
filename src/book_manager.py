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
