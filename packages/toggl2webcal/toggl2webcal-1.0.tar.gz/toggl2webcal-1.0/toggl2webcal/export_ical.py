import icalendar

from datetime import datetime, timedelta
from .models import TimeEntry


def build_ical(session, filename):
    calendar = icalendar.Calendar()
    calendar.add('prodid', "toggl2ical")
    calendar.add('version', '2.0')
    calendar.add('CALSCALE', 'GREGORIAN')
    calendar.add('X-WR-CALNAME', 'Toggl events')
    calendar.add('method', 'publish')

    for entry in session.query(TimeEntry).order_by(TimeEntry.start):
        entry: TimeEntry
        event = icalendar.Event()
        event.add('summary', entry.description)
        event.add('uid', entry.id)
        event.add('dtstart', entry.start)
        if entry.end:
            adjusted_end = entry.end - timedelta(minutes=5)

            event.add('dtend', adjusted_end)
        else:
            event.add('dtend', datetime.now())
        event.add('dtstamp', datetime.now())
        calendar.add_component(event)

    ical = calendar.to_ical()

    with open(filename, "wb") as file:
        file.write(ical)
