from __future__ import print_function

import datetime
import uuid
import os
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.events']

PATH = 'C:\\Users\\andre\\work\\acorn\\acorn\\acorn-377214-72e9ef25960f.json'
SERVICE_ACCOUNT_FILE = PATH

CALENDAR_ID = 'c_fcac2d5608ba437916879de91dc0a7d83ce4ade9588' \
              '05ebd569c267035c92dc0@group.calendar.google.com'

def main():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_credentials = credentials.with_subject('info@acornfintechplatform.co.za')

    try:
        service = build('calendar', 'v3', credentials=delegated_credentials)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

        start_datetime = datetime.datetime.now(tz=pytz.utc)
        event = (
            service.events()
            .insert(
                conferenceDataVersion=1,
                calendarId=CALENDAR_ID,
                body={
                    'summary': 'Google I/O 2015',
                    'location': '800 Howard St., San Francisco, CA 94103',
                    'description': 'A chance to hear more about Google\'s developer products.',
                    'start': {
                        'dateTime': '2022-10-06T09:00:00+02:00',
                        'timeZone': 'Africa/Johannesburg',
                    },
                    'end': {
                        'dateTime': '2022-10-06T17:00:00+02:00',
                        'timeZone': 'Africa/Johannesburg',
                    },
                    'recurrence': [
                        'RRULE:FREQ=DAILY;COUNT=2'
                    ],
                    'attendees': [
                        {'email': 'rori@gmail.com'},
                        {'email': 'l@example.com'},
                    ],
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 10},
                        ],
                    },
                    "conferenceData": {
                        "createRequest": {
                            "requestId": "sample67890",
                            # A unique ID for the client application. Randomly generated.
                            "conferenceSolutionKey": {
                                "type": "hangoutsMeet"
                            },
                        },
                    },
                },

            )
            .execute()
        )



    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
