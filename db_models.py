import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import String, Integer, Float, Date, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

load_dotenv()

DB_URL = os.getenv("DB_URL", "sqlite:///weather_lab.db")
engine = create_engine(DB_URL, echo=False)

#=== Base class for models ===
class Base(DeclarativeBase):
    pass

#=== Weather forecast table ===
class WeatherForecast(Base):
    __tablename__ = "weather_forecast"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String, nullable=False)
    forecast_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    temp_min: Mapped[float] = mapped_column(Float, nullable=False)
    temp_max: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[int] = mapped_column(Integer, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

#=== Create tables if not exist ===
def init_db():
    Base.metadata.create_all(engine)

#=== Save daily forecast, skip duplicates ===
def save_forecast(city, days):
    saved = 0
    skipped = 0
    with Session(engine) as session:
        for d in days:
            exists = session.query(WeatherForecast).filter_by(
                city=city, forecast_date=d["date"]
            ).first()
            if exists:
                skipped += 1
                continue
            row = WeatherForecast(
                city=city,
                forecast_date=datetime.strptime(d["date"], "%Y-%m-%d").date(),
                temp_min=d["temp_min"],
                temp_max=d["temp_max"],
                humidity=d["humidity"],
                wind_speed=d["wind_speed"],
                description=d["description"],
            )
            session.add(row)
            saved += 1
        session.commit()
    return saved, skipped
#if __name__ == "__main__":
    init_db()
    from geolocator import get_location
    from weather import fetch_forecast, aggregate_by_day
    loc = get_location()
    pts = fetch_forecast(loc["lat"], loc["lon"])
    days = aggregate_by_day(pts)
    n = save_forecast(loc["city"], days)
    print(f"Сохранено записей: {n}")
