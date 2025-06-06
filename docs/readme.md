# Проектная (учебная) практика

## Участники

| ФИО                         | Учебная группа | Код направления подготовки | Профиль образовательной программы                          |
|----------------------------|----------------|-----------------------------|-------------------------------------------------------------|
| Калашян Хэнк Араевич       | 241-337        | 09.03.02                    | Креативные Инд. (Информационные системы и технологии)       |
| Хуторная Виктория Алексеевна | 241-336        | 09.03.02                    | Креативные Инд. (Информационные системы и технологии)       |

---

## Базовая часть задания

### Цели проекта
1. Создание единой цифровой платформы для курсов ДПО Московского Политеха
2. Систематизация информации об образовательных программах
3. Упрощение процесса поиска и записи на курсы
4. Повышение доступности образовательных программ

### Функционал сайта
1. Навигация по разделам:
   - Главная страница с общей информацией
   - Страница "О проекте" с описанием целей и задач
   - Раздел "Участники" с информацией о команде
   - "Журнал" для отслеживания новостей и обновлений
   - "Ресурсы" с дополнительными материалами

2. Основные возможности:
   - Просмотр доступных курсов ДПО
   - Информация о программах обучения
   - Контактные данные
   - Навигация по образовательным программам
   - Интеграция с социальными сетями (Telegram)

### Использованные технологии

#### Frontend:
1. HTML5:
   - Семантическая верстка
   - Адаптивный дизайн
   - Современные теги и атрибуты

2. CSS3:
   - Flexbox для компоновки элементов
   - CSS-переменные для управления стилями
   - Анимации и переходы
   - Media queries для адаптивности
   - Градиенты и современные визуальные эффекты

3. Внешние библиотеки:
   - Font Awesome для иконок
   - Google Fonts (Roboto, Open Sans)

#### Дизайн:
- Фирменные цвета Мосполитеха (красный #e30611)
- Современный минималистичный стиль
- Адаптивный интерфейс
- Анимированные элементы для улучшения UX

### Особенности реализации
1. Производительность:
   - Оптимизированные изображения
   - Минимизированные CSS-файлы
   - Быстрая загрузка страниц

2. Безопасность:
   - Защита от XSS-атак
   - Безопасная передача данных
   - Валидация форм

3. Доступность:
   - Семантическая верстка
   - Адаптивный дизайн
   - Поддержка различных устройств
   - Кроссбраузерная совместимость

## Перспективы развития
1. Внедрение системы авторизации
2. Добавление личного кабинета
3. Интеграция с платежными системами
4. Разработка API для внешних сервисов
5. Внедрение системы поиска и фильтрации курсов

## Вариативная часть задания

**Разработка телеграм-бота на Python**

В рамках вариативной части проектной работы планируется реализовать многофункционального телеграм-бота на языке программирования Python с использованием библиотеки `telebot`. Бот будет включать следующие функции:
- Добавить книгу в список прочитанных
- Показать список прочитанных книг
- Ставить оценки книгам
- Оставлять отзывы на книги

Проект будет реализован с соблюдением принципов модульного программирования:
- Отдельный модуль для работы с Telegram API
- Модуль обработки пользовательских команд
- Модуль хранения данных пользователей

**Цели проекта:**
1. Освоить работу с Telegram Bot API
2. Изучить библиотеку `telebot` для создания ботов
3. Реализовать систему обработки пользовательских команд
4. Организовать хранение данных пользователей

**Используемые технологии:**
- Язык программирования Python 3.10+
- Библиотека `telebot` (версия 4.27.0)
- База данных in-memory для хранения пользовательских данных
- Библиотека `python-dotenv` для управления конфигурацией

**Планируемый функционал:**
1. Система команд:
   - `/start` - Начать работу с ботом
   - `/help` - список доступных команд
   - `/addbook` - Добавить книгу в список прочитанных
   - `/mybooks` - Показать список прочитанных книг
   - `/cancel` - Отменить текущее действие

2. Интерактивные клавиатуры для удобного взаимодействия

3. Система кэширования часто запрашиваемых данных

4. Логирование действий бота

---

## Ответственный по проектной (учебной) практике

*Меньшикова Наталия Павловна, ИиИТ.*

---

## Проектная деятельность

Проектная (учебная) практика проводилась в связке с выполнением проекта  
**«Автоматизация внутренних бизнес-процессов университета»**  
по дисциплине **«Проектная деятельность»**.

Куратор по проектной деятельности: **Чернова Вера Михайловна**.

---

## Период проведения

**С 03 февраля 2025 г. по 24 мая 2025 г.**

---

## Дополнительные материалы

Для реализации проекта будут использоваться следующие обучающие материалы:
1. Официальная документация telebot: https://pytba.readthedocs.io/ru/latest/index.html
2. Руководство по созданию Telegram ботов: https://core.telegram.org/bots
3. Примеры интеграции с внешними API
4. Материалы по работе с базами данных в Python

Результатом работы станет полностью функциональный телеграм-бот, размещенный на облачном сервере, с возможностью дальнейшего расширения функционала.