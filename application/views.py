"""
The `views.py` file defines the views for the application.

The views are responsible for handling requests from the user and returning
the appropriate response.

The views file contains the following views:
    * `join_meeting`
    * `host_url`
    * `api_connection`
"""
import json
import pathlib
import os
import uuid
from django.utils.timezone import make_aware
from datetime import datetime
import googleapiclient
import threading
from dateutil.parser import parse

from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from system_management.decorators import check_token_in_session
from system_management.general_func_classes import host_url, api_connection, _send_email_thread
import system_management.constants as constants
from system_management.amazons3 import upload_to_s3

PATH = str(os.path.join(settings.BASE_DIR, "acorn-377214-72e9ef25960f.json")).replace('\\', '/')
SERVICE_ACCOUNT_FILE = PATH

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
]

CALENDAR_ID = 'c_fcac2d5608ba437916879de91dc0a7d83ce4ade9588' \
              '05ebd569c267035c92dc0@group.calendar.google.com'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)


@check_token_in_session
def join_meeting(request, assessment_id):
    """Join google meetings for the application assessment."""
    if request.method == 'POST':
        assessment_id = request.POST.get('assessment_id')
        gps_coordinates = request.POST.get('gps_coordinates')

        url = f"{host_url(request)}{reverse('join_meeting_api')}"

        payload = json.dumps({
            "assessment_id": assessment_id,
            "gps_coordinates": gps_coordinates
        })
        headers = {
            "Authorization": f"Token {request.session['token']}",
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, headers=headers, data=payload)
        return JsonResponse(response_data, safe=False)

    if request.method == "GET":
        context = {'id': assessment_id}
        return render(request, 'join_meeting.html', context)


@check_token_in_session
def insurance_providers(request):
    """
    Get all insurance providers for html page.

    :param request:
        Django request object.

    :return:
        Rendered html page for manage insurance providers.    
    """
    if request.method == "GET":
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('insurance_providers_api')}"

        payload = json.dumps({

        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="GET", url=url, data=payload, headers=headers)

        context = {
            "providers": response_data.get('data'),
        }

        return render(request, 'admin/insurance_providers.html', context)


@check_token_in_session
def add_insurance_provider(request):
    """
    Send insurance provider form data to api.

    :param request:
        Django request object.

    :return:
        Return Json response of api call status and data.    
    """
    if request.method == 'POST':
        token = request.session.get('token')

        insurance_name = request.POST['insurance_name']
        email = request.POST['email']
        contact_no = request.POST['contact_no']

        url = f"{host_url(request)}{reverse('add_insurance_provider_api')}"

        payload = json.dumps({
            'insurance_name': insurance_name,
            'email': email,
            'contact_no': contact_no
        })
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload, headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def edit_insurance_provider(request):
    """
    Edit insurance data send to the api for edit insurance provider.

    :param request:
        Django request object.

    :return:
        Return Json response of api call status and data.    
    """
    if request.method == 'POST':
        token = request.session.get('token')

        insurance_name = request.POST.get('insurance_name')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_no')
        insurance_id = request.POST.get('insurance_id')

        url = f"{host_url(request)}{reverse('edit_insurance_provider_api')}"

        payload = json.dumps({
            'insurance_name': insurance_name,
            'email': email,
            'contact_no': contact_no,
            'insurance_id': insurance_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload, headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def del_insurance_provider(request):
    """
    Delete insurance provider send to the api for delete insurance provider.

    :param request:
        Django request object.

    :return:
        Return Json response of api call status and data.    
    """
    if request.method == 'POST':
        token = request.session.get('token')

        insurance_id = request.POST.get('insurance_id')

        url = f"{host_url(request)}{reverse('del_insurance_provider_api')}"

        payload = json.dumps({
            'insurance_id': insurance_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="POST", url=url, data=payload, headers=headers)

        return JsonResponse(response_data, safe=False)


@check_token_in_session
def edit_assessment_note_file(request):
    """
    Edit assessment notes of the application.
    """
    if request.method == 'POST':
        token = request.session.get('token')
        notes_id = request.POST.get('notes_id')
        file = request.FILES.get('notes_file')

        url = f"{host_url(request)}{reverse('edit_assessment_note_file_api')}"

        payload = json.dumps({
            'notes_id': notes_id
        })

        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': constants.JSON_APPLICATION
        }

        response_data = api_connection(method="GET", url=url, data=payload, headers=headers)

        file_name_obj = response_data.get('data').get('note')

        file_name = file_name_obj + f"{str(pathlib.Path(file.name).suffix)}"
        file_url = upload_to_s3(file, file_name)

        payload = json.dumps({
            'notes_id': notes_id,
            'file': file_url
        })

        response_data = api_connection(method="POST", url=url, data=payload, headers=headers)

        return JsonResponse(data=response_data, safe=False)


@check_token_in_session
def save_assessment_notes(request):
    """
    Save assessment notes to S3.
    """
    if request.method == 'POST':
        claim_id = request.POST.get('claim_id')
        assessment_id = request.POST.get('assessment_id')
        descriptions = request.POST.getlist("notes_description[]")
        string = descriptions[0].strip("'")
        description_values = string.split(',')
        files = request.FILES.getlist("notes_file[]")
        files_dictionary = dict(zip(description_values, files))

        url = f"{host_url(request)}{reverse('save_assessment_notes_api')}"

        headers = {
            'Authorization': f'Token {request.session["token"]}',
            'Content-Type': constants.JSON_APPLICATION
        }

        [
            save_note_object(description, file, claim_id, url, headers, assessment_id)
            for description, file in files_dictionary.items()
        ]

        response_data = {
            'status': 'success',
            'message': 'Assessment note saved successfully.'
        }

        return JsonResponse(data=response_data, safe=False)


def save_note_object(description, file, claim_id, url, headers, assessment_id):
    """
    Save note object from list.
    """
    file_name_obj = description
    file_name = file_name_obj + f"{str(pathlib.Path(file.name).suffix)}"
    file_url = upload_to_s3(file, file_name)
    payload = json.dumps({
        'assessment_id': assessment_id,
        'claim_id': claim_id,
        'description': description,
        'file': file_url
    })
    api_connection(method="POST", url=url, data=payload, headers=headers)
    return None


def build_service():
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    return service


@check_token_in_session
def schedule_assessment(request):
    """
    Schedule an assessment.
    
    :param request:
        Django request parameter.

    :return:
        Scheduled google meeting api status.
    
    """
    if request.method == 'POST':
        app_id = request.POST.get('application_id')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {request.session.get("token")}'
        }

        url = f"{host_url(request)}{reverse('get_application_api')}"

        payload = json.dumps({
            "application_id": app_id,
            'assessor_id': request.session.get('user_id')
        })

        response_data = api_connection(
            method="GET",
            url=url,
            data=payload,
            headers=headers
        )

        status = response_data.get('status')

        if status != 'success':
            return JsonResponse(data=response_data, safe=False)

        application = response_data.get('application')
        client = application.get('client')
        assessor = application.get('assessor')

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')

        start_date = str(make_aware(datetime.strptime(
            start_date,
            '%Y-%m-%dT%H:%M'
        )
        ))

        end_date = str(make_aware(datetime.strptime(
            end_date,
            '%Y-%m-%dT%H:%M'
        )
        ))

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        delegated_credentials = credentials.with_subject('info@acornfintechplatform.co.za')

        try:
            service = build('calendar', 'v3', credentials=delegated_credentials)

            if assessor:
                event = (
                    service.events()
                    .insert(
                        calendarId=CALENDAR_ID,
                        conferenceDataVersion=1,
                        body={
                            'summary': f'Assessment {str(application["id"])}',
                            'location': 'Online',
                            'visibility': 'public',
                            'description': description,
                            'start': {
                                'dateTime': parse(start_date).isoformat(),
                                'timeZone': 'Africa/Johannesburg',
                            },
                            'end': {
                                'dateTime': parse(end_date).isoformat(),
                                'timeZone': 'Africa/Johannesburg',
                            },

                            'reminders': {
                                'useDefault': False,
                                'overrides': [
                                    {'method': 'email', 'minutes': 24 * 60},
                                    {'method': 'popup', 'minutes': 10},
                                ],
                            },
                            "attendees": [
                                {
                                    "id": assessor['id'],
                                    "displayName": f"{assessor['first_name']} {assessor['last_name']}",
                                    "email": assessor['email'],
                                },
                                {
                                    "id": client['id'],
                                    "displayName": f"{client['first_name']} {client['last_name']}",
                                    "email": client['email'],
                                },
                            ],
                        },
                    )
                    .execute()
                )
            else:
                event = (
                    service.events()
                    .insert(
                        calendarId=CALENDAR_ID,
                        conferenceDataVersion=1,
                        body={
                            'summary': f'Assessment {str(application["id"])}',
                            'location': 'Online',
                            'visibility': 'public',
                            'description': description,
                            'start': {
                                'dateTime': parse(start_date).isoformat(),
                                'timeZone': 'Africa/Johannesburg',
                            },
                            'end': {
                                'dateTime': parse(end_date).isoformat(),
                                'timeZone': 'Africa/Johannesburg',
                            },

                            'reminders': {
                                'useDefault': False,
                                'overrides': [
                                    {'method': 'email', 'minutes': 24 * 60},
                                    {'method': 'popup', 'minutes': 10},
                                ],
                            },
                            "attendees": [
                                {
                                    "id": client['id'],
                                    "displayName": f"{client['first_name']} {client['last_name']}",
                                    "email": client['email'],
                                },
                            ],
                        },
                    )
                    .execute()
                )

            event_summary = event['summary']
            event_id = event['id']
            end_time = event['end']['dateTime']

            payload = json.dumps({
                "application_id": application['id'],
                "description": description,
                "start_date": start_date,
                "end_time": end_time,
                "event_summary": event_summary,
                "event_id": event_id,
            })

            url = f"{host_url(request)}{reverse('create_assessment_api')}"

            response_data = api_connection(
                method="POST",
                url=url,
                data=payload,
                headers=headers
            )

            status = response_data.get('status')

            if status == 'success':
                url = f"{host_url(request)}{reverse('send_email_api')}"
                assessment_id = response_data.get('assessment_id')
                if assessor:
                    join_link = reverse("join_meeting", args=(assessment_id,))
                    join_url = f'{host_url(request)}{join_link}'

                    subject = ' You have a scheduled meetings at acorn'

                    html_tpl_path = 'email_temps/google_meeting_assessor.html'

                    receiver_email = assessor['email']

                    context_data = {
                        'assessor_email': assessor['email'],
                        'assessor_first_name': assessor['first_name'],
                        'assessor_last_name': assessor['last_name'],
                        'client_email': client['email'],
                        'client_first_name': client['first_name'],
                        'client_last_name': client['last_name'],
                        'meeting_link': join_url,
                        'meeting_message': description,
                        'meeting_date': start_date
                    }

                    payload = json.dumps({
                        "html_tpl_path": html_tpl_path,
                        "receiver_email": receiver_email,
                        "context_data": context_data,
                        "subject": subject,
                    })

                    thread = threading.Thread(target=_send_email_thread, args=(url, headers, payload))
                    thread.start()


                url = f"{host_url(request)}{reverse('create_room_api')}"
                payload = json.dumps({
                    "assessment_id": assessment_id
                })
                response_data = api_connection(
                    method="POST",
                    url=url,
                    data=payload,
                    headers=headers
                )
                status = response_data.get('status')

                if status == 'success':
                    url = f"{host_url(request)}{reverse('send_email_api')}"
                    client = response_data.get('data')

                    login_link = f"{host_url(request)}{reverse('login_view')}"
                    subject = ' You have a scheduled meetings at acorn'

                    receiver_email = client['email']

                    html_tpl_path = 'email_temps/client_login.html'

                    context_data = {
                        'client_email': client['email'],
                        'client_first_name': client['first_name'],
                        'client_last_name': client['last_name'],
                        'login_url': login_link,
                        'password': client['password'],
                        'meeting_date': start_date
                    }

                    payload = json.dumps({
                        "html_tpl_path": html_tpl_path,
                        "receiver_email": receiver_email,
                        "context_data": context_data,
                        "subject": subject,
                    })

                    thread = threading.Thread(
                        target=_send_email_thread, 
                        args=(url, headers, payload
                    ))
                    thread.start()

                    response_data = {
                        'status': 'success',
                        'message': 'Assessment created successfully'
                    }

            return JsonResponse(response_data, safe=False)

        except:
            response_data = {
                'status': 'error',
                'message': 'An error occurred creating an Assessment'
            }
            return JsonResponse(response_data, safe=False)
       


@check_token_in_session
def complete_status(request, application_id):
    if request.method == 'GET':
        application_status = constants.COMPLETED

        url = f"{host_url(request)}{reverse('complete_status_api')}"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {request.session.get("token")}'
        }
        payload = json.dumps({
            "application_id": application_id,
            "application_status": application_status

        })

        response_data = api_connection(method="POST", data=payload, url=url, headers=headers)
        response_status = response_data.get('status')
        if response_status == 'success':
            return redirect('manage_application', application_id=application_id)

    return render(request, 'assessor/assessor.html')


@check_token_in_session
def change_application_status(request):
    """
    Change application status based on send data.

    :param request:
        Django rest framework
    :return:
        Status of api call.
    """
    if request.method == 'POST':
        application_status = request.POST.get('application_status')
        application_id = request.POST.get('application_id')

        url = f"{host_url(request)}{reverse('change_status_api')}"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {request.session.get("token")}'
        }
        payload = json.dumps({
            "application_id": application_id,
            "application_status": application_status

        })

        response_data = api_connection(method="POST", data=payload, url=url, headers=headers)
        return JsonResponse(data=response_data, safe=False)


@check_token_in_session
def event_calendar(request):
    """
    Events for application assessments.

    :param request:
        Django rest framework
    :return:
        Status of api call.
    """
    if request.method == 'GET':
        url = f"{host_url(request)}{reverse('event_calendar_api')}"
        payload = json.dumps({
            'user_id': request.session.get('user_id')
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {request.session.get("token")}'
        }

        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)
        status = response_data.get('status')

        context = {}

        if status == 'success':
            events = response_data.get('data')
            context = {
                'events': events
            }
        return render(request, 'assessment/calendar.html', context)
    
    

@check_token_in_session
def create_room(request):
    if request.method == 'POST':
        token = request.session.get('token')
        room_name = request.POST.get('room_name')
        url = f"{host_url(request)}{reverse('create_room_api')}"
        payload = json.dumps({
            "room_name": room_name
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {token}'
        }
        response_data = api_connection(method="POST", url=url, headers=headers, data=payload)

        return JsonResponse(response_data, safe=True)


@check_token_in_session
def video_conference(request, assessment_id):
    """
    Video conference.

    :param request:
        Django rest framework
    :param assessment_id:
        Assessment ID for event room.
    :return:
        Status of api call.
    """
    if request.method == 'GET':
        token = request.session.get('token')
        url = f"{host_url(request)}{reverse('video_conference_api')}"
        payload = json.dumps({
            'assessment_id': assessment_id
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {token}'
        }
        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)
        status = response_data.get('status')
        context = {}

        if status == 'success':
            room_id = response_data.get('data').get('id')
            room_status = response_data.get('data').get('room_status')
            if room_status == constants.COMPLETE:
                return redirect('video_complete_status', twilio_room_id=room_id)

            context = {
                'twilio_room_id': room_id
            }
        return render(request, 'assessment/video_conference.html', context)


@check_token_in_session
def get_assessments(request):
    """
    Get all assessments for a selected day to show in the calendar.

    :param request:
        Django rest framework
    :return:
        Status of api call.
    """
    if request.method == 'POST':
        date = request.POST.get('date')
        url = f"{host_url(request)}{reverse('get_assessments_api')}"
        payload = json.dumps({
            'date': date
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {request.session.get("token")}'
        }

        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)
        return JsonResponse(response_data, safe=True)


@check_token_in_session
def get_assessment_info(request):
    """
     Get single assessment info for calendar

    :param request:
        Django rest framework
    :return:
        Status of api call.
    """
    if request.method == 'POST':
        assessment_id = request.POST.get('assessment_id')
        url = f"{host_url(request)}{reverse('get_assessment_info_api')}"
        payload = json.dumps({
            'assessment_id': assessment_id
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {request.session.get("token")}'
        }

        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)
        return JsonResponse(response_data, safe=True)


@check_token_in_session
def get_event_token(request):
    """
     Get single assessment info for calendar

    :param request:
        Django rest framework
    :return:
        Status of api call.
    """
    if request.method == 'GET':
        twilio_room_id = request.GET.get('twilio_room_id')
        url = f"{host_url(request)}{reverse('get_event_token_api')}"
        payload = json.dumps({
            'twilio_room_id': twilio_room_id,
            'user_id': request.session.get('user_id')
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {request.session.get("token")}'
        }

        response_data = api_connection(method="GET", url=url, headers=headers, data=payload)
        return JsonResponse(response_data, safe=True)


@check_token_in_session
def mark_event_complete(request):
    """
    Mark event complete.

    :param request:
        Django rest framework
    :return:
        Status of api call.
    """
    if request.method == 'POST':
        twilio_room_id = request.POST.get('twilio_room_id')
        url = f"{host_url(request)}{reverse('mark_event_complete_api')}"
        payload = json.dumps({
            'room_id': twilio_room_id
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {request.session.get("token")}'
        }

        response_data = api_connection(method="POST", url=url, headers=headers, data=payload)
        return JsonResponse(response_data, safe=True)


@check_token_in_session
def video_complete_status(request, twilio_room_id):
    """
    Video is complete page.

    :param request:
        Django rest framework
    :return:
        render html page
    """
    if request.method == 'GET':
        url = f"{host_url(request)}{reverse('recording_to_s3_api')}"
        payload = json.dumps({
            'room_id': twilio_room_id
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {request.session.get("token")}'
        }

        response_data = api_connection(method="POST", url=url, headers=headers, data=payload)
        return render(request, 'assessment/video_complete_status.html', response_data)
