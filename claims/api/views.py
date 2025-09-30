"""
Claim api views containing all the api functions
The following api is stored here:

"""
import json
import pandas as pd
from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from application.models import InsuranceProvider
from claims.api.serializers import EditClaimApplicationSerializer
from claims.api.serializers import (
    EditClientApplicationSerialize,
    EditBusinessApplicationSerializer,
    EditClaimApplicationSerializer
)
import system_management.constants as constants
from system_management.models import User
from system_management.api.serializers import (
    UserModelSerializer,
    UserSerializer
)
from system_management.amazons3 import delete_s3_file
from claims.models import (
    WhatCategory,
    CauseCategory,
    HowCategory,
    ApplicationHow,
    ApplicationWhat,
    ApplicationCause,
    HowQuestionTitle,
    HowQuestionOption,
    HowQuestion,
    HowQuestionAnswer,
    WhatQuestionTitle,
    WhatQuestionOption,
    WhatQuestion,
    WhatQuestionAnswer,
    Claim
)

from surveys.api.serializers import (
    ApplicationClientModelSerializer
)

from claims.api.serializers import (
    AddClientSerializer,
    AddBusinessSerializer,
    EditHowCategorySerializer,
    EditWhatCategorySerializer,
    EditCauseCategorySerializer,
    AddHowCategorySerializer,
    AddWhatCategorySerializer,
    AddCauseCategorySerializer,
    CauseCategoryModelSerializer,
    HowCategoryModelSerializer,
    WhatCategoryModelSerializer,
    ManageApplicationSerializer,
    ApplicationTypeModelSerializer,
    ChangeApplicationTypeSerializer,
    ApplicationTypeCategoriesSerializer,
    AssignCauseApplicationSerializer,
    AssignHowApplicationSerializer,
    AssignWhatApplicationSerializer,
    TitleAddSerializer,
    CreateTitleQuestionSerializer,
    CategoryIdSerializer,
    HowQuestionTitleModelSerializer,
    HowQuestionAnswerModelSerializer,
    HowQuestionOptionModelSerializer,
    HowQuestionModelSerializer,
    WhatQuestionTitleModelSerializer,
    WhatQuestionOptionModelSerializer,
    WhatQuestionAnswerModelSerializer,
    WhatQuestionModelSerializer,
    GetClaimQuestionsSerializer,
    ClaimSaveQuestionSerializer,
    EditTitleSerializer,
    DeleteTitleSerializer,
    EditTitleQuestionSerializer,
    DeleteQuestionSerializer,
    WhatQuestionTitleSerializer,
    HowQuestionTitleSerializer,
    GenerateReportClaimSerializer,
    ApplicationClaimModelSerializer,
    ClaimModelSerializer,
    ClaimApplicationSerializer
)

from application.models import (
    Client,
    ClientIncident,
    Business,
    Application,
    ApplicationType,
    ApplicationStatus
)
from claims.api.services import (
    application_link_data,
    get_claim_info_service,
    get_preview_report_info,
    get_claim_categories
)


@api_view(['GET'])
def get_claim_application_api(request):
    """
    Get claim application api for the collection fo all data

    :param request:
        Django request parameter.
    :return:
        Api response with status code and call status. 
    """
    if request.method == "GET":
        body = json.loads(request.body)
        serializer = ClaimApplicationSerializer(data=body)

        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        claim_id = validated_data.get('claim_id')

        claim = Claim.objects.filter(id=claim_id)
        if not claim.exists():
            response_data = json.dumps({
                'status': 'error',
                'message': f"Claim with id: {claim_id} does not exist"
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        claim_serializer = ClaimModelSerializer(claim, many=True)
        df_claim = pd.DataFrame(claim_serializer.data)
        df_claim = get_claim_info_service(df_claim)
        categories = get_claim_categories(df_claim)

        application_types = ApplicationType.objects.values(
            'id',
            'name'
        )

        type_serializer = ApplicationTypeModelSerializer(application_types, many=True)

        response_data = json.dumps({
            'status': 'success',
            'message': f"Claim data send for claim with id: {claim_id}",
            'data': df_claim.to_dict('records')[0],
            'application_types': type_serializer.data,
            'categories': categories
        })

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def manage_application_api(request):
    """
    Manage Application API for the collection of all data

    :param request:
        Django request parameter.
    :return:
        Api response with status code and call status. 
    """
    if request.method == "GET":
        body = json.loads(request.body)
        serializer = ManageApplicationSerializer(data=body)
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        application_id = validated_data.get('application_id')

        try:
            application = Application.objects.get(id=application_id)

        except Application.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': f"Application with id: {application_id} does not exist"
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = ApplicationClaimModelSerializer(application)

        claims = Claim.objects.filter(
            application_id=application_id
        )
        claim_serializer = ClaimModelSerializer(claims, many=True)
        data = {
            "current_application": serializer.data,
            "claims": claim_serializer.data
        }

        response_data = json.dumps({
            'status': 'success',
            'message': f"Application data send for application with id: {application_id}",
            'data': data
        })
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def application_type_categories_api(request):
    """
    Get categories for claim based on application type.

    """
    if request.method == "GET":
        body = json.loads(request.body)
        serializer = ApplicationTypeCategoriesSerializer(data=body)

        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        application_type = validated_data.get('application_type')

        application_type = ApplicationType.objects.filter(id=application_type).values(
            'id',
            'name'
        )

        if not application_type.exists():
            data = json.dumps({
                "status": "error",
                "message": f"Application type with id: {application_type} not found"
            })
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        df_types = pd.DataFrame(application_type)
        application_type_data = application_link_data(df_types)

        data = {
            'claim_info': application_type_data.to_dict('records')[0]
        }

        data = json.dumps({
            "status": "success",
            "message": "Retrieve application categories successful.",
            "data": data
        })

        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_claim_info_api(request):
    """
    Collect all data for claim application management 
    """
    if request.method == "GET":
        assessors = list(User.objects.filter(
            user_type__name=constants.ASSESSOR
        ).values(
            'id',
            'first_name',
            'last_name'
        ))

        statuses = list(ApplicationStatus.objects.values(
            'id',
            'name'
        ))

        insurance_provider = list(InsuranceProvider.objects.values(
            'id',
            'insurance_name'
        ))

        application_types = ApplicationType.objects.all()
        type_serializer = ApplicationTypeModelSerializer(application_types, many=True)

        data = {
            'insurance_provider': insurance_provider,
            'assessors': assessors,
            'statuses': statuses,
            'application_types': type_serializer.data
        }

        data = json.dumps({
            "status": "success",
            "message": "Retrieve application categories successful.",
            "data": data,
        })

        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_sub_claim_api(request):
    """
    This function is used to add a survey client
    :param request:
        request django parameter
    :return:
        status and message stating success or error

    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = ChangeApplicationTypeSerializer(data=body)

        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        application_id = validated_data.get('application_id')
        application_type_id = validated_data.get('application_type')

        try:
            application = Application.objects.get(id=application_id)

        except Application.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': f"Application with id: {application_id} does not exist"
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        try:
            application_type = ApplicationType.objects.get(id=application_type_id)

        except ApplicationType.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': f"Application type with id: {application_type_id} does not exist"
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        claim = Claim.objects.create(
            application_id=application.id,
            application_type_id=application_type.id,
        )
        serializer = ClaimModelSerializer(claim)
        serializer.data

        claims = Claim.objects.filter(
            application_id=application.id,
        )

        claim_serializer = ClaimModelSerializer(claims, many=True)
        df_claim = pd.DataFrame(claim_serializer.data)
        df_claim = df_claim.loc[
            df_claim['id'] == claim.id
            ]
        categories = get_claim_categories(df_claim)

        application_types = ApplicationType.objects.values(
            'id',
            'name'
        )
        type_serializer = ApplicationTypeModelSerializer(application_types, many=True)

        data = {
            'claim': serializer.data,
            'claim_categories': categories,
            'claim_selection': claim_serializer.data,
            'application_types': type_serializer.data
        }

        response_data = json.dumps({
            "status": "success",
            "message": "Sub claim created successfully.",
            "data": data,
        })

        return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_claim_client_api(request):
    """
    This function is used to add a survey client

    :param request:
        request django parameter
    :return:
        status and message stating success or error

    """
    if request.method == "POST":
        body = json.loads(request.body)
        incident_date = body.get('incident_date')

        if incident_date is None:
            data = json.dumps({
                "status": "error",
                "message": "Incident date is required."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        incident_date = make_aware(datetime.strptime(incident_date, '%Y-%m-%dT%H:%M'))
        body['incident_date'] = incident_date
        serializer = AddClientSerializer(data=body)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            last_name = serializer.validated_data.get('last_name')
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')
            insurer_id = serializer.validated_data.get('insurer_id')
            id_number = serializer.validated_data.get('id_number')
            policy_number = serializer.validated_data.get('policy_number')

            incident_date = serializer.validated_data.get('incident_date')
            incident_location = serializer.validated_data.get('incident_location')
            incident_city = serializer.validated_data.get('incident_city')
            incident_province = serializer.validated_data.get('incident_province')
            incident_postal = serializer.validated_data.get('incident_postal')

            client = Client.objects.create(
                first_name=name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                insurer_id=insurer_id,
                id_number=id_number,
                policy_no=policy_number
            )

            client_id = client.id

            ClientIncident.objects.create(
                date_of_incident=incident_date,
                street_address=incident_location,
                city=incident_city,
                province=incident_province,
                postal_code=incident_postal,
                client_id=client_id
            )

            data = json.dumps({
                "status": "success",
                "message": "Client information added successfully.",
                "data": client_id
            })
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def add_claim_business_api(request):
    """
    Client business info api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        business_serializer = AddBusinessSerializer(data=body)

        if business_serializer.is_valid():
            client_id = business_serializer.validated_data.get('client_id')
            business_name = business_serializer.validated_data.get('business_name')
            business_reg_number = business_serializer.validated_data.get('business_reg_number')
            business_vat_number = business_serializer.validated_data.get('business_vat_number')
            business_email = business_serializer.validated_data.get('business_email')
            business_phone_number = business_serializer.validated_data.get('business_phone_number')

            Business.objects.create(
                client_id=client_id,
                business_name=business_name,
                business_email=business_email,
                reg_number=business_reg_number,
                vat_number=business_vat_number,
                phone_no=business_phone_number
            )

            data = json.dumps({
                "status": "success",
                "message": "Client information added successfully."
            })
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            data = json.dumps({
                "status": "error",
                "message": str(business_serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def add_what_category_api(request):
    """
    Add what category api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = AddWhatCategorySerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        category = validated_data.get('category')
        cause_id = validated_data.get('cause_id')

        try:
            cause_object = CauseCategory.objects.get(id=cause_id)

        except CauseCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Cause id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        WhatCategory.objects.create(
            name=category,
            cause_id=cause_object.id
        )

        what_objects = WhatCategory.objects.filter(cause_id=cause_id)
        serializer = WhatCategoryModelSerializer(what_objects, many=True)

        data = json.dumps({
            "status": "success",
            "message": "What category added successfully.",
            "data": serializer.data
        })

        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def edit_what_category_api(request):
    """
    Edit what category api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = EditWhatCategorySerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        category = validated_data.get('category')
        cause_id = validated_data.get('cause_id')
        what_id = validated_data.get('what_id')

        try:
            what_object = WhatCategory.objects.get(id=what_id)

        except WhatCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "What id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            cause_object = CauseCategory.objects.get(id=cause_id)

        except CauseCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Cause id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        what_object.name = category
        what_object.cause_id = cause_object.id
        what_object.save()

        what_objects = WhatCategory.objects.filter(cause_id=cause_id)
        serializer = WhatCategoryModelSerializer(what_objects, many=True)

        data = json.dumps({
            "status": "success",
            "message": "What category edited successfully.",
            "data": serializer.data
        })

        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def del_what_category_api(request):
    """
    Delete what category api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        what_id = body.get('what_id')

        if what_id is None:
            data = json.dumps({
                "status": "error",
                "message": "What id is required."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            what_object = WhatCategory.objects.get(id=what_id)

        except WhatCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "What id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        cause_id = what_object.cause_id
        what_object.delete()

        what_objects = WhatCategory.objects.filter(cause_id=cause_id)
        serializer = WhatCategoryModelSerializer(what_objects, many=True)

        data = json.dumps({
            "status": "success",
            "message": "What category deleted successfully.",
            "data": serializer.data
        })

        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def add_how_category_api(request):
    """
    Add how category api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = AddHowCategorySerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        category = validated_data.get('category')
        cause_id = validated_data.get('cause_id')

        try:
            cause_object = CauseCategory.objects.get(id=cause_id)

        except CauseCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Cause id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        HowCategory.objects.create(
            name=category,
            cause_id=cause_object.id
        )

        how_objects = HowCategory.objects.filter(cause_id=cause_object.id)
        serializer = HowCategoryModelSerializer(how_objects, many=True)

        data = json.dumps({
            "status": "success",
            "message": "'How' category added successfully.",
            "data": serializer.data
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def edit_how_category_api(request):
    """
    Edit how category api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = EditHowCategorySerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        category = validated_data.get('category')
        cause_id = validated_data.get('cause_id')
        how_id = validated_data.get('how_id')

        try:
            how_object = HowCategory.objects.get(id=how_id)

        except HowCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "How id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            cause_object = CauseCategory.objects.get(id=cause_id)

        except CauseCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Cause id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        how_object.name = category
        how_object.cause_id = cause_object.id
        how_object.save()

        how_objects = HowCategory.objects.filter(cause_id=cause_object.id)
        serializer = HowCategoryModelSerializer(how_objects, many=True)

        data = json.dumps({
            "status": "success",
            "message": "How category edited successfully.",
            "data": serializer.data
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def del_how_category_api(request):
    """
    Delete how category api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        how_id = body.get('how_id')

        if how_id is None:
            data = json.dumps({
                "status": "error",
                "message": "How id is required."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            how_object = HowCategory.objects.get(id=how_id)

        except HowCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "How id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        cause_id = how_object.cause_id
        how_object.delete()

        how_objects = HowCategory.objects.filter(cause_id=cause_id)
        serializer = HowCategoryModelSerializer(how_objects, many=True)

        data = json.dumps({
            "status": "success",
            "message": "How category deleted successfully.",
            "data": serializer.data
        })

        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def add_cause_category_api(request):
    """
    Add cause category api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = AddCauseCategorySerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        category = validated_data.get('category')
        application_type = validated_data.get('application_type')

        if CauseCategory.objects.filter(application_type=application_type).exists():
            data = json.dumps({
                'status': "error",
                'message': f"Cause category with name {category} already exists."
            })
            return Response(data, status.HTTP_400_BAD_REQUEST)

        try:
            application_type_obj = ApplicationType.objects.get(id=application_type)

        except ApplicationType.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": f"Application type with id: {application_type} not found",
            })
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        CauseCategory.objects.create(
            name=category,
            application_type_id=application_type_obj.id
        )

        cause_objects = CauseCategory.objects.filter(
            application_type_id=application_type_obj.id
        )
        serializer = CauseCategoryModelSerializer(cause_objects, many=True)

        data = json.dumps({
            "status": "success",
            "message": "'Cause' category added successfully.",
            "data": serializer.data
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def edit_cause_category_api(request):
    """
    Edit cause category api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = EditCauseCategorySerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        category = validated_data.get('category')
        cause_id = validated_data.get('cause_id')

        try:
            cause_object = CauseCategory.objects.get(id=cause_id)

        except CauseCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Cause id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        cause_object.name = category
        cause_object.save()

        cause_objects = CauseCategory.objects.all()
        serializer = CauseCategoryModelSerializer(cause_objects, many=True)

        data = json.dumps({
            "status": "success",
            "message": "Cause category edited successfully.",
            "data": serializer.data
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def del_cause_category_api(request):
    """
    Delete cause category api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        cause_id = body.get('cause_id')

        if cause_id is None:
            data = json.dumps({
                "status": "error",
                "message": "Cause id is required."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            cause_object = CauseCategory.objects.get(id=cause_id)

        except CauseCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Cause id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        cause_object.delete()

        cause_objects = CauseCategory.objects.all()
        serializer = CauseCategoryModelSerializer(cause_objects, many=True)

        data = json.dumps({
            "status": "success",
            "message": "Cause category deleted successfully.",
            "data": serializer.data
        })

        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def edit_client_application_api(request):
    """
    Edit client application api.
    :param request:
    :return:
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = EditClientApplicationSerialize(data=body)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            client_id = validated_data['client_id']
            first_name = validated_data['first_name']
            last_name = validated_data['last_name']
            email = validated_data['email']
            id_number = validated_data['id_number']
            phone_number = validated_data['phone_number']

            Client.objects.filter(id=client_id).update(first_name=first_name,
                                                       last_name=last_name,
                                                       email=email,
                                                       id_number=id_number,
                                                       phone_number=phone_number
                                                       )
            response_data = json.dumps({
                "status": "success",
                "message": "Client application edited successfully."
            })
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_business_application_api(request):
    """
    Edit business application api.
    :param request:
    :return:
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = EditBusinessApplicationSerializer(data=body)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            client_id = validated_data['client_id']
            business_name = validated_data['business_name']
            business_email = validated_data['business_email']
            reg_number = validated_data['reg_number']
            vat_number = validated_data['vat_number']
            phone_no = validated_data['phone_no']

            Business.objects.filter(id=client_id).update(business_name=business_name,
                                                         business_email=business_email,
                                                         reg_number=reg_number,
                                                         vat_number=vat_number,
                                                         phone_no=phone_no
                                                         )

            response_data = json.dumps({
                "status": "success",
                "message": "Business application edited successfully."
            })
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_claim_application_api(request):
    """
    Edit business application api.
    :param request:
    :return:
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = EditClaimApplicationSerializer(data=body)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            client_id = validated_data['client_id']
            insurance_id = validated_data['insurance_id']

            policy_no = validated_data['policy_no']
            street_address = validated_data['street_address']
            city = validated_data['city']
            postal_code = validated_data['postal_code']

            ClientIncident.objects.filter(client_id=client_id).update(
                street_address=street_address,
                city=city,
                postal_code=postal_code
            )
            Client.objects.filter(id=client_id).update(
                insurer_id=insurance_id,
                policy_no=policy_no

            )

            response_data = json.dumps({
                "status": "success",
                "message": "Claim application edited successfully."
            })
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_claim_categories_api(request):
    """
    API for the collection of all claim categories.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "GET":
        application_type = ApplicationType.objects.all()

        try:
            type_serializer = ApplicationTypeModelSerializer(application_type, many=True)

        except KeyError:
            data = json.dumps({
                "status": "error",
                "message": "Key Error during application type serializer data"
            })
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        what_categories = WhatCategory.objects.all()

        try:
            what_serializer = WhatCategoryModelSerializer(what_categories, many=True)

        except KeyError:
            data = json.dumps({
                "status": "error",
                "message": "Error during how category serializer data"
            })
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        how_categories = HowCategory.objects.all()

        try:
            how_serializer = HowCategoryModelSerializer(how_categories, many=True)

        except KeyError:
            data = json.dumps({
                "status": "error",
                "message": "Error during how category serializer data"
            })
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        cause_categories = CauseCategory.objects.all()

        try:
            cause_serializer = CauseCategoryModelSerializer(cause_categories, many=True)

        except KeyError:
            data = json.dumps({
                "status": "error",
                "message": "Error during serializer data"
            })
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {
            'how_categories': how_serializer.data,
            'what_categories': what_serializer.data,
            'cause_categories': cause_serializer.data,
            'application_types': type_serializer.data
        }

        data = json.dumps({
            "status": "success",
            "message": "Claim categories retrieved successfully.",
            "data": data
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_all_claims_api(request):
    """
    Get all claim applications information api

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "GET":
        claims_list = Claim.objects.values_list('application_id', flat=True)

        claim_applications = Application.objects.filter(
            id__in=claims_list
        )

        application_model_serializer = ApplicationClientModelSerializer(claim_applications,
                                                                        many=True)
        response_data = json.dumps({
            "status": "success",
            "message": "Claim data retrieved successfully!",
            "data": application_model_serializer.data
        })

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_assessors_api(request):
    """
    Get all available assessors for the assign to a claim.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "GET":
        assessors = User.objects.filter(user_type__name=constants.ASSESSOR)
        serializer = UserModelSerializer(assessors, many=True)

        response_data = json.dumps({
            "status": "success",
            "message": "Assessors retrieved successfully!",
            "data": serializer.data
        })

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def change_application_type_api(request):
    """
    Change application type api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)

        serializer = ChangeApplicationTypeSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": "Invalid data."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        application_id = validated_data.get('application_id')
        application_type = validated_data.get('application_type')

        try:
            application = Application.objects.get(id=application_id)

        except Application.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Application id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            application_type_obj = ApplicationType.objects.get(id=application_type)
        except Application.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Application id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        ApplicationWhat.objects.filter(application_id=application_id).delete()
        ApplicationHow.objects.filter(application_id=application_id).delete()
        ApplicationCause.objects.filter(application_id=application_id).delete()

        application.application_type_id = application_type_obj.id
        application.save()

        data = json.dumps({
            "status": "success",
            "message": "Application type changed successfully.",
            "data": application_type_obj.name
        })
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def assign_what_application_api(request):
    """
    Assign what application api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)

        serializer = AssignWhatApplicationSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": "Invalid data."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        claim_id = validated_data.get('claim_id')
        what_id = validated_data.get('what_id')

        try:
            application = Claim.objects.get(id=claim_id)

        except Claim.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Claim id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:

            what_object = WhatCategory.objects.get(id=what_id)

        except WhatCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "What category object id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not ApplicationWhat.objects.filter(claim_id=application.id).exists():
            ApplicationWhat.objects.create(
                claim_id=application.id,
                what_id=what_object.id
            )
        else:
            ApplicationWhat.objects.filter(claim_id=application.id).update(
                what_id=what_object.id
            )

        files = WhatQuestionAnswer.objects.filter(
            question_id__has_file=True,
            claim_id=application.id
        ).values_list('answer', flat=True)

        [
            delete_s3_file(file)
            for file in files
        ]

        WhatQuestionAnswer.objects.filter(
            claim_id=application.id
        ).delete()

        what_titles = WhatQuestionTitle.objects.filter(what_id=what_object.id)
        question_title_serializer = WhatQuestionTitleSerializer(what_titles, many=True)

        df_questions = pd.DataFrame(question_title_serializer.data)
        if not df_questions.empty:
            df_questions = df_questions.loc[
                (df_questions['questions'].astype(str) != '[]') &
                (df_questions['questions'] != '')
                ]

        questions = df_questions.to_dict('records')

        data = json.dumps({
            "status": "success",
            "message": "What category assigned to application successfully.",
            "data": what_object.name,
            'questions': questions
        })
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def assign_how_application_api(request):
    """
    Assign how application api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)

        serializer = AssignHowApplicationSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": "Invalid data."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        claim_id = validated_data.get('claim_id')
        how_id = validated_data.get('how_id')

        try:
            application = Claim.objects.get(id=claim_id)

        except Claim.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Claim id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:

            how_object = HowCategory.objects.get(id=how_id)

        except HowCategory.DoesNotExist:

            data = json.dumps({
                "status": "error",
                "message": "How category object id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not ApplicationHow.objects.filter(claim_id=application.id).exists():

            ApplicationHow.objects.create(
                claim_id=application.id,
                how_id=how_object.id
            )

        else:

            ApplicationHow.objects.filter(claim_id=application.id).update(
                how_id=how_object.id
            )

        files = HowQuestionAnswer.objects.filter(
            question_id__has_file=True,
            claim_id=application.id
        ).values_list('answer', flat=True)

        [
            delete_s3_file(file)
            for file in files
        ]

        HowQuestionAnswer.objects.filter(
            claim_id=application.id
        ).delete()

        how_titles = HowQuestionTitle.objects.filter(how_id=how_object.id)

        question_title_serializer = HowQuestionTitleSerializer(
            how_titles,
            many=True
        )

        df_questions = pd.DataFrame(question_title_serializer.data)
        if not df_questions.empty:
            df_questions = df_questions.loc[
                (df_questions['questions'].astype(str) != '[]') &
                (df_questions['questions'] != '')
                ]

        questions = df_questions.to_dict('records')

        data = json.dumps({
            "status": "success",
            "message": "How category assigned to application successfully.",
            "data": how_object.name,
            "questions": questions
        })
        return Response(data=data, status=status.HTTP_200_OK)


def filter_answers(df_questions: pd.DataFrame, application_id: int):
    """
    Filter the answers for the questions.

    :param df_questions:
        Dataframe of the questions.

    :param application_id:
        Application id for current application.

    :return:
        Dictionary list of the questions with the answers.
    """

    if not df_questions.empty:
        df_questions['answers'] = df_questions['answers'].apply(
            lambda answers:
            pd.DataFrame(answers).loc[['application_id'] == application_id]
            if str(answers) != '[]' and answers != ''
            else
            []
        )

    questions = df_questions.to_dict('records')
    return questions


@api_view(['POST'])
def assign_cause_application_api(request):
    """
    Assign cause application api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)

        serializer = AssignCauseApplicationSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        claim_id = validated_data.get('claim_id')
        cause_id = validated_data.get('cause_id')

        try:
            application = Claim.objects.get(id=claim_id)

        except Claim.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Claim application object does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:

            cause_object = CauseCategory.objects.get(id=cause_id)

        except CauseCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Cause category object id does not exist."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not ApplicationCause.objects.filter(claim_id=application.id).exists():
            ApplicationCause.objects.create(
                claim_id=application.id,
                cause_id=cause_object.id
            )
        else:
            ApplicationCause.objects.filter(claim_id=application.id).update(
                cause_id=cause_object.id
            )

        ApplicationHow.objects.filter(
            claim_id=application.id
        ).delete()

        files = HowQuestionAnswer.objects.filter(
            question_id__has_file=True,
            claim_id=application.id
        ).values_list('answer', flat=True)

        [
            delete_s3_file(file)
            for file in files
        ]

        HowQuestionAnswer.objects.filter(
            claim_id=application.id
        ).delete()

        ApplicationWhat.objects.filter(
            claim_id=application.id
        ).delete()

        files = WhatQuestionAnswer.objects.filter(
            question_id__has_file=True,
            claim_id=application.id
        ).values_list('answer', flat=True)

        [
            delete_s3_file(file)
            for file in files
        ]

        WhatQuestionAnswer.objects.filter(
            claim_id=application.id
        ).delete()

        data = json.dumps({
            "status": "success",
            "message": "Cause category assigned to application successfully.",
            "data": cause_object.name
        })
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_how_title_api(request):
    """
    Create how title api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = TitleAddSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        how_id = validated_data.get('category_id')
        title = validated_data.get('title')

        title_object = HowQuestionTitle.objects.create(
            title=title,
            how_id=how_id
        )
        data = {
            'id': title_object.id,
            'title': title_object.title,
            'how_id': title_object.how_id
        }
        response_data = json.dumps({
            "status": "success",
            "message": "How title created successfully.",
            "data": data
        })

        return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_what_title_api(request):
    """
    Create what title api.

    :param request:
        Django request parameter

    :return:
        status and message stating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = TitleAddSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        what_id = validated_data.get('category_id')
        title = validated_data.get('title')

        title_object = WhatQuestionTitle.objects.create(
            title=title,
            what_id=what_id
        )
        data = {
            'id': title_object.id,
            'title': title_object.title,
            'what_id': title_object.what_id
        }
        response_data = json.dumps({
            "status": "success",
            "message": "What title created successfully.",
            "data": data
        })

        return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_question_how_api(request):
    """
    Create question api for how category.

    :param request:
        Django Request parameter.
    :return:
        Question created successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        question_serializer = CreateTitleQuestionSerializer(data=body)

        if question_serializer.is_valid():
            title_id = question_serializer.validated_data.get('title_id')
            question = question_serializer.validated_data.get('question')
            question_type = question_serializer.validated_data.get('question_type')
            question_option = question_serializer.validated_data.get('options')
            is_mandatory = question_serializer.validated_data.get('is_mandatory')
            has_other_field = question_serializer.validated_data.get('has_other_field')

            has_checkbox = False
            has_selection = False
            has_text = False
            has_date = False
            has_file = False
            has_location = False
            has_options = False

            if question_type == "checkbox":
                has_checkbox = True
                has_options = True

            elif question_type == "date":
                has_date = True

            elif question_type == "file":
                has_file = True

            elif question_type == "location":
                has_location = True

            elif question_type == "selection":
                has_selection = True
                has_options = True

            elif question_type == "text":
                has_text = True

            else:
                data = json.dumps({
                    'status': 'error',
                    'message': 'Invalid question type'
                })
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            question_object = HowQuestion.objects.create(
                how_title_id=title_id,
                question=question,
                question_type=question_type,
                has_other_field=has_other_field,
                is_mandatory=is_mandatory,
                has_checkbox=has_checkbox,
                has_selection=has_selection,
                has_text=has_text,
                has_date=has_date,
                has_file=has_file,
                has_location=has_location
            )

            if has_options:
                question_id = question_object.id

                bulk_options = [
                    HowQuestionOption(
                        question_id=question_id,
                        option=option
                    )
                    for option in question_option
                ]

                HowQuestionOption.objects.bulk_create(bulk_options)

            data = {
                'id': question_object.id,
                'question': question_object.question,
                'question_type': question_object.question_type,
                'has_other_field': question_object.has_other_field,
                'is_mandatory': question_object.is_mandatory,
            }

            data = json.dumps({
                'status': 'success',
                'message': 'Question created successfully',
                'data': data
            })
            return Response(data, status=status.HTTP_200_OK)

        else:
            data = json.dumps({
                'status': 'error',
                'message': str(question_serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    else:
        data = ({
            'status': 'error',
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def create_question_what_api(request):
    """
    Create question api for what category.

    :param request:
        Django Request parameter.
    :return:
        Question created successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        question_serializer = CreateTitleQuestionSerializer(data=body)

        if question_serializer.is_valid():
            title_id = question_serializer.validated_data.get('title_id')
            question = question_serializer.validated_data.get('question')
            question_type = question_serializer.validated_data.get('question_type')
            question_option = question_serializer.validated_data.get('options')
            is_mandatory = question_serializer.validated_data.get('is_mandatory')
            has_other_field = question_serializer.validated_data.get('has_other_field')

            has_checkbox = False
            has_selection = False
            has_text = False
            has_date = False
            has_file = False
            has_location = False
            has_options = False

            if question_type == "checkbox":
                has_checkbox = True
                has_options = True

            elif question_type == "date":
                has_date = True

            elif question_type == "file":
                has_file = True

            elif question_type == "location":
                has_location = True

            elif question_type == "selection":
                has_selection = True
                has_options = True

            elif question_type == "text":
                has_text = True

            else:
                data = json.dumps({
                    'status': 'error',
                    'message': 'Invalid question type'
                })
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            question_object = WhatQuestion.objects.create(
                what_title_id=title_id,
                question=question,
                question_type=question_type,
                has_other_field=has_other_field,
                is_mandatory=is_mandatory,
                has_checkbox=has_checkbox,
                has_selection=has_selection,
                has_text=has_text,
                has_date=has_date,
                has_file=has_file,
                has_location=has_location
            )

            if has_options:
                question_id = question_object.id

                bulk_options = [
                    WhatQuestionOption(
                        question_id=question_id,
                        option=option
                    )
                    for option in question_option
                ]

                WhatQuestionOption.objects.bulk_create(bulk_options)

            data = {
                'id': question_object.id,
                'question': question_object.question,
                'question_type': question_object.question_type,
                'has_other_field': question_object.has_other_field,
                'is_mandatory': question_object.is_mandatory,
            }

            data = json.dumps({
                'status': 'success',
                'message': 'Question created successfully',
                'data': data
            })
            return Response(data, status=status.HTTP_200_OK)

        else:
            data = json.dumps({
                'status': 'error',
                'message': str(question_serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    else:
        data = ({
            'status': 'error',
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def how_category_questions_api(request):
    """
    Get all questions for how category.

    :param request:
        Django Request parameter.
    :return:
        All questions for how category.
    """
    if request.method == "GET":
        body = json.loads(request.body)
        serializer = CategoryIdSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.data)
            })
            return Response(data, status=status.HTTP_200_OK)

        validated_data = serializer.validated_data
        category_id = validated_data.get('category_id')

        try:
            how_object = HowCategory.objects.get(id=category_id)

        except HowCategory.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message': 'How category not found.'
            })
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        question_titles = HowQuestionTitle.objects.filter(
            how_id=category_id
        )

        title_serializer = HowQuestionTitleModelSerializer(question_titles, many=True)
        df_titles = pd.DataFrame(title_serializer.data)

        if not df_titles.empty:
            title_ids = df_titles['id'].values.tolist()

            questions = HowQuestion.objects.filter(
                how_title_id__in=title_ids
            )

            question_serializer = HowQuestionModelSerializer(questions, many=True)
            df_questions = pd.DataFrame(question_serializer.data)

            if not df_questions.empty:
                options = HowQuestionOption.objects.filter(
                    question_id__in=df_questions['id'].values.tolist()
                )

                option_serializer = HowQuestionOptionModelSerializer(options, many=True)
                df_options = pd.DataFrame(option_serializer.data)

                if not df_options.empty:
                    df_questions['options'] = df_questions.apply(
                        lambda series:
                        df_options.loc[
                            df_options['question_id'] == series['id']
                            ].to_dict('records'), axis=1)

                answer = HowQuestionAnswer.objects.filter(
                    question_id__in=df_questions['id'].values.tolist()
                )

                answer_serializer = HowQuestionAnswerModelSerializer(answer, many=True)
                df_answers = pd.DataFrame(answer_serializer.data)

                if not df_answers.empty:
                    df_questions['answers'] = df_questions.apply(
                        lambda series:
                        df_answers.loc[
                            df_answers['question_id'] == series['id']
                            ].to_dict('records'), axis=1)

                df_titles['questions'] = df_titles.apply(
                    lambda series:
                    df_questions.loc[
                        df_questions['how_title_id'] == series['id']
                        ].to_dict('records'), axis=1)

        question_titles = df_titles.to_dict('records')

        data = json.dumps({
            'status': 'success',
            'message': 'All questions for how category.',
            'data': question_titles,
            'how_category': how_object.name
        })
        return Response(data, status=status.HTTP_200_OK)

    else:
        data = ({
            'status': 'error',
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def what_category_questions_api(request):
    """
    Get all questions for what category.

    :param request:
        Django Request parameter.
    :return:
        All questions for what category.
    """
    if request.method == "GET":
        body = json.loads(request.body)
        serializer = CategoryIdSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.data)
            })
            return Response(data, status=status.HTTP_200_OK)

        validated_data = serializer.validated_data
        category_id = validated_data.get('category_id')

        try:
            what_object = WhatCategory.objects.get(id=category_id)
        except WhatCategory.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message': 'What category not found.'
            })
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        question_titles = WhatQuestionTitle.objects.filter(
            what_id=category_id
        )

        title_serializer = WhatQuestionTitleModelSerializer(question_titles, many=True)
        df_titles = pd.DataFrame(title_serializer.data)

        if not df_titles.empty:

            title_ids = df_titles['id'].values.tolist()

            questions = WhatQuestion.objects.filter(
                what_title_id__in=title_ids
            )

            question_serializer = WhatQuestionModelSerializer(questions, many=True)
            df_questions = pd.DataFrame(question_serializer.data)

            if not df_questions.empty:
                options = WhatQuestionOption.objects.filter(
                    question_id__in=df_questions['id'].values.tolist()
                )

                option_serializer = WhatQuestionOptionModelSerializer(options, many=True)
                df_options = pd.DataFrame(option_serializer.data)

                if not df_options.empty:
                    df_questions['options'] = df_questions.apply(
                        lambda series:
                        df_options.loc[
                            df_options['question_id'] == series['id']
                            ].to_dict('records'), axis=1)

                answer = WhatQuestionAnswer.objects.filter(
                    question_id__in=df_questions['id'].values.tolist()
                )
                answer_serializer = WhatQuestionAnswerModelSerializer(answer, many=True)
                df_answers = pd.DataFrame(answer_serializer.data)

                if not df_answers.empty:
                    df_questions['answers'] = df_questions.apply(
                        lambda series:
                        df_answers.loc[
                            df_answers['question_id'] == series['id']
                            ].to_dict('records'), axis=1)

                df_titles['questions'] = df_titles.apply(
                    lambda series:
                    df_questions.loc[
                        df_questions['what_title_id'] == series['id']
                        ].to_dict('records'), axis=1)

        question_titles = df_titles.to_dict('records')

        data = json.dumps({
            'status': 'success',
            'message': 'All questions for what category.',
            'data': question_titles,
            'what_category': what_object.name
        })
        return Response(data, status=status.HTTP_200_OK)

    else:
        data = ({
            'status': 'error',
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_claim_questions_api(request):
    """
    Api for the retrieval of what and how questions for application.

    :param request:
        Django request parameter.
    :return:
        List of records containing questions for application.
    """
    if request.method == "GET":
        body = json.loads(request.body)
        serializer = GetClaimQuestionsSerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        application_id = validated_data.get('application_id')
        what_id = validated_data.get('what_id')
        how_id = validated_data.get('how_id')

        if not HowCategory.objects.filter(id=how_id).exists():
            data = json.dumps({
                'status': 'error',
                'message': 'How category not found.'
            })
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if not WhatCategory.objects.filter(id=what_id).exists():
            data = json.dumps({
                'status': 'error',
                'message': 'What category not found.'
            })
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if not Application.objects.filter(id=application_id).exists():
            data = json.dumps({
                'status': 'error',
                'message': 'Application not found.'
            })
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        data = {
            'what_questions': get_what_questions(what_id, application_id),
            'how_questions': get_how_questions(how_id, application_id),
        }

        data = json.dumps({
            'status': 'success',
            'message': 'All questions for application.',
            'data': data
        })
        return Response(data, status=status.HTTP_200_OK)


def get_how_questions(category_id, application_id):
    """
    Get how questions for application.
    
    :param category_id:
        How category id.
    
    :param application_id:
        Current application id
    """

    question_titles = HowQuestionTitle.objects.filter(
        how_id=category_id
    )

    title_serializer = HowQuestionTitleModelSerializer(question_titles, many=True)
    df_titles = pd.DataFrame(title_serializer.data)
    df_titles = df_titles.assign(
        questions=''
    )
    if not df_titles.empty:
        title_ids = df_titles['id'].values.tolist()

        questions = HowQuestion.objects.filter(
            how_title_id__in=title_ids
        )

        question_serializer = HowQuestionModelSerializer(questions, many=True)
        df_questions = pd.DataFrame(question_serializer.data)
        df_questions = df_questions.assign(
            options='',
            answers=''
        )
        if not df_questions.empty:
            options = HowQuestionOption.objects.filter(
                question_id__in=df_questions['id'].values.tolist()
            )

            option_serializer = HowQuestionOptionModelSerializer(options, many=True)
            df_options = pd.DataFrame(option_serializer.data)

            if not df_options.empty:
                df_questions['options'] = df_questions['id'].apply(
                    lambda question_id:
                    df_options.loc[
                        df_options['question_id'] == question_id
                        ].to_dict('records')
                )

            answer = HowQuestionAnswer.objects.filter(
                question_id__in=df_questions['id'].values.tolist(),
                application_id=application_id
            )

            answer_serializer = HowQuestionAnswerModelSerializer(answer, many=True)
            df_answers = pd.DataFrame(answer_serializer.data)

            if not df_answers.empty:
                df_questions['answers'] = df_questions['id'].apply(
                    lambda question_id:
                    df_answers.loc[
                        df_answers['question_id'] == question_id
                        ].to_dict('records')
                )

            df_titles['questions'] = df_titles['id'].apply(
                lambda title_id:
                df_questions.loc[
                    df_questions['how_title_id'] == title_id
                    ].to_dict('records')
            )

        df_titles = df_titles.loc[
            (df_titles['questions'].astype(str) != '[]') &
            (df_titles['questions'] != '')
            ]

    question_titles = df_titles.to_dict('records')
    return question_titles


def get_what_questions(category_id, application_id):
    """Get what questions for application.
    
    :param category_id:
        How category id.
    
    :param application_id:
        Current application id
    """
    question_titles = WhatQuestionTitle.objects.filter(
        what_id=category_id
    )

    title_serializer = WhatQuestionTitleModelSerializer(question_titles, many=True)
    df_titles = pd.DataFrame(title_serializer.data)
    df_titles = df_titles.assign(
        questions=''
    )
    if not df_titles.empty:

        title_ids = df_titles['id'].values.tolist()

        questions = WhatQuestion.objects.filter(
            what_title_id__in=title_ids
        )

        question_serializer = WhatQuestionModelSerializer(questions, many=True)
        df_questions = pd.DataFrame(question_serializer.data)
        df_questions = df_questions.assign(
            options='',
            answers=''
        )
        if not df_questions.empty:
            options = WhatQuestionOption.objects.filter(
                question_id__in=df_questions['id'].values.tolist()
            )

            option_serializer = WhatQuestionOptionModelSerializer(options, many=True)
            df_options = pd.DataFrame(option_serializer.data)

            if not df_options.empty:
                df_questions['options'] = df_questions['id'].apply(
                    lambda question_id:
                    df_options.loc[
                        df_options['question_id'] == question_id
                        ].to_dict('records')
                )

            answer = WhatQuestionAnswer.objects.filter(
                question_id__in=df_questions['id'].values.tolist(),
                application_id=application_id
            )
            answer_serializer = WhatQuestionAnswerModelSerializer(answer, many=True)
            df_answers = pd.DataFrame(answer_serializer.data)

            if not df_answers.empty:
                df_questions['answers'] = df_questions['id'].apply(
                    lambda question_id:
                    df_answers.loc[
                        df_answers['question_id'] == question_id
                        ].to_dict('records')
                )

            df_titles['questions'] = df_titles['id'].apply(
                lambda title_id:
                df_questions.loc[
                    df_questions['what_title_id'] == title_id
                    ].to_dict('records')
            )

        df_titles = df_titles.loc[
            (df_titles['questions'].astype(str) != '[]') &
            (df_titles['questions'] != '')
            ]

    question_titles = df_titles.to_dict('records')
    return question_titles


@api_view(['POST'])
def save_claim_questions_api(request):
    """
    Save claim questions api for how and what questions.

    :param request:
        Django request parameter.
    :return:
        Response of saved question statuses.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = ClaimSaveQuestionSerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        claim_id = validated_data.get('claim_id')
        what_answers = validated_data.get('what_answers')
        how_answers = validated_data.get('how_answers')

        [
            create_what_question_instance(answer, claim_id)
            for answer in what_answers
        ]

        [
            create_how_question_instance(answer, claim_id)
            for answer in how_answers
        ]

        data = json.dumps({
            'status': 'success',
            'message': 'Questions saved successfully!'
        })
        return Response(data, status=status.HTTP_200_OK)


def create_how_question_instance(answer, claim_id):
    """
    Create question instance.

    :param answer:
        Survey answer.
    :param application_id:
        Application id.
    :return:
        Question instance.
    """
    question_id = answer['question_id']

    try:
        question = HowQuestion.objects.get(id=question_id)

    except HowQuestion.DoesNotExist:
        return None

    question_type = answer['question_type']
    answer_field = answer['answer']

    if question.has_other_field:
        survey_answer = HowQuestionAnswer.objects.filter(
            question_id=question_id,
            claim_id=claim_id
        ).values('id')

        if not survey_answer.exists():
            HowQuestionAnswer.objects.create(
                question_id=question.id,
                claim_id=claim_id,
                answer=answer_field
            )
        elif survey_answer.count() == 1:
            if question_type == 'other':

                HowQuestionAnswer.objects.create(
                    question_id=question.id,
                    claim_id=claim_id,
                    answer=answer_field
                )

            else:
                survey_answer = HowQuestionAnswer.objects.filter(
                    question_id=question_id,
                    claim_id=claim_id
                ).order_by('id').first()

                if survey_answer:
                    survey_answer.answer = answer_field
                    survey_answer.save()
        else:
            if question_type == 'other':
                survey_answer = HowQuestionAnswer.objects.filter(
                    question_id=question_id,
                    claim_id=claim_id
                ).order_by('id').last()

                if survey_answer:
                    survey_answer.answer = answer_field
                    survey_answer.save()
            else:
                survey_answer = HowQuestionAnswer.objects.filter(
                    question_id=question_id,
                    claim_id=claim_id
                ).order_by('id').first()

                if survey_answer:
                    survey_answer.answer = answer_field
                    survey_answer.save()

    else:
        if not HowQuestionAnswer.objects.filter(
                question_id=question_id,
                claim_id=claim_id
        ).exists():

            HowQuestionAnswer.objects.create(
                question_id=question.id,
                claim_id=claim_id,
                answer=answer_field
            )

        else:

            HowQuestionAnswer.objects.filter(
                question_id=question_id,
                claim_id=claim_id
            ).update(
                answer=answer_field
            )

    return None


def create_what_question_instance(answer, claim_id):
    """
    Create question instance.

    :param answer:
        Survey answer.
    :param application_id:
        Application id.
    :return:
        Question instance.
    """
    question_id = answer['question_id']

    try:
        question = WhatQuestion.objects.get(id=question_id)

    except WhatQuestion.DoesNotExist:
        return None

    question_type = answer['question_type']
    answer_field = answer['answer']

    if question.has_other_field:
        survey_answer = WhatQuestionAnswer.objects.filter(
            question_id=question_id,
            claim_id=claim_id
        ).values('id')

        if not survey_answer.exists():

            WhatQuestionAnswer.objects.create(
                question_id=question.id,
                claim_id=claim_id,
                answer=answer_field
            )

        elif survey_answer.count() == 1:
            if question_type == 'other':

                WhatQuestionAnswer.objects.create(
                    question_id=question.id,
                    claim_id=claim_id,
                    answer=answer_field
                )
            else:
                survey_answer = WhatQuestionAnswer.objects.filter(
                    question_id=question_id,
                    claim_id=claim_id
                ).order_by('id').first()

                if survey_answer:
                    survey_answer.answer = answer_field
                    survey_answer.save()
        else:
            if question_type == 'other':
                survey_answer = WhatQuestionAnswer.objects.filter(
                    question_id=question_id,
                    claim_id=claim_id
                ).order_by('id').last()

                if survey_answer:
                    survey_answer.answer = answer_field
                    survey_answer.save()
            else:
                survey_answer = WhatQuestionAnswer.objects.filter(
                    question_id=question_id,
                    claim_id=claim_id
                ).order_by('id').first()

                if survey_answer:
                    survey_answer.answer = answer_field
                    survey_answer.save()

    else:
        if not WhatQuestionAnswer.objects.filter(
                question_id=question_id,
                claim_id=claim_id
        ).exists():

            WhatQuestionAnswer.objects.create(
                question_id=question.id,
                claim_id=claim_id,
                answer=answer_field
            )

        else:

            WhatQuestionAnswer.objects.filter(
                question_id=question_id,
                claim_id=claim_id
            ).update(
                answer=answer_field
            )

    return None


@api_view(['POST'])
def edit_title_what_api(request):
    """
    Edit title what api.

    :param request:
        Django request parameter.
    :return:
        Response of edited title what.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = EditTitleSerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        title_id = validated_data.get('title_id')
        title_name = validated_data.get('title')

        title_what = WhatQuestionTitle.objects.get(id=title_id)
        title_what.title = title_name
        title_what.save()

        data = json.dumps({
            'status': 'success',
            'message': 'Title what edited successfully!'
        })
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_title_what_api(request):
    """
    Delete title what api.

    :param request:
        Django request parameter.
    :return:
        Response of deleted title what.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = DeleteTitleSerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        title_id = validated_data.get('title_id')

        try:
            title_what = WhatQuestionTitle.objects.get(id=title_id)

        except WhatQuestionTitle.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message': 'Title what does not exist!'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        questions = WhatQuestion.objects.filter(
            what_title_id=title_id
        ).values_list('id', flat=True)

        files = WhatQuestionAnswer.objects.filter(
            question_id__has_file=True,
            question_id__in=questions
        ).values_list('answer', flat=True)

        [
            delete_s3_file(file)
            for file in files
        ]

        WhatQuestionAnswer.objects.filter(
            question_id__in=questions
        ).delete()

        WhatQuestionOption.objects.filter(
            question_id__in=questions
        ).delete()

        WhatQuestion.objects.filter(
            what_title_id=title_id
        ).delete()

        title_what.delete()

        data = json.dumps({
            'status': 'success',
            'message': 'Title what deleted successfully!'
        })

        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def edit_title_how_api(request):
    """
    Edit title how api.

    :param request:
        Django request parameter.
    :return:
        Response of edited title what.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = EditTitleSerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        title_id = validated_data.get('title_id')
        title_name = validated_data.get('title')

        try:
            title_how = HowQuestionTitle.objects.get(id=title_id)

        except HowQuestionTitle.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message': 'Title how does not exist!'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        title_how.title = title_name
        title_how.save()

        data = json.dumps({
            'status': 'success',
            'message': 'Title how edited successfully!'
        })
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_title_how_api(request):
    """
    Delete title how api.

    :param request:
        Django request parameter.
    :return:
        Response of deleted title what.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = DeleteTitleSerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        title_id = validated_data.get('title_id')

        try:
            title_how = HowQuestionTitle.objects.get(id=title_id)

        except HowQuestionTitle.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message': 'Title how does not exist!'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        questions = HowQuestion.objects.filter(
            how_title_id=title_id
        ).values_list('id', flat=True)

        HowQuestionAnswer.objects.filter(
            question_id__in=questions
        ).delete()

        files = HowQuestionAnswer.objects.filter(
            question_id__in=questions,
            question_id__has_file=True
        ).values_list('answer', flat=True)

        [
            delete_s3_file(file)
            for file in files
        ]

        HowQuestionAnswer.objects.filter(
            question_id__in=questions
        ).delete()

        HowQuestionOption.objects.filter(
            question_id__in=questions
        ).delete()

        HowQuestion.objects.filter(
            how_title_id=title_id
        ).delete()

        title_how.delete()

        data = json.dumps({
            'status': 'success',
            'message': 'Title how deleted successfully!'
        })

        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def edit_how_question_api(request):
    """
    Edit question api for how category.

    :param request:
        Django Request parameter.
    :return:
        Question created successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        question_serializer = EditTitleQuestionSerializer(data=body)
        if question_serializer.is_valid():
            question = question_serializer.validated_data.get('question')
            question_type = question_serializer.validated_data.get('question_type')
            question_option = question_serializer.validated_data.get('options')
            is_mandatory = question_serializer.validated_data.get('is_mandatory')
            has_other_field = question_serializer.validated_data.get('has_other_field')
            how_question_id = question_serializer.validated_data.get('question_id')

            has_checkbox = False
            has_selection = False
            has_text = False
            has_date = False
            has_file = False
            has_location = False
            has_options = False

            if question_type == "checkbox":
                has_checkbox = True
                has_options = True

            elif question_type == "date":
                has_date = True

            elif question_type == "file":
                has_file = True

            elif question_type == "location":
                has_location = True

            elif question_type == "selection":
                has_selection = True
                has_options = True

            elif question_type == "text":
                has_text = True

            else:
                data = json.dumps({
                    'status': 'error',
                    'message': 'Invalid question type'
                })
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            try:
                question_object = HowQuestion.objects.get(id=how_question_id)

            except HowQuestion.DoesNotExist:
                data = json.dumps({
                    'status': 'error',
                    'message': 'Question not found'
                })
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            question_object.question = question
            question_object.question_type = question_type
            question_object.has_other_field = has_other_field
            question_object.is_mandatory = is_mandatory
            question_object.has_checkbox = has_checkbox
            question_object.has_selection = has_selection
            question_object.has_text = has_text
            question_object.has_date = has_date
            question_object.has_file = has_file
            question_object.has_location = has_location
            question_object.save()

            HowQuestionOption.objects.filter(
                question_id=question_object.id
            ).delete()

            if has_options:
                question_id = question_object.id

                bulk_options = [
                    HowQuestionOption(
                        question_id=question_id,
                        option=option
                    )
                    for option in question_option
                ]

                HowQuestionOption.objects.bulk_create(bulk_options)

                options = HowQuestionOption.objects.filter(
                    question_id=question_id
                )
                serializer = HowQuestionOptionModelSerializer(options, many=True)
                options_data = f"{pd.DataFrame(serializer.data).to_dict('records')}"

            else:
                options_data = ''

            data = {
                'id': question_object.id,
                'question': question_object.question,
                'question_type': question_object.question_type,
                'has_other_field': question_object.has_other_field,
                'is_mandatory': question_object.is_mandatory,
                'options': options_data
            }

            data = json.dumps({
                'status': 'success',
                'message': 'Question created successfully',
                'data': data
            })
            return Response(data, status=status.HTTP_200_OK)

        else:
            data = json.dumps({
                'status': 'error',
                'message': str(question_serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    else:
        data = ({
            'status': 'error',
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def edit_what_question_api(request):
    """
    Edit question api for what category.

    :param request:
        Django Request parameter.
    :return:
        Question created successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        question_serializer = EditTitleQuestionSerializer(data=body)

        if question_serializer.is_valid():
            question = question_serializer.validated_data.get('question')
            question_type = question_serializer.validated_data.get('question_type')
            question_option = question_serializer.validated_data.get('options')
            is_mandatory = question_serializer.validated_data.get('is_mandatory')
            has_other_field = question_serializer.validated_data.get('has_other_field')
            what_question_id = question_serializer.validated_data.get('question_id')

            has_checkbox = False
            has_selection = False
            has_text = False
            has_date = False
            has_file = False
            has_location = False
            has_options = False

            if question_type == "checkbox":
                has_checkbox = True
                has_options = True

            elif question_type == "date":
                has_date = True

            elif question_type == "file":
                has_file = True

            elif question_type == "location":
                has_location = True

            elif question_type == "selection":
                has_selection = True
                has_options = True

            elif question_type == "text":
                has_text = True

            else:
                data = json.dumps({
                    'status': 'error',
                    'message': 'Invalid question type'
                })
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            try:
                question_object = WhatQuestion.objects.get(id=what_question_id)

            except WhatQuestion.DoesNotExist:
                data = json.dumps({
                    'status': 'error',
                    'message': 'Question not found'
                })
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            question_object.question = question
            question_object.question_type = question_type
            question_object.has_other_field = has_other_field
            question_object.is_mandatory = is_mandatory
            question_object.has_checkbox = has_checkbox
            question_object.has_selection = has_selection
            question_object.has_text = has_text
            question_object.has_date = has_date
            question_object.has_file = has_file
            question_object.has_location = has_location
            question_object.save()

            WhatQuestionOption.objects.filter(
                question_id=question_object.id
            ).delete()

            if has_options:
                question_id = question_object.id

                bulk_options = [
                    WhatQuestionOption(
                        question_id=question_id,
                        option=option
                    )
                    for option in question_option
                ]

                WhatQuestionOption.objects.bulk_create(bulk_options)

                options = WhatQuestionOption.objects.filter(
                    question_id=question_id
                )
                serializer = WhatQuestionOptionModelSerializer(options, many=True)
                options_data = f"{pd.DataFrame(serializer.data).to_dict('records')}"

            else:
                options_data = ''

            data = {
                'id': question_object.id,
                'question': question_object.question,
                'question_type': question_object.question_type,
                'has_other_field': question_object.has_other_field,
                'is_mandatory': question_object.is_mandatory,
                'options': options_data
            }

            data = json.dumps({
                'status': 'success',
                'message': 'Question created successfully',
                'data': data
            })
            return Response(data, status=status.HTTP_200_OK)

        else:
            data = json.dumps({
                'status': 'error',
                'message': str(question_serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    else:
        data = ({
            'status': 'error',
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def delete_what_question_api(request):
    """
    Delete question api for what category.

    :param request:
        Django Request parameter.
    :return:
        Question created successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        question_serializer = DeleteQuestionSerializer(data=body)

        if not question_serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(question_serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        question_id = question_serializer.validated_data.get('question_id')

        try:
            question_object = WhatQuestion.objects.get(id=question_id)

        except WhatQuestion.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message': 'Question not found'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        WhatQuestionOption.objects.filter(
            question_id=question_object.id
        ).delete()

        files = WhatQuestionAnswer.objects.filter(
            question_id__has_file=True,
            question_id=question_object.id
        ).values_list('answer', flat=True)

        [
            delete_s3_file(file)
            for file in files
        ]

        WhatQuestionAnswer.objects.filter(
            question_id=question_object.id
        ).delete()

        question_object.delete()

        data = json.dumps({
            'status': 'success',
            'message': 'Question deleted successfully'
        })
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def delete_how_question_api(request):
    """
    Delete question api for how category.

    :param request:
        Django Request parameter.
    :return:
        Question created successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        question_serializer = DeleteQuestionSerializer(data=body)

        if not question_serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(question_serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        question_id = question_serializer.validated_data.get('question_id')

        try:
            question_object = HowQuestion.objects.get(id=question_id)

        except HowQuestion.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message': 'Question not found'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        HowQuestionOption.objects.filter(
            question_id=question_object.id
        ).delete()

        files = HowQuestionAnswer.objects.filter(
            question_id__has_file=True,
            question_id=question_object.id
        ).values_list('answer', flat=True)

        [
            delete_s3_file(file)
            for file in files
        ]

        HowQuestionAnswer.objects.filter(
            question_id=question_object.id
        ).delete()

        question_object.delete()

        data = json.dumps({
            'status': 'success',
            'message': 'Question deleted successfully'
        })
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def generate_report_claim_api(request):
    """
    Generate report for claim.

    :param request:
        Django Request parameter.
    :return:
        Report generated successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        report_serializer = GenerateReportClaimSerializer(data=body)

        if not report_serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(report_serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        application_id = report_serializer.validated_data.get('application_id')

        application = Application.objects.filter(id=application_id)
        if not application.exists():
            response_data = json.dumps({
                'status': 'error',
                'message': f'Application with id: {application_id} does not exists'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        app_serializer = ApplicationClaimModelSerializer(instance=application, many=True)
        df_application = pd.DataFrame(app_serializer.data)
        df_application = get_preview_report_info(df_application)

        response_data = json.dumps({
            'status': 'success',
            'message': 'Application data retreived',
            'data': df_application.to_dict('records')[0]
        })
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def report_single_claim_api(request):
    """
    Generate report for a selected claim.

    :param request:
        Django Request parameter.
    :return:
        Report generated successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        report_serializer = ClaimApplicationSerializer(data=body)

        if not report_serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(report_serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        claim_id = report_serializer.validated_data.get('claim_id')

        claim = Claim.objects.filter(id=claim_id)
        if not claim.exists():
            response_data = json.dumps({
                'status': 'error',
                'message': f"Claim with id: {claim_id} does not exist"
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        application = Application.objects.get(id=claim.first().application_id)
        serializer = ApplicationClaimModelSerializer(instance=application)

        claim_serializer = ClaimModelSerializer(claim, many=True)
        df_claim = pd.DataFrame(claim_serializer.data)
        df_claim = get_claim_info_service(df_claim)

        data = {
            'application': serializer.data,
            'claim': df_claim.to_dict('records')[0]
        }

        response_data = json.dumps({
            'status': 'success',
            'message': 'Application data retreived',
            'data': data
        })
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def preview_report_claim_api(request):
    """
    preview report for claim.

    :param request:
        Django Request parameter.
    :return:
        Report preview successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        report_serializer = GenerateReportClaimSerializer(data=body)

        if not report_serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(report_serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        application_id = report_serializer.validated_data.get('application_id')
        application = Application.objects.filter(id=application_id)
        if not application.exists():
            response_data = json.dumps({
                'status': 'error',
                'message': f'Application with id: {application_id} does not exists'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        app_serializer = ApplicationClaimModelSerializer(instance=application, many=True)
        df_application = pd.DataFrame(app_serializer.data)
        df_application = get_preview_report_info(df_application)

        response_data = json.dumps({
            'status': 'success',
            'message': 'Application data retreived',
            'data': df_application.to_dict('records')[0]
        })
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_client_claims_api(request):
    """
    API for the collection of client assigned claim applications.

    Args:
        request(django): Django request parameter.

    Return:
        Response(API response): 
            - status
            - data
            - status code
    """
    if request.method == "GET":
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        user_id = validated_data.get('user_id')
        try:
            client_user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': f'User with id: {user_id} not found'
            })
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        claims_list = Claim.objects.filter(
            application_id__client_id__email = client_user.email
        ).values_list('application_id', flat=True)

        claim_applications = Application.objects.filter(
            id__in=claims_list
        )

        application_model_serializer = ApplicationClientModelSerializer(
            claim_applications,
            many=True
        )

        response_data = json.dumps({
            "status": "success",
            "message": "Claim data retrieved successfully!",
            "data": application_model_serializer.data
        })

        return Response(response_data, status=status.HTTP_200_OK)