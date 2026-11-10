# Weather ETL Lab

Программа для получения прогноза погоды на 4 дня. Определяет местоположение по IP, запрашивает данные у OpenWeatherMap, агрегирует их по дням, сохраняет в базу данных SQLite и выгружает отчет в формате Markdown.

## Стек технологий

- Python 3
- `requests` — HTTP-запросы к API
- `SQLAlchemy` — ORM для работы с SQLite
- `python-dotenv` — загрузка переменных окружения
- SQLite — встроенная база данных

## Установка и настройка

1. Клонируйте репозиторий и перейдите в папку:
   ```bash
   git clone https://github.com/ProstoSyich/weather-etl-lab.git
   cd weather-etl-lab
