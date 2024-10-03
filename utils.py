from datetime import datetime, timedelta, timezone
import pytz

def convert_time_bigquery(timestamp):
    dt = datetime.fromtimestamp(timestamp / 1000.0)
    return dt.isoformat()

def more_than_twenty_four_hours(message_time):
    local_timezone = pytz.timezone('America/Sao_Paulo')
    date = datetime.strptime(message_time, '%d/%m/%y %H:%M:%S')
    date = local_timezone.localize(date)
    now = datetime.now(local_timezone)
    return now - date > timedelta(hours=24)

def bigquery_now():
    local_timezone = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(local_timezone)
    return now.isoformat()

def datetime_to_iso(datetime_object):
    return datetime_object.isoformat()