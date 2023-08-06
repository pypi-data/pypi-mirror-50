#!/usr/bin/env python3
import argparse

from .export_ical import build_ical
from .import_toggl import add_entries_to_db
from .models import get_session_creator

example_text = '''Example:

 toggl2webcal TOGGL_TOKEN sqlite:///time.sqlite 
 toggl2webcal TOGGL_TOKEN postgresql://myself@localhost 

'''

parser = argparse.ArgumentParser(
    description="Export toggl data to webcal file",
    epilog=example_text,
    formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument('token', help='Toggl token')
parser.add_argument('database', help='SQL alchemy database connector')

parser.add_argument(
    '-d', '--days',
    type=int,
    help='number of days to look back',
    default=7
)

parser.add_argument(
    '--no-import',
    action='store_true',
    dest='no_import',
    help='Don\'t run import from toggl',
)

parser.add_argument(
    '--no-export',
    action='store_true',
    dest='no_export',
    help='Don\'t run export to webcal',
)

parser.add_argument(
    '-o', '--out',
    help='output path for the webcal file',
    default="calendar.ics"
)


def main():
    args = parser.parse_args()
    Session = get_session_creator(args.database)

    if not args.no_import:
        add_entries_to_db(Session(), args.token, args.days)

    if not args.no_export:
        build_ical(Session(), args.out)


if __name__ == '__main__':
    main()
