import os
import requests
from collections import defaultdict
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
#=== Fetch 3-hour forecast from OpenWeatherMap ===
def fetch_forecast(city, lat, lon):
    api_key = os.getenv("WEATHER_API_KEY")
    base_url = os.getenv("WEATHER_API_BASE_URL")

    params = {
        "appid": api_key,
        "units": "metric",
        "lang": "ru",
    }

    # Fallback
    if lat is not None and lon is not None:
        params["lat"] = lat
        params["lon"] = lon
    else:
        params["q"] = city

    try:
        response = requests.get(base_url, params=params, timeout =10)
        if response.status_code == 401:
            print("Неверный API ключ")
            return None
        if response.status_code == 404:
            print("Город не найден")
            return None
        if response.status_code == 429:
            print("Превышен лимит запросов")
            return None
        if response.status_code != 200:
            print(f"Ошибка API: {response.status_code}")
            return None
        data = response.json()
        return data["list"]
    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
        return None
#=== Aggregate 3-hour points into daily summaries ===
def aggregate_by_day(points, city):
    days = defaultdict(list)
    for p in points:
        date_str = p["dt_txt"].split(" ")[0]
        days[date_str].append(p)

    result = []
    for date_str in sorted(days.keys())[:4]:
        day_points = days[date_str]
        temps_min = [p["main"]["temp_min"] for p in day_points]
        temps_max = [p["main"]["temp_max"] for p in day_points]
        humidities = [p["main"]["humidity"] for p in day_points]
        winds = [p["wind"]["speed"] for p in day_points]

        desc = day_points[0]["weather"][0]["description"]
        for p in day_points:
            if "12:00:00" in p["dt_txt"]:
                desc = p["weather"][0]["description"]
                break

        result.append({
            "city": city,
            "date": date_str,
            "temp_min": min(temps_min),
            "temp_max": max(temps_max),
            "humidity": round(sum(humidities) / len(humidities)),
            "wind_speed": max(winds),
            "description": desc,
        })
    return result

#=== Wrapper: fetch + aggregate ===
def get_daily(city, lat, lon):
    points = fetch_forecast(city, lat, lon)
    if points is None:
        print("OpenWeatherMap forecast error")
        return None

    daily = aggregate_by_day(points, city)
    if len(daily) == 0:
        print("Aggregation error: no days")
        return None
    return daily

#if __name__ == "__main__":
    from geolocator import get_location
    loc = get_location()
    print(loc)
    pts = fetch_forecast(loc["lat"], loc["lon"])
    if pts is None:
        print("Прогноз не получен, дальше не идём")
    else:
        days = aggregate_by_day(pts)
        for d in days:
            print(d)
