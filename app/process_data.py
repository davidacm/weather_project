from datetime import datetime, timedelta

from . import conversions


def from_time(utc_time: float, seconds_timezone: int) -> datetime:
    """creates a datetime object, from an float seconds in unix format, and the timezone specified in seconds.

    Args:
        utc_time (float): the UTC time
        seconds_timezone (int): the timezone, this will change the final result.

    Returns:
        datetime: the datetime with the specified timezone.
    """
    time = datetime.utcfromtimestamp(utc_time)
    time += timedelta(seconds=seconds_timezone)
    return time


def process_json(json: dict):
    result = {
        'location_name': f"{json['name']}, {json['sys']['country']}",
        'pressure': f"{json['main']['pressure']} hpa",
        'humidity': f"{json['main']['humidity']}%",
        'geo_coordinates': f"[{json['coord']['lat']}, {json['coord']['lon']}]",
    }

    celsius = json['main']['temp']
    fahrenheit = conversions.celsius_to_fahrenheit(celsius)
    result['temperature'] = f"{celsius} °C, {fahrenheit} °F"

    wind_description = conversions.wind_velocity_to_description(json['wind']['speed'])
    cardinal = conversions.degrees_to_cardinal(json['wind']['deg'])
    result['wind'] = f"{wind_description}, {json['wind']['speed']} m/s, {cardinal}"

    result['cloudiness'] = conversions.cloudiness_percent_to_description(json['clouds']['all'])

    time = from_time(json['sys']['sunrise'], json['timezone'])
    result['sunrise'] = time.strftime('%H:%M')

    time = from_time(json['sys']['sunset'], json['timezone'])
    result['sunset'] = time.strftime('%H:%M')

    # requested time: server time in UTC.
    time = datetime.utcnow()
    result['requested_time'] = time.strftime("%Y-%m-%d %H:%M:%S")

    return result

