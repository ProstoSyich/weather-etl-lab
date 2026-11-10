import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from db_models import WeatherForecast, engine

load_dotenv()


#=== Get output path from env ===
def get_output_path():
    path = os.getenv("OUTPUT_FILE")
    if not path:
        print("OUTPUT_FILE is not set")
        return None
    return path


#=== Load records from db ===b
def load_records(city):
    with Session(engine) as session:
        rows = (
            session.query(WeatherForecast)
            .filter_by(city=city)
            .order_by(WeatherForecast.forecast_date)
            .all()
        )
    return rows


#=== Build markdown lines ===
def build_markdown(city, rows):
    first = rows[0].forecast_date
    last = rows[-1].forecast_date

    lines = []
    lines.append("# Прогноз погоды")
    lines.append("")
    lines.append(f"Локация: {city}")
    lines.append(f"Период: {first} - {last}")
    lines.append("")

    lines.append("| Дата | Мин. темп. | Макс. темп. | Описание | Влажность | Ветер |")
    lines.append("|------|-----------|-------------|----------|-----------|-------|")

    for r in rows:
        lines.append(
            f"| {r.forecast_date} | {r.temp_min} | {r.temp_max} | "
            f"{r.description} | {r.humidity} | {r.wind_speed} |"
        )

    lines.append("")
    lines.append(f"Сформировано: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return "\n".join(lines)


#=== Main export ===
def to_markdown(city):
    rows = load_records(city)

    if not rows:
        print("Bd is empty")
        return None

    content = build_markdown(city, rows)

    path = get_output_path()
    if path is None:
        return None

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
        print(f"Writing error: {e}")
        return None

    print(f"Markdown saved: {path}")
    return path
#if __name__ == "__main__":
    p = to_markdown("London")
    print(p)
