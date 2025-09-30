"""
cron.py file used for the crontab actions for the Google calendar.

"""
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from application.models import Application
from application.models import Assessment


SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]
PATH = str(os.path.join(settings.BASE_DIR, "acorn-377214-72e9ef25960f.json")).replace('\\', '/')
SERVICE_ACCOUNT_FILE = PATH
CALENDAR_ID = 'c_fcac2d5608ba437916879de91dc0a7d83ce4ade9588' \
              '05ebd569c267035c92dc0@group.calendar.google.com'


def my_cron_job():
    """
    Cron job for the collection of the Google meeting information.
    """
    complete_applications_ids = Application.objects.filter(
        application_status_id=3).values_list('id', flat=True)

    id_list = Assessment.objects.filter(application_id__in=complete_applications_ids,
                                        video_link="", event_id__isnull=False
                                        ).values_list('application_id', flat=True)
    if id_list:
        [get_video_attachment_link(application_id) for application_id in id_list]
        return None
    else:
        return None


def get_video_attachment_link(application_id):
    """
    Get the video attachment of the assigned Google meeting.
    """
    assessment = Assessment.objects.get(application_id=application_id)

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_credentials = credentials.with_subject('info@acornfintechplatform.co.za')

    try:
        service = build('calendar', 'v3', credentials=delegated_credentials)
        event = service.events().get(calendarId=CALENDAR_ID, eventId=assessment.event_id).execute()
        try:
            assessment.video_link = event['attachments'][0]['fileUrl']
            assessment.save()
        except KeyError:
            assessment.video_link = ""
            assessment.save()
        return None
    except HttpError:
        return None