import datetime

def convert_time_bigquery(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    return dt.isoformat()