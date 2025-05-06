# Telegram Psychologist Bot

Telegram бот, способный вести психологические сессии с использованием ChatGPT API.

## Возможности

- 1-часовые психологические сессии
- Сохранение истории диалогов
- Автоматическое завершение сессии по истечении времени
- Возможность досрочного завершения сессии
- Восстановление контекста при повторных обращениях

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd psychobot
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории проекта:
```env
TELEGRAM_API_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql+asyncpg://user:password@localhost/psychobot
```

5. Создайте базу данных PostgreSQL:
```sql
CREATE DATABASE psychobot;
```

## Запуск

1. Активируйте виртуальное окружение (если еще не активировано):
```bash
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

2. Запустите бота:
```bash
python main.py
```

## Использование

1. Найдите бота в Telegram по его username
2. Отправьте команду `/start` для начала сессии
3. Общайтесь с ботом в течение часа
4. Используйте команду `/end` для досрочного завершения сессии

## Структура проекта

```
psychobot/
│
├── main.py                     # Точка входа
├── settings.py                # Конфигурация проекта
├── requirements.txt
│
├── bot/                       # Логика Telegram-бота
│   ├── handlers.py            # Обработка сообщений и команд
│   ├── dispatcher.py          # Подключение хендлеров
│   └── session_manager.py     # Логика работы сессий и времени
│
├── core/                      # Бизнес-логика
│   ├── chatgpt_client.py      # Запросы к ChatGPT API
│   └── dialogue_engine.py     # Логика поведения "психолога"
│
├── db/                        # Работа с БД
│   ├── models.py              # SQLAlchemy модели
│   ├── database.py            # Подключение и инициализация
│   └── crud.py                # CRUD-операции
│
└── utils/                     # Утилиты и вспомогательные функции
    └── timers.py              # Таймеры и отложенные действия
```

## Лицензия

MIT 