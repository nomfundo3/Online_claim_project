"""
Application front end logic views containing the following views.

"""
import json
import io
from system_management.amazons3 import delete_s3_file, upload_to_s3, open_s3_file
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from application.api.serializers import GetApplicationStatusSerializer
import system_management.constants as constants
from system_management.models import (
    User,
    UserType,
    Profile
)
from system_management.views import (
    generate_password
)
from application.models import (
    Assessment,
    InsuranceProvider,
    ApplicationType,
    ApplicationStatus,
    Application,
    Client,
    Business,
    ClientIncident,
    TwilioRoom,
    TwilioRecording
)
from application.api.serializers import (
    AssessmentSerializer,
    InsuranceProviderSerializer,
    ApplicationTypeSerializer,
    InsuranceProviderModelSerializer,
    UpdateInsuranceProviderSerializer,
    DeleteInsuranceProviderSerializer,
    CreateApplicationSerializer,
    EditAssessmentNoteFileSerializer,
    SingleAssessmentNoteSerializer,
    AssessmentNoteModalSerializer,
    CreateAssessmentNotesSerializer,
    CreateAssessmentSerializer,
    GetApplicationSerializer,
    ApplicationAssessmentSerializer,
    CreateRoomSerializer,
    GetAssessmentsSerializer,
    AssessmentModelSerializer,
    AssessmentApplicationSerializer,
    GetAssessmentInfoSerializer,
    GetRoomSerializer,
    EventCalendarSerializer,
    GetAssessmentEventTokenSerializer,
    TwilioRoomModelSerializer
)
from surveys.models import (
    Survey
)
from decouple import config
from twilio.rest import Client as CL
import twilio
import pandas as pd
from claims.models import (
    HowQuestionAnswer,
    WhatQuestionAnswer,
    Application,
    ApplicationHow,
    ApplicationWhat,
    ApplicationCause,
    AssessmentNote,
    Claim
)


@api_view(['GET'])
def get_application_types_api(request):
    """
    This function is used to get the application types

    :param request:
        request django parameter
    :return:
        application types
    """
    if request.method == "GET":
        application_types = ApplicationType.objects.all()
        serializer = ApplicationTypeSerializer(application_types, many=True)
        data = json.dumps({
            "status": "success",
            "data": serializer.data
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            'status': "error",
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data, status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def join_meeting_api(request):
    """
    Join meeting api for client location update.

    Args:
        request:
    Returns:
        Response:
        data:
            - status
            - message
        status code:
    """
    if request.method == "POST":
        body = json.loads(request.data)
        serializer = AssessmentSerializer(data=body)
        if serializer.is_valid():
            assessment_id = serializer.validated_data.get('assessment_id')
            location = serializer.validated_data.get('gps_coordinates')

        else:
            data = json.dumps({
                'status': "error",
                'message': str(serializer.errors)
            })
            return Response(data, status.HTTP_400_BAD_REQUEST)

        assessment = Assessment.objects.get(id=assessment_id)
        assessment.client_location = location
        assessment.save()

        data = json.dumps({
            'status': 'success',
            'message': 'Assessment joined successfully'
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:

        data = json.dumps({
            'status': "error",
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data, status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def insurance_providers_api(request):
    """
    This function is used to get the list of insurance providers

    :param request:
        request django parameter
    :return:
        list of insurance providers

    """
    if request.method == "GET":
        all_providers = InsuranceProvider.objects.all()
        serializer = InsuranceProviderModelSerializer(all_providers, many=True)

        data = json.dumps({
            "status": "success",
            "message": "Insurance providers retrieved successfully.",
            "data": serializer.data
        })

        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_insurance_provider_api(request):
    """
    API for the add of a new insurance provider.

    :param request:
        Django request parameter.

    :return:
        Response of status of api call and status code.
        
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = InsuranceProviderSerializer(data=body)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            insurance_name = validated_data['insurance_name']
            email = validated_data['email']
            contact_no = validated_data['contact_no']

            if InsuranceProvider.objects.filter(insurance_name=insurance_name).exists():
                data = json.dumps({
                    'status': "error",
                    'message': f"Insurance Provider with name {insurance_name} already exists."
                })
                return Response(data, status.HTTP_400_BAD_REQUEST)

            InsuranceProvider.objects.create(
                insurance_name=insurance_name,
                email=email,
                contact_no=contact_no
            )

            all_providers = InsuranceProvider.objects.all()
            updated_serializer = InsuranceProviderModelSerializer(all_providers, many=True)

            response_data = json.dumps({
                "status": "success",
                "message": "Insurance provider added successfully",
                "data": updated_serializer.data
            })

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = json.dumps({
                "status": "error",
                "errors": serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_insurance_provider_api(request):
    """
    API for the edit of insurance providers.

    :param request:
        Django request parameter.

    :return:
        Response of status of api call and status code.
        
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = UpdateInsuranceProviderSerializer(data=body)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            insurance_name = validated_data['insurance_name']
            email = validated_data['email']
            contact_no = validated_data['contact_no']
            insurance_id = validated_data['insurance_id']

            InsuranceProvider.objects.filter(id=insurance_id).update(
                insurance_name=insurance_name,
                email=email,
                contact_no=contact_no
            )

            all_providers = InsuranceProvider.objects.all()
            updated_serializer = InsuranceProviderModelSerializer(all_providers, many=True)

            response_data = json.dumps({
                "status": "success",
                "message": "Insurance provider added successfully",
                "data": updated_serializer.data
            })

            return Response(response_data, status=status.HTTP_201_CREATED)

        else:
            response_data = json.dumps({
                "status": "error",
                "errors": serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def del_insurance_provider_api(request):
    """
    Delete insurance provider from the database.

    :param request:
        Django request parameter.

    :return:
        Response of status of api call and status code.
        
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = DeleteInsuranceProviderSerializer(data=body)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            insurance_id = validated_data['insurance_id']

            try:
                insurance = InsuranceProvider.objects.get(id=insurance_id)

            except InsuranceProvider.DoesNotExist:
                response_data = json.dumps({
                    "status": "error",
                    "message": "Insurance provider does not exist"
                })
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            Client.objects.filter(
                insurer_id=insurance.id
            ).update(
                insurer_id = None
            )

            insurance.delete()
            all_providers = InsuranceProvider.objects.all()
            updated_serializer = InsuranceProviderModelSerializer(all_providers, many=True)

            response_data = json.dumps({
                "status": "success",
                "message": "Insurance provider deleted successfully",
                "data": updated_serializer.data
            })

            return Response(response_data, status=status.HTTP_201_CREATED)

        else:
            response_data = json.dumps({
                "status": "error",
                "errors": serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_application_api(request):
    """
    Create a application api based on info in body.

    :param request:
        Django request parameter.
    :return:
        Response of api call with data and status of api call. 
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = CreateApplicationSerializer(data=body)

        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors),
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        application_category = validated_data.get('application_category')
        application_type = validated_data.get('application_type')
        user_id = validated_data.get('user_id')
        client_id = validated_data.get('client_id')

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Client does not exist'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        try:
            application_type = ApplicationType.objects.get(name=application_type)
        except ApplicationType.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Application type does not exist'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        try:
            application_status = ApplicationStatus.objects.get(name=constants.PENDING)

        except ApplicationStatus.DoesNotExist:
            application_status = ApplicationStatus.objects.create(name=constants.PENDING)

        application = Application.objects.create(
            user_id=user_id,
            application_status_id=application_status.id,
            client_id=client.id
        )

        if application_category == constants.CLAIM:
            Claim.objects.create(
                application_id=application.id,
                application_type_id=application_type.id
            )

        elif application_category == constants.SURVEY:
            Survey.objects.create(
                application_id=application.id,
                application_type_id=application_type.id
            )

        else:

            application.delete()

            response_data = json.dumps({
                'status': 'error',
                'message': 'Application category does not exist'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        data = {
            'id': application.id,
        }

        response_data = json.dumps({
            'status': 'success',
            'message': 'Application created successfully',
            'data': data
        })
        return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def edit_assessment_note_file_api(request):
    """
    Edit assessment notes api for assessment file update.

    :param request:
        Django request parameter.
    
    :return:
        - GET:
            Response of api call with data and status of api call.
        - POST:
            Response of api call with data and status of api call.
    """
    if request.method == 'GET':
        body = json.loads(request.body)
        serializer = SingleAssessmentNoteSerializer(data=body)

        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors),
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        notes_id = validated_data.get('notes_id')
        assessment_note = AssessmentNote.objects.filter(id=notes_id)

        if not assessment_note.exists():
            response_data = json.dumps({
                'status': 'error',
                'message': 'Assessment note not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        assessment_note = assessment_note.first()
        serializer = AssessmentNoteModalSerializer(assessment_note)

        response_data = json.dumps({
            'status': 'success',
            'message': 'Assessment note file data',
            'data': serializer.data
        })
        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        body = json.loads(request.body)

        serializer = EditAssessmentNoteFileSerializer(data=body)
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors),
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        file = validated_data.get('file')
        notes_id = validated_data.get('notes_id')

        try:
            assessment_note = AssessmentNote.objects.get(id=notes_id)

        except AssessmentNote.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Assessment note not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        assessment_note.file = file
        assessment_note.save()

        response_data = json.dumps({
            'status': 'success',
            'message': 'File uploaded successfully'
        })
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def save_assessment_notes_api(request):
    """
    Save assessment notes api for assessment file upload.

    :param request:
        Django request parameter.
    
    :return:
        - POST:
            Response of api call with data and status of api call.
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = CreateAssessmentNotesSerializer(data=body)

        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors),
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        claim_id = validated_data.get('claim_id')
        assessment_id = validated_data.get('assessment_id')
        description = validated_data.get('description')
        file = validated_data.get('file')

        try:
            assessment = Assessment.objects.get(id=assessment_id)

        except Assessment.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Assessment not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        try:
            claim = Claim.objects.get(id=claim_id)

        except Claim.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Claim not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        if AssessmentNote.objects.filter(
                assessment_id=assessment_id,
                claim_id=claim_id,
                note=description
        ).exists():
            response_data = json.dumps({
                'status': 'error',
                'message': 'Assessment with description already exists'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        AssessmentNote.objects.create(
            note=description,
            assessment_id=assessment.id,
            claim_id=claim.id,
            file=file,
        )

        response_data = json.dumps({
            'status': 'success',
            'message': 'Assessment note saved successfully'
        })
        return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_assessment_api(request):
    """
    Create an assessment object based on assigned date and description. 

    :param request:
        Django request parameter.
    
    :return:
        - POST:
            Response of api call with data and status of api call.
    """
    body = json.loads(request.body)
    serializer = CreateAssessmentSerializer(data=body)
    if not serializer.is_valid():
        response_data = json.dumps({
            'status': 'error',
            'message': str(serializer.errors),
        })
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data

    application_id = validated_data.get('application_id')
    description = validated_data.get('description')
    start_date = validated_data.get('start_date')
    end_time = validated_data.get('end_time')
    event_summary = validated_data.get('event_summary')
    event_id = validated_data.get('event_id')

    try:
        application = Application.objects.get(id=application_id)

    except Application.DoesNotExist:
        response_data = json.dumps({
            'status': 'error',
            'message': 'Application not found'
        })
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    application_stats = ApplicationStatus.objects.values(
        'id',
        'name'
    ).filter(name=constants.SCHEDULED)

    if application_stats.exists():
        application_status_id = application_stats.first()['id']
    else:
        application_status_id = ApplicationStatus.objects.create(
            name=constants.SCHEDULED
        ).id

    if not Assessment.objects.filter(application_id=application.id).exists():
        assessment = Assessment.objects.create(
            message=description,
            scheduled_date_time=start_date,
            end_date_time=end_time,
            application_id=application.id,
            summary=event_summary,
            event_id=event_id
        )

        application.application_status_id = application_status_id
        application.save()

    else:
        assessment = Assessment.objects.get(
            application_id=application.id
        )
        assessment.message = description
        assessment.scheduled_date_time = start_date
        assessment.end_date_time = end_time
        assessment.summary = event_summary
        assessment.event_id = event_id
        assessment.save()

        application.application_status_id = application_status_id
        application.save()

    response_data = json.dumps({
        'status': 'success',
        'message': 'Assessment created successfully',
        'assessment_id': assessment.id
    })
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_application_api(request):
    """
    Get application for single id passed.

    :param request:
        Django request parameter.
    
    :return:
        - POST:
            Response of api call with data and status of api call.
    """
    if request.method == 'GET':
        body = json.loads(request.body)
        serializer = GetApplicationSerializer(data=body)
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors),
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        application_id = validated_data.get('application_id')

        application = Application.objects.filter(
            id=application_id
        )

        if not application.exists():
            response_data = json.dumps({
                'status': 'error',
                'message': 'Application not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        application = application.first()

        application_serializer = ApplicationAssessmentSerializer(application)

        response_data = json.dumps({
            'status': 'success',
            'message': 'Application found successfully',
            'application': application_serializer.data,
        })

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def complete_status_api(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = GetApplicationStatusSerializer(data=body)
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        application_id = validated_data.get('application_id')
        application_status = validated_data.get('application_status')

        try:

            application = Application.objects.get(id=application_id
                                                  )
        except Application.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Application not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        application_stats = ApplicationStatus.objects.values(
            'name'
        ).filter(
            name=application_status
        )

        if application_stats.exists():
            application_status = ApplicationStatus.objects.get(
                name=constants.COMPLETED
            )
        else:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Application status does not exists'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        application.application_status_id = application_status.id
        application.save()

        response_data = json.dumps({
            'status': 'success',
            'message': 'Application completed successfully',
        })

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def change_status_api(request):
    """
    Change application status to assigned status.

    :param request:
        Django request parameter.
    
    :return:
        - POST:
            Response of api call with data and status of api call.
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = GetApplicationStatusSerializer(data=body)
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        application_id = validated_data.get('application_id')
        application_status = validated_data.get('application_status')

        try:
            application = Application.objects.get(id=application_id
                                                  )
        except Application.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Application not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        try:
            application_status = ApplicationStatus.objects.get(name=application_status)

        except ApplicationStatus.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Application Status not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        application.application_status_id = application_status.id
        application.save()

        response_data = json.dumps({
            'status': 'success',
            'message': 'Application status changed successfully',
        })

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def event_calendar_api(request):
    """
    Events for assessments scheduled for applications.

    :param request:
        Django request parameter.
    
    :return:
        - GET:
            Response of api call with data and status of api call.
    """
    if request.method == "GET":
        serializer = EventCalendarSerializer(data=request.data)
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        user_id = validated_data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'User not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        if user.user_type.name == constants.ADMIN:
            assessments = Assessment.objects.all()
        elif user.user_type.name == constants.CLIENT_ROLE:
            assessments = Assessment.objects.filter(
            application_id__client_id__email = user.email)
        else:
            assessments = Assessment.objects.filter(
                application_id__assessor_id = user_id
            )

        assessments_serializer = AssessmentModelSerializer(assessments, many=True)
        df_assessments = pd.DataFrame(assessments_serializer.data)

        if not df_assessments.empty:
            df_assessments = df_assessments.sort_values(by='scheduled_date_time')

        response_data = json.dumps({
            'status': 'success',
            'message': 'Assessments retrieved successfully',
            'data': df_assessments.to_dict(orient='records')
        })
        return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_room_api(request):
    """
    Create a room in twilio api

    Args:
        request (Request): Django request parameter.

    Returns:
        Response: Django response parameter.
    """
    if request.method == 'POST':
        serializer = CreateRoomSerializer(data=request.data)

        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        assessment_id = validated_data.get('assessment_id')

        try:
            assessment = Assessment.objects.get(id=assessment_id)

        except Assessment.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Assessment not found'
            })
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

        client_object = assessment.application.client
        password = generate_password()
        try:
            user_client = User.objects.get(email=client_object.email)
            user_client.set_password(password)
            user_client.save()

        except User.DoesNotExist:
            try:
                role_client = UserType.objects.get(name = constants.CLIENT_ROLE)
            except UserType.DoesNotExist:
                response_data = json.dumps({
                    'status': 'error',
                    'message': 'User type not found'
                })
                return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)
            user_client = User.objects.create_user(
                email=client_object.email,
                first_name=client_object.first_name,
                last_name=client_object.last_name,
                user_type=role_client,
                password=password
            )
            Profile.objects.create(
                id_number=client_object.id_number,
                phone_number=client_object.phone_number,
                street_address=constants.EMPTY,
                suburb=constants.EMPTY,
                city=constants.EMPTY,
                province=constants.EMPTY,
                user=user_client
            )

        room_name = f"{assessment.summary}_{config('COMPANY_PATH')}"
        client = CL(config('ACCOUNT_SID'), config('AUTH_TOKEN'))
        try:
            room = client.video.v1.rooms.create(
                record_participants_on_connect=True,
                type='group',
                unique_name=room_name
            )
            TwilioRoom.objects.update_or_create(
                assessment_id=assessment.id,
                defaults={
                    "room_sid":room.sid,
                    "room_name":room_name,
                    "room_status":constants.ACTIVE
                }
            )
            
            data = {
                'password': password,
                'email': user_client.email,
                'first_name': user_client.first_name,
                'last_name': user_client.last_name,
            }
            response_data = json.dumps({
                'status': 'success',
                'message': 'Room created successfully',
                'data': data
            })
            return Response(data=response_data, status=status.HTTP_200_OK)

        except twilio.base.exceptions.TwilioRestException as e:
            if 'room exists' in str(e):
                response_data = json.dumps({
                    'status': 'success',
                    'message': 'Room already created successfully'
                })
                return Response(data=response_data, status=status.HTTP_200_OK)
            else:
                
                response_data = json.dumps({
                    'status': 'error',
                    'message':"Apologies, we have exceeded the allowed rate for requests. kindly wait for a duration of 10 minutes before attempting again. Thank you for your patience and understanding."
                })
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def complete_room_api(request):
    """
    Complete a room in twilio api

    Args:
        request (Request): Django request parameter.

    Returns:
        Response: Django response parameter.
    """
    if request.method == 'POST':
        serializer = GetRoomSerializer(data=request.data)

        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        room_id = validated_data.get('room_id')
        client = CL(config('ACCOUNT_SID'), config('AUTH_TOKEN'))
        try:
            twilio_room = TwilioRoom.objects.get(id=room_id)
        except TwilioRoom.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Room not found'
            })
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

        client.video.v1.rooms(twilio_room.sid).update(status='completed')
        twilio_room.room_status=constants.COMPLETE
        twilio_room.save()

        response_data = json.dumps({
            'status': 'success',
            'message': 'Room completed successfully',
        })
        return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_assessments_api(request):
    """
    Retrieve the assessments for the selected date.

    Args:
        request(Django): Django request parameter.

    Returns:
        Response: Django response parameter.
    """
    if request.method == 'GET':
        serializer = GetAssessmentsSerializer(data=request.data)

        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        date = validated_data.get('date')

        assessments = Assessment.objects.filter(
            scheduled_date_time__contains=date
        )
        assessments_serializer = AssessmentModelSerializer(assessments, many=True)
        df_assessments = pd.DataFrame(assessments_serializer.data)
        if not df_assessments.empty:
            df_assessments = df_assessments.sort_values(by='scheduled_date_time')
        
        response_data = json.dumps({
            'status': 'success',
            'message': 'Assessments retrieved successfully',
            'data': df_assessments.to_dict(orient='records')
        })
        return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_assessment_info_api(request):
    """
    Get assessment info for single id passed.

    :param request:
        Django request parameter.
    
    :return:
        - GET:
            Response of api call with data and status of api call.
    """
    if request.method == 'GET':
        body = json.loads(request.body)
        serializer = GetAssessmentInfoSerializer(data=body)
        
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors),
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        assessment_id = validated_data.get('assessment_id')

        assessment = Assessment.objects.filter(
            id=assessment_id
        )

        if not assessment.exists():
            response_data = json.dumps({
                'status': 'error',
                'message': 'Assessment not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        assessment = assessment.first()
        assessment_serializer = AssessmentApplicationSerializer(assessment)
        response_data = json.dumps({
            'status': 'success',
            'message': 'Assessments retrieved successfully',
            'data': assessment_serializer.data
        })
        return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_event_token_api(request):
    """
    Get twilio token for video meeting

    Args:
        request(django): Django rest framework request

    Return:
        Response: JWT token
    """
    if request.method == 'GET':
        body = json.loads(request.body)
        serializer = GetAssessmentEventTokenSerializer(data=body)
        
        
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors),
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        twilio_room_id = validated_data.get('twilio_room_id')
        user_id = validated_data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'User not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        try:
            twilio_room = TwilioRoom.objects.get(id=twilio_room_id)
        except TwilioRoom.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Room not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        account_sid = config('ACCOUNT_SID')
        api_key = config('TWILIO_API_KEY')
        api_secret = config('TWILIO_API_KEY_SECRET')

        # required for Video grant
        identity = user.email

        # Create Access Token with credentials
        token = AccessToken(
            account_sid=account_sid, 
            signing_key_sid=api_key, 
            secret=api_secret, 
            identity=identity,
            ttl=3600
        )
        room_name = twilio_room.room_name
        
        # Create a Video grant and add to token
        video_grant = VideoGrant(
            room=room_name
        )

        token.add_grant(video_grant)

        response_data = json.dumps({
            'status': 'success',
            'message': 'Token retrieved successfully',
            'token': token.to_jwt(),
            'room_name': room_name
        })
        return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def video_conference_api(request):
    """
    Get video conference room info

    Args:
        request(Django): Django request parameter.

    Return:
        Reponse: Room info for connections.
    """
    if request.method == 'GET':
        body = json.loads(request.body)
        serializer = GetAssessmentInfoSerializer(data=body)
        
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors),
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        assessment_id = validated_data.get('assessment_id')

        assessment = Assessment.objects.filter(
            id=assessment_id
        )

        if not assessment.exists():
            response_data = json.dumps({
                'status': 'error',
                'message': 'Assessment not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        try:
            twilio_room = TwilioRoom.objects.get(assessment_id=assessment_id)
        except TwilioRoom.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Room not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        room_serializer = TwilioRoomModelSerializer(twilio_room)

        response_data = json.dumps({
            'status': 'success',
            'message': 'Room info retrieved successfully',
            'data': room_serializer.data
        })
        return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def mark_event_complete_api(request):
    """
    Get video conference room as complete to remove access to the room.

    Args:
        request(Django): Django request parameter.

    Return:
        Reponse: Room complete status for connections.
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = GetRoomSerializer(data=body)
        
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors),
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        twilio_room_id = validated_data.get('room_id')

        try:
            twilio_room = TwilioRoom.objects.get(id=twilio_room_id)
        except TwilioRoom.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Room not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        try:
            twilio_recording = TwilioRecording.objects.get(twilio_room_id=twilio_room_id)
        except TwilioRecording.DoesNotExist:
            twilio_room.room_status = constants.COMPLETE
            twilio_room.save()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Room completed successfully',
            })
            return Response(data=response_data, status=status.HTTP_200_OK)

        try:
            client = CL(config('ACCOUNT_SID'), config('AUTH_TOKEN'))
            client.video.recordings(twilio_recording.recording_sid).update(status='completed')
            twilio_room.room_status = constants.COMPLETE
            twilio_room.save()

        except twilio.base.exceptions.TwilioRestException:
            twilio_room.room_status = constants.COMPLETE
            twilio_room.save()

        finally:

            response_data = json.dumps({
                'status': 'success',
                'message': 'Room completed successfully',
            })
            return Response(data=response_data, status=status.HTTP_200_OK)

        
@api_view(['POST'])
def recording_to_s3_api(request):
    """
    Send recording of conference to S3.

    Args:
        request(Django): Django request parameter.

    Return:
        Reponse: Room recordings. 
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = GetRoomSerializer(data=body)
        
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors),
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        twilio_room_id = validated_data.get('room_id')

        try:
            twilio_room = TwilioRoom.objects.get(id=twilio_room_id)
        except TwilioRoom.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': 'Room not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        room_sid = twilio_room.room_sid

        try:
            client = CL(config('ACCOUNT_SID'), config('AUTH_TOKEN'))
            recordings = client.video \
                   .v1 \
                   .rooms(room_sid) \
                   .recordings \
                   .list(limit=20)

            recording_sid = ''

            for recording in recordings:
                if recording.status == 'completed':
                    recording_sid = recording.sid            


            if recording_sid == '':
                response_data = json.dumps({
                    'status': 'success',
                    'message': 'No recordings found'
                })
                return Response(data=response_data, status=status.HTTP_200_OK)

            chosen_recording = client.video.recordings(recording_sid).fetch()
            recording_buffer = io.BytesIO(chosen_recording.content)
            file_name = f'assessment_{twilio_room.assessment.id}/recordings/recording_{recording_sid}.mp4'
            file_path = upload_to_s3(
                file=recording_buffer,
                file_name=file_name
            )
            TwilioRecording.objects.update_or_create(
                twilio_room_id = twilio_room.id,
                defaults={
                    'recording_sid' : recording_sid,
                    'recording_url' : file_path
                }
            )
            recording_buffer.close()
            recording_path = open_s3_file(
                filepath=file_path
            )
            response_data = json.dumps({
                'status': 'success',
                'message': 'Recording uploaded successfully',
                'data': recording_path
            })
            return Response(data=response_data, status=status.HTTP_200_OK)

        except twilio.base.exceptions.TwilioRestException as e:
            response_data = json.dumps({
                'status': 'error',
                'message': f"Twilio error: {e}"
            })
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response_data = json.dumps({
                'status': 'error',
                'message': f"Error: {e}"
            })
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        