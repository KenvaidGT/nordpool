from datetime import date, datetime
from zoneinfo import ZoneInfo
from statistics import mean
from nordpool import elspot

TZ = ZoneInfo("Europe/Riga")


def _fetch_raw(target_date: date, area: str = "LV", resolution: int = 15):
    prices_spot = elspot.Prices("EUR")
    return prices_spot.fetch(
        end_date=target_date,
        areas=[area],
        resolution=resolution,
    )


def get_prices_15min(target_date: date = date.today(), area: str = "LV"):
    data = _fetch_raw(target_date, area, 15)
    result = []

    for entry in data["areas"][area]["values"]:
        result.append({
            "start": entry["start"].astimezone(TZ),
            "end": entry["end"].astimezone(TZ),
            "value": entry["value"],  # EUR/MWh
        })

    return result


def get_daily_average(target_date: date = date.today(), area: str = "LV"):
    prices = get_prices_15min(target_date, area)
    return mean(p["value"] for p in prices)


def get_current_price(area: str = "LV"):
    now = datetime.now(TZ)
    prices = get_prices_15min(date.today(), area)

    for p in prices:
        if p["start"] <= now < p["end"]:
            return p

    return None


if __name__ == "__main__":
    today = date.today()

    prices = get_prices_15min(today)
    avg = get_daily_average(today)

    print(f"Nordpool LV prices for {today} (Europe/Riga)")
    print("-" * 44)

    for p in prices:
        s = p["start"].strftime("%H:%M")
        e = p["end"].strftime("%H:%M")
        print(f"{s} - {e}: {p['value']:.2f} EUR/MWh")

    print("-" * 44)
    print(f"Daily average: {avg:.2f} EUR/MWh")

    current = get_current_price()
    if current:
        s = current["start"].strftime("%H:%M")
        e = current["end"].strftime("%H:%M")
        print(f"Current price ({s}-{e}): {current['value']:.2f} EUR/MWh")