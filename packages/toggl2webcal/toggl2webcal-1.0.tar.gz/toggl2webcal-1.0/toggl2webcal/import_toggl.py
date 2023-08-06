import requests
from datetime import datetime, timedelta

from dateutil.parser import parse
from .models import TimeEntry
import os

TOKEN = os.getenv('TOGGL_TOKEN')

TOGGL_URL_TEMPLATE = "https://www.toggl.com/api/v8/time_entries?start_date={}&end_date={}"
TOGGL_TIME_FORMAT = "%Y-%m-%dT%H:%M:00Z"


def add_entries_to_db(session, api_token, days):
    end_date = datetime.now().strftime(TOGGL_TIME_FORMAT)
    start_date = (datetime.now() - timedelta(days=int(days))).strftime(TOGGL_TIME_FORMAT)

    response = requests.get(TOGGL_URL_TEMPLATE.format(start_date, end_date), auth=(api_token, 'api_token'))
    response.raise_for_status()

    for entry in response.json():
        session.merge(TimeEntry(
            id=entry['id'],
            start=parse(entry["start"]),
            end=parse(entry["stop"]),
            description=entry['description'],
            original_id=entry['id'],
            source='toggl',
        ))

    session.commit()
