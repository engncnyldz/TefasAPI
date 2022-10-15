from datetime import date, datetime, timedelta
from pytz import timezone, country_timezones
from ..config import settings

def get_expire_time():

    refresh_hour = settings.refresh_hour
    refresh_day = date.today().day

    refresh_datetime = datetime(date.today().year, date.today().month, refresh_day, refresh_hour, 0, 0)


    if (refresh_hour == 0):
        refresh_datetime = refresh_datetime + timedelta(days=1)

    istanbul_timezone = timezone(country_timezones.get("TR")[0])
    refresh_time = int(istanbul_timezone.localize(refresh_datetime).timestamp())
    time_now = int(datetime.now().timestamp())
    expires_at = refresh_time

    if (time_now > refresh_time):
        expires_at = refresh_datetime + timedelta(days=1)

    return expires_at
