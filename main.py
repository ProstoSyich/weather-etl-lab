from geolocator import get_location
from weather import get_daily
from db_models import init_db, save_forecast
from exporter import to_markdown


#Main flow
def main():
    #=== DB Init ===
    try:
        init_db()
    except Exception as e:
        print(f"Error DB init: {e}")
        return 1

    #=== Get Location ===
    try:
        loc = get_location()
    except Exception as e:
        print(f"Error getting location: {e}")
        return 2

    city = loc["city"]
    lat = loc["lat"]
    lon = loc["lon"]

    print(f"City: {city}")
    if lat is not None and lon is not None:
        print(f"Coords: {lat}, {lon}")
    else:
        print("Coords not found. Fallback.")
    print()

    #=== Get Forecast ===
    daily = get_daily(city, lat, lon)
    if daily is None:
        print("Weather forecast error")
        return 3

    print(f"Days: {len(daily)}")
    print(f"Period: {daily[0]['date']} - {daily[-1]['date']}")
    print()

    #=== Save to DB ===
    result = save_forecast(city, daily)
    if result is None:
        print("DB saving error")
        return 4

    saved, skipped = result
    print(f"Saved: {saved}")
    print(f"Skipped: {skipped}")
    print()

    #=== Export to Markdown ===
    path = to_markdown(city)
    if path is None:
        print("Markdown export error")
        return 5

    print(f"File: {path}")
    return 0


if __name__ == "__main__":
    code = main()
    exit(code)
