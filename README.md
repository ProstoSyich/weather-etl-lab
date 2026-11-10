# Weather ETL Lab

Лабораторная работа: ETL-контур на Python для сбора прогноза погоды.

## Описание

Программа автоматически определяет местоположение по IP, запрашивает прогноз погоды на 4 дня (сегодня + 3) из OpenWeatherMap, агрегирует 3-часовые данные в дневные сводки, сохраняет результат в базу данных SQLite и выгружает в файл формата Markdown.

## Используемые технологии

- Python 3
- requests (HTTP-запросы к API)
- SQLAlchemy (ORM для работы с базой данных)
- SQLite (встроенная база данных)
- python-dotenv (загрузка переменных окружения из файла .env)

## Установка и настройка

1. Клонировать репозиторий и перейти в папку:
   git clone https://github.com/ProstoSyich/weather-etl-lab.git
   cd weather-etl-lab

2. Создать и активировать виртуальное окружение:
   python3 -m venv .venv
   source .venv/bin/activate

3. Установить зависимости:
   pip install -r requirements.txt

4. Создать файл .env по шаблону:
   cp .env.example .env

5. Открыть .env и вписать свой ключ OpenWeatherMap в переменную WEATHER_API_KEY. (Получить бесплатный ключ можно на openweathermap.org).

## Запуск

python3 main.py

Программа выполнит следующие шаги:
1. Инициализирует базу данных.
2. Определит город и координаты по IP (или возьмет город из GEO_API_FALLBACK_CITY).
3. Запросит прогноз у OpenWeatherMap.
4. Сгруппирует данные по дням.
5. Сохранит записи в базу (пропуская дубликаты).
6. Сгенерирует файл weather_report.md.

## Структура проекта

- geolocator.py — определение координат и города через IP.
- weather.py — запрос к API погоды и агрегация данных по дням.
- db_models.py — модель таблицы и функции сохранения/загрузки из SQLite.
- exporter.py — формирование Markdown-отчета из базы данных.
- main.py — главный скрипт, связывающий все модули.
- .env.example — шаблон конфигурации.
- requirements.txt — список зависимостей.

## Пример вывода в консоль

City: London
Coords: 51.5081, -0.1278

Days: 4
Period: 2026-11-10 - 2026-11-13

Saved: 4
Skipped: 0

Markdown saved: weather_report.md
File: weather_report.md
