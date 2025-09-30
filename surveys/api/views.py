"""
Survey api views containing all the api functions
The following api is stored here:
    *`login_api`

"""

import datetime
import json
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import system_management.constants as constants
from system_management.models import (
    User
)

from application.models import (
    Business,
    Client,
    Application,
    ApplicationType,
    Assessment,
    ApplicationStatus
)

from surveys.models import (
    SurveyCategoryType,
    SurveyCategory,
    SurveyApplicationTitle,
    SurveyQuestion,
    SurveyAnswer,
    SurveyQuestionOption,
    Survey
)
from application.api.serializers import (
    ApplicationTypeSerializer
)
from surveys.api.serializers import (
    AddClientSerializer,
    DeleteQuestionSerializer,
    EditBusinessApplicationSerializer,
    EditClientApplicationSerialize,
    ManageSurveySerializer,
    SurveyCategoryTypeSerializer,
    SurveyQuestionOptionModelSerializer,
    UpdateSurveyCatSerializer,
    UpdateSurveyCatTypeSerializer,
    AddBusinessSerializer,
    AddSurveyTitleSerializer,
    UpdateSurveyQuestionSerializer,
    UpdateSurveyTitleSerializer,
    SurveyAnswerSerializer,
    SurveyCategorySerializer,
    SurveyApplicationTitleSerializer,
    AddSurveySurveyCatSerializer,
    SurveyQuestionSerializer,
    SurveyQuestionOptionSerializer,
    CreateQuestionSurveySerializer,
    SurveyorUserModelSerializer,
    SurveySaveQuestionSerializer,
    ApplicationClientModelSerializer,
    SurveyApplicationRetrieveSerializer,
    ChangeSurveyTypeSerializer,
    GetSurveyInfoSerializer,
    CreateMultiSurveySerializer
)
from system_management.amazons3 import (
    delete_s3_file
)
from surveys.api.services import (
    get_survey_categories,
    get_survey_answers,
    get_application_type_info
)


@api_view(['GET'])
def get_survey_overview_api(request):
    """
    This function is used to get the survey overview

    :param request:
        request django parameter
    :return:
        - status and message stating success or error
        - Survey data from serializer
    """
    if request.method == "GET":
        application_types = ApplicationType.objects.values(
            'id',
            'name'
        )
        df_application_types = pd.DataFrame(application_types)
        if not df_application_types.empty:
            df_application_types['tab_name'] = df_application_types['name'].apply(
                lambda name:
                str(name).replace(' ', '_')
            )
            df_application_types = get_application_type_info(df_application_types)
        response_data = json.dumps({
            "status": "success",
            "message": "Surveys data retrieved successfully!",
            "data": df_application_types.to_dict('records'),
        })
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def surveys_api(request):
    if request.method == "GET":
        survey_applications = Survey.objects.values_list(
            'application_id',
            flat=True
        )
        applications = Application.objects.filter(
            id__in=survey_applications
        )

        application_serializer = ApplicationClientModelSerializer(
            applications,
            many=True
        )

        surveyors = User.objects.filter(user_type_id__name=constants.SURVEYOR)
        serializer = SurveyorUserModelSerializer(surveyors, many=True)

        response_data = json.dumps({
            "status": "success",
            "message": "Surveys data retrieved successfully!",
            "data": application_serializer.data,
            "surveyors": serializer.data
        })

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_survey_client_api(request):
    """
    This function is used to add a survey client

    :param request:
        request django parameter
    :return:
        status and message stating success or error

    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = AddClientSerializer(data=body)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            name = validated_data.get('name')
            last_name = validated_data.get('last_name')
            email = validated_data.get('email')
            phone_number = validated_data.get('phone_number')
            insurer_id = validated_data.get('insurer_id')
            id_number = validated_data.get('id_number')
            policy_number = validated_data.get('policy_number')
            location = serializer.validated_data.get('incident_location')

            client = Client.objects.create(
                first_name=name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                insurer_id=insurer_id,
                id_number=id_number,
                policy_no=policy_number,
                location=location
            )

            client_id = client.id

            data = json.dumps({
                "status": "success",
                "message": "Client information added successfully.",
                "data": client_id
            })
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            data = json.dumps({
                "status": "error",
                "message": "Fields error occurred - invalid request",
                "data": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def add_survey_business_api(request):
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
            validated_data = business_serializer.validated_data
            client_id = validated_data.get('client_id')
            business_name = validated_data.get('business_name')
            business_reg_number = validated_data.get('business_reg_number')
            business_vat_number = validated_data.get('business_vat_number')
            business_email = validated_data.get('business_email')
            business_phone_number = validated_data.get('business_phone_number')

            try:
                client = Client.objects.get(id=client_id)
            except Client.DoesNotExist:
                data = json.dumps({
                    "status": "error",
                    "message": "Client does not exist."
                })
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            Business.objects.create(
                client_id=client.id,
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
                "message": "Fields error occurred - invalid request",
                "data": str(business_serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['GET'])
def view_survey_application_api(request):
    """
    This function is used to get the list of survey applications

    :param request:
        request django parameter.
    :return:
        survey application information.

    """

    if request.method == "GET":
        body = json.loads(request.body)

        if 'application_id' not in body:
            data = json.dumps({
                "status": "error",
                "message": "Please provide a valid application id."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        application_id = body.get('application_id')
        application = Application.objects.filter(
            id=application_id).values(
            'id',
            'description',
            'date_created',
            'date_modified',
            'date_assigned',
            'application_status_id',
            'assessor_id',
            'user_id'
        )

        if not application:
            data = json.dumps({
                "status": "error",
                "message": "Application not found."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        application = application.first()
        survey_types = SurveyCategoryType.filter(
            category__type_id=application['application_type_id'])

        if survey_types.exists():

            serializer = SurveyCategoryTypeSerializer(survey_types, many=True)

            data = json.dumps({
                "status": "success",
                "application": application,
                "data": serializer.data
            })
        else:
            data = json.dumps({
                "status": "success",
                "application": application,
                "data": []
            })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def survey_category_questions_api(request):
    """
    This function is for the request for a category questions and titles.

    :param request:
        request django parameter.
    :return:
    
        survey category questions and titles.

    """
    if request.method == "GET":
        body = json.loads(request.body)

        if 'category_id' not in body:
            data = json.dumps({
                "status": "error",
                "message": "Please provide a valid category id."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        category_id = body.get('category_id')
        category = SurveyCategory.objects.filter(
            id=category_id).exists()

        if not category:
            data = json.dumps({
                "status": "error",
                "message": "Category not found."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        questions = SurveyQuestion.objects.filter(
            application_title__subcategory_type_id=category_id).values(
            'id',
            'question',
            'question_type',
            'application_title__subcategory_type_id',
            'application_title__name',
            'application_title_id',
            'has_checkbox',
            'has_selection',
            'has_text',
            'has_date',
            'has_file',
            'has_other_field',
            'has_location'
        )
        if questions.exists():
            question_list = questions.values_list('id', flat=True)
            options = SurveyQuestionOption.objects.filter(
                question_id__in=question_list
            ).values(
                'id',
                'question_id',
                'option'
            )

            answers = SurveyAnswer.objects.filter(
                question_id__in=question_list
            ).values(
                'id',
                'answer',
                'question_id',
            )
            df_questions = pd.DataFrame(questions)
            df_questions = df_questions.order_by('application_title_id')
            df_questions = df_questions.apply(
                lambda series:
                get_answers_options(
                    series, answers, options
                ), axis=1)

            application_titles = list(set(
                df_questions[[
                    'application_title_id',
                    'application_title__name'
                ]].to_dict('records')
            ))

            questions = df_questions.to_dict('records')

            data = json.dumps({
                "status": "success",
                "questions": questions,
                "application_titles": application_titles
            })
            return Response(data=data, status=status.HTTP_200_OK)

        else:
            data = json.dumps({
                "status": "success",
                "questions": [],
                "application_titles": []
            })
            return Response(data=data, status=status.HTTP_200_OK)


def get_answers_options(series, answers, options):
    """
    Add answers and options to the series object.

    :param series:
        series object.
    :param answers:
        answers object.
    :param options:
        options object.
    :return:
        series object with answers and options.
    """
    answers = answers.filter(question_id=series['id'])
    if answers.exists():
        series['answers'] = answers
    else:
        series['answers'] = ''
    options = options.filter(question_id=series['id'])

    if options.exists():
        series['options'] = options
    else:
        series['options'] = ''
    return series


@api_view(['POST'])
def change_assessor_api(request):
    """
    Change assigned surveyor/assessor of the application.

    :param request:
        request django parameter.
    :return:
        change assigned surveyor/assessor of the application.
    """
    if request.method == "POST":
        body = json.loads(request.body)

        if 'application_id' not in body:
            data = json.dumps({
                "status": "error",
                "message": "Please provide a valid application id."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if 'assessor' not in body:
            data = json.dumps({
                "status": "error",
                "message": "Please provide a valid assessor id."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        application_id = body.get('application_id')
        assessor = body.get('assessor')

        try:
            application = Application.objects.get(id=application_id)

        except Application.DoesNotExist:
            data = ({
                'status': 'error',
                'message': 'Application for client not found.'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            assessor_obj = User.objects.get(id=assessor)

        except User.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message': 'Assessor not found.'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if application.assessor_id == assessor_obj.id:
            message = f"""
            Survey is already assigned to {assessor_obj.first_name} {assessor_obj.last_name}
            """
            data = json.dumps({
                'status': 'info',
                'message': message
            })
            return Response(data, status.HTTP_200_OK)

        else:
            application.assessor_id = assessor_obj.id
            application.date_assigned = datetime.datetime.now()
            application.save()
            message = f'''
            Claim  assigned to {assessor_obj.first_name} {assessor_obj.last_name} successfully.
            '''
            data = {
                'first_name': assessor_obj.first_name,
                'last_name': assessor_obj.last_name,
                'email': assessor_obj.email
            }

            data = json.dumps({
                "status": "success",
                "message": message,
                "data": data
            })
            return Response(data, status=status.HTTP_200_OK)
    else:

        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })

        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_survey_categories_api(request):
    """
    Get survey categories.

    :param request:
        request django parameter.
    :return:
        get survey categories.
    """
    if request.method == "GET":
        categories = SurveyCategory.objects.all()
        serializer = SurveyCategorySerializer(categories, many=True)
        data = json.dumps({
            "status": "success",
            "data": serializer.data
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })

        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_survey_types_api(request):
    """
    Get survey categories.

    :param request:
        request django parameter.
    :return:
        get survey categories.
    """
    if request.method == "GET":
        types = SurveyCategoryType.objects.all()
        serializer = SurveyCategoryTypeSerializer(types, many=True)
        data = json.dumps({
            "status": "success",
            "data": serializer.data
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })

        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_survey_titles_api(request):
    """
    Get survey categories.

    :param request:
        request django parameter.
    :return:
        get survey categories.
    """
    if request.method == "GET":
        titles = SurveyApplicationTitle.objects.all()
        serializer = SurveyApplicationTitleSerializer(titles, many=True)
        data = json.dumps({
            "status": "success",
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
def add_survey_category_api(request):
    """
    Add survey category.

    :param request:
        request django parameter.
    :return:
        add survey category.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = AddSurveySurveyCatSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        application_type = validated_data.get("application_type")

        try:
            application_type_object = ApplicationType.objects.get(
                id=application_type
            )

        except ApplicationType.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Application type not found."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        category_name = validated_data.get("category_name")

        survey_cat = SurveyCategory.objects.create(
            type_id=application_type_object.id,
            name=category_name
        )

        survey_cat_data = {
            'id': survey_cat.id,
            'name': survey_cat.name,
            'type_id': survey_cat.type_id,
            'type_name': str(survey_cat.type.name)
        }

        data = json.dumps({
            "status": "success",
            "message": "Survey category added successfully.",
            'data': survey_cat_data
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })

        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def update_survey_category_api(request):
    """
    Update survey category.

    :param request:
        request django parameter.
    :return:
        update survey category.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = UpdateSurveyCatSerializer(data=body)
        if serializer.is_valid():
            application_type = serializer.validated_data.get("application_type")
            category_name = serializer.validated_data.get("category_name")
            category_id = serializer.validated_data.get("category_id")

            try:
                application_type_object = ApplicationType.objects.get(
                    id=application_type
                )
            except ApplicationType.DoesNotExist:
                data = json.dumps({
                    "status": "error",
                    "message": "Application type not found."
                })
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            try:
                survey_cat = SurveyCategory.objects.get(id=category_id)

            except SurveyCategory.DoesNotExist:
                data = json.dumps({
                    "status": "error",
                    "message": "Survey category not found."
                })
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            prev_id = survey_cat.type_id
            survey_cat.name = category_name
            survey_cat.type_id = application_type_object.id
            survey_cat.save()

            data = {
                'prev_id': prev_id,
                'type_id': application_type_object.id,
                'name': survey_cat.name,
                'id': survey_cat.id
            }

            data = json.dumps({
                "status": "success",
                "message": "Survey category updated successfully.",
                "data": data
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
def delete_survey_category_api(request):
    """
    Delete survey category.

    :param request:
        request django parameter.
    :return:
        delete survey category.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        if "category_id" not in body:
            data = json.dumps({
                "status": "error",
                "message": "Please provide a valid category id."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        category_id = body.get("category_id")

        try:
            category_object = SurveyCategory.objects.get(id=category_id)

        except SurveyCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Survey category not found."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        SurveyQuestionOption.objects.filter(
            question__application_title__subcategory_type__category_id=category_object.id
        ).delete()

        SurveyAnswer.objects.filter(
            question__application_title__subcategory_type__category_id=category_object.id
        ).delete()

        SurveyQuestion.objects.filter(
            application_title__subcategory_type__category_id=category_object.id
        ).delete()

        SurveyApplicationTitle.objects.filter(
            subcategory_type__category_id=category_object.id
        ).delete()

        SurveyCategoryType.objects.filter(
            category_id=category_object.id
        ).delete()

        category_object.delete()

        data = json.dumps({
            "status": "success",
            "message": "Survey category deleted successfully."
        })

        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_survey_category_type_api(request):
    """
    Add survey category type.

    :param request:
        request django parameter.
    :return:
        add survey category type.
    """
    if request.method == "POST":
        body = json.loads(request.body)

        if "category_id" not in body:
            data = json.dumps({
                "status": "error",
                "message": "Please provide a valid category id."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if "category_type_name" not in body:
            data = json.dumps({
                "status": "error",
                "message": "Please provide a valid category type name."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        category_id = body.get("category_id")

        try:
            survey_category = SurveyCategory.objects.get(
                id=category_id
            )
        except SurveyCategory.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Survey category not found."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        category_type_name = body.get("category_type_name")

        survey_cat_type = SurveyCategoryType.objects.create(
            category_id=survey_category.id,
            name=category_type_name
        )

        data = {
            'type_id': survey_cat_type.id,
            'category_id': survey_category.id,
            'category_name': survey_category.name,
            'category_tab_name': str(survey_category.name).replace(' ', '_'),
            'type_name': str(survey_cat_type.name).replace(' ', '_')
        }

        data = json.dumps({
            "status": "success",
            "message": "Survey category type added successfully.",
            "data": data
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })

        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def update_survey_category_type_api(request):
    """
    Update survey category type.

    :param request:
        request django parameter.
    :return:
        update survey category type.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = UpdateSurveyCatTypeSerializer(data=body)
        if serializer.is_valid():
            category_name = serializer.validated_data.get("category_name")
            category_type_id = serializer.validated_data.get("category_type_id")

            try:
                survey_category = SurveyCategoryType.objects.get(
                    id=category_type_id
                )
            except SurveyCategory.DoesNotExist:
                data = json.dumps({
                    "status": "error",
                    "message": "Survey category type not found."
                })
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            previous_name = survey_category.name
            survey_category.name = category_name
            survey_category.save()

            data = {
                'id': survey_category.id,
                'name': survey_category.name,
                'category_id': survey_category.category_id,
                'previous_name': previous_name
            }

            response_data = json.dumps({
                "status": "success",
                "message": "Survey category type updated successfully.",
                "data": data
            })
            return Response(data=response_data, status=status.HTTP_200_OK)

        else:

            response_data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })

            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
    else:

        response_data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })

        return Response(data=response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def delete_survey_category_type_api(request):
    """
    Delete survey category type.

    :param request:
        request django parameter.
    :return:
        delete survey category type.
    """
    if request.method == "POST":
        body = json.loads(request.body)

        if "category_type_id" not in body:
            data = json.dumps({
                "status": "error",
                "message": "Please provide a valid category type id."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        category_type_id = body.get("category_type_id")

        try:
            category_object = SurveyCategoryType.objects.get(id=category_type_id)

        except SurveyCategoryType.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Survey category type not found."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        SurveyQuestionOption.objects.filter(
            question__application_title__subcategory_type_id=category_object.id
        ).delete()

        SurveyAnswer.objects.filter(
            question__application_title__subcategory_type_id=category_object.id
        ).delete()

        SurveyQuestion.objects.filter(
            application_title__subcategory_type_id=category_object.id
        ).delete()

        SurveyApplicationTitle.objects.filter(
            subcategory_type_id=category_object.id
        ).delete()

        category_object.delete()

        data = json.dumps({
            "status": "success",
            "message": "Survey category type deleted successfully."
        })

        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_survey_title_api(request):
    """
    Add survey title.

    :param request:
        request django parameter.
    :return:
        add survey title.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = AddSurveyTitleSerializer(data=body)
        if serializer.is_valid():
            survey_title_name = serializer.validated_data.get("survey_title_name")
            survey_category_type_id = serializer.validated_data.get("survey_category_type_id")

            try:
                survey_category_type = SurveyCategoryType.objects.get(
                    id=survey_category_type_id
                )

            except SurveyCategoryType.DoesNotExist:
                data = json.dumps({
                    "status": "error",
                    "message": "Survey category type not found."
                })
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            application_title = SurveyApplicationTitle.objects.create(
                name=survey_title_name,
                subcategory_type_id=survey_category_type.id
            )
            title_data = {
                'id': application_title.id,
                'name': application_title.name
            }

            data = json.dumps({
                "status": "success",
                "message": "Survey title added successfully.",
                "data": title_data
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
def update_survey_title_api(request):
    """
    Update survey title.

    :param request:
        request django parameter.
    :return:
        update survey title.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = UpdateSurveyTitleSerializer(data=body)
        if serializer.is_valid():
            survey_title_id = serializer.validated_data.get("survey_title_id")
            survey_title_name = serializer.validated_data.get("survey_title_name")

            try:
                survey_title_object = SurveyApplicationTitle.objects.get(
                    id=survey_title_id
                )

            except SurveyApplicationTitle.DoesNotExist:
                data = json.dumps({
                    "status": "error",
                    "message": "Survey title not found."
                })
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            survey_title_object.name = survey_title_name
            survey_title_object.save()

            data = {
                'id': survey_title_object.id,
                'name': survey_title_object.name
            }

            response_data = json.dumps({
                "status": "success",
                "message": "Survey title updated successfully."
            })
            return Response(data=response_data, status=status.HTTP_200_OK)

        else:
            response_data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

    else:
        response_data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def delete_survey_title_api(request):
    """
    Delete survey title.

    :param request:
        request django parameter.
    :return:
        delete survey title.
    """
    if request.method == "POST":
        body = json.loads(request.body)

        if "survey_title_id" not in body:
            data = json.dumps({
                "status": "error",
                "message": "Please provide a valid survey title id."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        survey_title_id = body.get("survey_title_id")

        try:
            survey_title_object = SurveyApplicationTitle.objects.get(id=survey_title_id)

        except SurveyApplicationTitle.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Survey title not found."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        SurveyQuestionOption.objects.filter(
            question__application_title_id=survey_title_object.id
        ).delete()

        SurveyAnswer.objects.filter(
            question__application_title_id=survey_title_object.id
        ).delete()

        SurveyQuestion.objects.filter(
            application_title_id=survey_title_object.id
        ).delete()

        survey_title_object.delete()

        data = json.dumps({
            "status": "success",
            "message": "Survey title deleted successfully."
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def generate_report_api(request):
    """
    Api for data for pdf reportlab.

    :param request:
        Django request parameter

    Response:
        client info
        application info
        questions info
        answers info
        assessment info
    """
    if request.method == "GET":
        body = json.loads(request.body)
        serializer = ManageSurveySerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        vaildated_data = serializer.validated_data
        application_id = vaildated_data.get("application_id")

        application = Application.objects.filter(
            id=application_id
        ).values(
            'id',
            'client_id',
            'assessor',
            'date_created',
            'assessor_id__first_name',
            'assessor_id__last_name'
        )

        if not application.exists():
            data = json.dumps({
                'status': 'error',
                'message': 'Application not found.'
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        application = application.first()
        application['date_created'] = application['date_created'].strftime('%b %d, %Y')

        client = Client.objects.filter(
            id=application['client_id']
        ).values(
            'id',
            'first_name',
            'last_name',
            'email',
            'id_number',
            'phone_number',
            'policy_no',
            'insurer_id',
            'insurer_id__insurance_name',
            'insurer_id__email',
            'insurer_id__contact_no',
        ).first()

        assessment = Assessment.objects.filter(
            application_id=application_id
        ).values(
            'id',
            'scheduled_date_time',
            'application_id',
            'client_location'
        ).first()

        if not assessment:
            assessment = ''
        else:
            assessment['scheduled_date_time'] = assessment['scheduled_date_time'].strftime(
                '%b %d, %Y')

        surveys = list(Survey.objects.filter(
            application_id=application_id
        ).values(
            'id',
            'application_type_id',
            'application_type__name',
            'application_id'
        ))
        df_survey = pd.DataFrame(surveys)
        df_survey = get_survey_answers(df_survey)

        data = json.dumps({
            'status': 'success',
            'application': application,
            'client': client,
            'assessment': assessment,
            'surveys': df_survey.to_dict('records')
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:

        data = json.dumps({
            'status': 'error',
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def survey_report_single_api(request):
    """
    Survey Report Single API for the colllection of selected survey info

    :param request:
        Django request parameter.

    Response:
        Answer saved successfully or error.    
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = GetSurveyInfoSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                "status": "error",
                "message": str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        vaildated_data = serializer.validated_data
        survey_id = vaildated_data.get("survey_id")

        surveys = Survey.objects.filter(
            id=survey_id
        ).values(
            'id',
            'application_type_id',
            'application_type__name',
            'application_id'
        )
        if not surveys.exists():
            data = json.dumps({
                'status': 'error',
                'message': 'Survey not found.'
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        df_survey = pd.DataFrame(list(surveys))
        df_survey = get_survey_answers(df_survey)

        application_id = surveys.first()['application_id']

        application = Application.objects.filter(
            id=application_id
        ).values(
            'id',
            'client_id',
            'assessor',
            'date_created',
            'assessor_id__first_name',
            'assessor_id__last_name'
        )

        application = application.first()

        application['date_created'] = application['date_created'].strftime('%b %d, %Y')

        client = Client.objects.filter(
            id=application['client_id']
        ).values(
            'id',
            'first_name',
            'last_name',
            'email',
            'id_number',
            'phone_number',
            'policy_no',
            'insurer_id',
            'insurer_id__insurance_name',
            'insurer_id__email',
            'insurer_id__contact_no',
        ).first()

        assessment = Assessment.objects.filter(
            application_id=application_id
        ).values(
            'id',
            'scheduled_date_time',
            'application_id',
            'client_location'
        ).first()

        if not assessment:
            assessment = ''
        else:
            assessment['scheduled_date_time'] = assessment['scheduled_date_time'].strftime(
                '%b %d, %Y')

        data = json.dumps({
            'status': 'success',
            'application': application,
            'client': client,
            'assessment': assessment,
            'surveys': df_survey.to_dict('records')
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:

        data = json.dumps({
            'status': 'error',
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def survey_answer_api(request):
    """
    Api for data for pdf reportlab.

    :param request:
        Django request parameter.

    Response:
        Answer saved successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        answer_serializer = SurveyAnswerSerializer(data=body)

        if answer_serializer.is_valid():
            survey_id = answer_serializer.validated_data.get('survey_id')
            question_id = answer_serializer.validated_data.get('question_id')
            answer = answer_serializer.validated_data.get('answer')
            try:
                question_object = SurveyQuestion.objects.get(id=question_id)

            except SurveyQuestion.DoesNotExist:
                data = json.dumps({
                    'status': 'error',
                    'message': 'Question not found.'
                })
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            application_title_id = question_object.application_title.id
            subcategory_type_id = question_object.application_title.subcategory_type.id
            category_id = question_object.application_title.subcategory_type.category.id

            SurveyAnswer.objects.create(
                question_id=question_id,
                answer=answer,
                survey_id=survey_id,
                category_id=category_id,
                subcategory_type_id=subcategory_type_id,
                application_title_id=application_title_id,
            )

            data = ({
                'status': 'success',
                'message': 'Answers saved successfully'
            })

            return Response(data, status=status.HTTP_200_OK)

        else:
            data = json.dumps({
                'status': 'error',
                'message': str(answer_serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    else:
        data = ({
            'status': 'error',
            'message': constants.INVALID_REQUEST_METHOD
        })
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_survey_questions_api(request):
    """
    Get all survey questions for survey management.

    :param request:
        Django Request parameter.
    :return:
        List of all questions for a survey.
    """
    if request.method == "GET":

        questions = SurveyQuestion.objects.all()
        options = SurveyQuestionOption.objects.all()

        question_serializer = SurveyQuestionSerializer(questions, many=True)
        option_serializer = SurveyQuestionOptionSerializer(options, many=True)

        try:
            df_questions = pd.DataFrame(question_serializer.data)
            df_options = pd.DataFrame(option_serializer.data)

            if df_questions.empty:
                data = json.dumps({
                    'status': 'success',
                    'questions': [],
                })
                return Response(data, status=status.HTTP_200_OK)

            question_list = df_options['question_id'].values.tolist()

            df_questions['options'] = df_questions['id'].apply(
                lambda question_id:
                df_options[df_options['question_id'] == question_id]['option'].values.tolist()
                if question_id in question_list
                else []
            )

            questions = df_questions.to_dict('records')

            data = json.dumps({
                'status': 'success',
                'data': questions,
            })
            return Response(data, status=status.HTTP_200_OK)

        except KeyError:
            data = json.dumps({
                'status': 'error',
                'message': 'Error occurred during serialization of questions'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_question_survey_api(request):
    """
    Create question api for survey question creation.

    :param request:
        Django Request parameter.
    :return:
        Question created successfully or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        question_serializer = CreateQuestionSurveySerializer(data=body)

        if question_serializer.is_valid():
            application_title_id = question_serializer.validated_data.get('application_title_id')
            question = question_serializer.validated_data.get('question')
            question_type = question_serializer.validated_data.get('question_type')
            survey_question_option = question_serializer.validated_data.get('options')
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

            question_object = SurveyQuestion.objects.create(
                application_title_id=application_title_id,
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
                    SurveyQuestionOption(
                        question_id=question_id,
                        option=option
                    )
                    for option in survey_question_option
                ]

                SurveyQuestionOption.objects.bulk_create(bulk_options)
                options = SurveyQuestionOption.objects.filter(
                    question_id=question_id
                )
                serializer = SurveyQuestionOptionModelSerializer(options, many=True)
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


@api_view(['GET'])
def survey_application_management_api(request):
    if request.method == "GET":
        body = json.loads(request.body)
        serializer = ManageSurveySerializer(data=body)

        if not serializer.is_valid():
            response_data = json.dumps({
                'status': 'error',
                'message': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        application_id = validated_data.get('application_id')

        try:
            application = Application.objects.get(id=application_id)

        except Application.DoesNotExist:
            response_data = json.dumps({
                'status': 'error',
                'message': f"Application with id: {application_id} does not exists."
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        surveys = Survey.objects.filter(application_id=application_id)

        if not surveys.exists():
            response_data = json.dumps({
                'status': 'error',
                'message': f"Application with id: {application_id} is not a survey."
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        application_serializer = SurveyApplicationRetrieveSerializer(instance=application)

        surveyors = User.objects.filter(
            user_type__name=constants.SURVEYOR
        ).values(
            'id',
            'first_name',
            'last_name'
        )

        statuses = ApplicationStatus.objects.values(
            'id',
            'name'
        )

        application_types = ApplicationType.objects.values(
            'id',
            'name'
        )

        data = {
            "current_application": application_serializer.data,
            "surveyors": list(surveyors),
            "statuses": list(statuses),
            'application_types': list(application_types),
            "survey": list(surveys.values(
                'application_type_id',
                'application_type_id__name',
                'id'
            ))
        }

        response_data = json.dumps({
            'status': 'success',
            'message': f"Application data sent for application with id: {application_id}",
            'data': data
        })

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def save_survey_questions_api(request):
    """
    Save survey questions api for category questions.

    :param request:
        Django request parameter.
    :return:
        Response of saved question statuses.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = SurveySaveQuestionSerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        survey_id = validated_data.get('survey_id')
        survey_answers = validated_data.get('survey_answers')

        [
            create_question_instance(answer, survey_id)
            for answer in survey_answers
        ]

        data = json.dumps({
            'status': 'success',
            'message': 'Questions saved successfully!'
        })
        return Response(data, status=status.HTTP_200_OK)


def create_question_instance(answer, survey_id):
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
        question = SurveyQuestion.objects.get(id=question_id)

    except SurveyQuestion.DoesNotExist:
        return None

    question_type = answer['question_type']
    answer_field = answer['answer']

    if question.has_other_field:
        survey_answer = SurveyAnswer.objects.filter(
            question_id=question_id,
            survey_id=survey_id
        ).values('id')

        if not survey_answer.exists():

            application_title = question.application_title
            subcategory_type = application_title.subcategory_type
            category = subcategory_type.category

            SurveyAnswer.objects.create(
                question_id=question.id,
                survey_id=survey_id,
                answer=answer_field,
                application_title_id=application_title.id,
                subcategory_type_id=subcategory_type.id,
                category_id=category.id,
            )
        elif survey_answer.count() == 1:
            if question_type == 'other':
                application_title = question.application_title
                subcategory_type = application_title.subcategory_type
                category = subcategory_type.category

                SurveyAnswer.objects.create(
                    question_id=question.id,
                    survey_id=survey_id,
                    answer=answer_field,
                    application_title_id=application_title.id,
                    subcategory_type_id=subcategory_type.id,
                    category_id=category.id,
                )
            else:
                survey_answer = SurveyAnswer.objects.filter(
                    question_id=question_id,
                    survey_id=survey_id
                ).order_by('id').first()
                if survey_answer:
                    survey_answer.answer = answer_field
                    survey_answer.save()
        else:
            if question_type == 'other':
                survey_answer = SurveyAnswer.objects.filter(
                    question_id=question_id,
                    survey_id=survey_id
                ).order_by('id').last()
                if survey_answer:
                    survey_answer.answer = answer_field
                    survey_answer.save()
            else:
                survey_answer = SurveyAnswer.objects.filter(
                    question_id=question_id,
                    survey_id=survey_id
                ).order_by('id').first()
                if survey_answer:
                    survey_answer.answer = answer_field
                    survey_answer.save()

    else:
        if not SurveyAnswer.objects.filter(
                question_id=question_id,
                survey_id=survey_id
        ).exists():

            application_title = question.application_title
            subcategory_type = application_title.subcategory_type
            category = subcategory_type.category

            SurveyAnswer.objects.create(
                question_id=question.id,
                survey_id=survey_id,
                answer=answer_field,
                application_title_id=application_title.id,
                subcategory_type_id=subcategory_type.id,
                category_id=category.id,
            )

        else:

            SurveyAnswer.objects.filter(
                question_id=question_id,
                survey_id=survey_id
            ).update(
                answer=answer_field
            )

    return None


@api_view(['POST'])
def delete_survey_question_api(request):
    """
    Delete survey question.

    :param request:
        request django parameter.
    :return:
        delete survey question.
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
            survey_question_object = SurveyQuestion.objects.get(id=question_id)

        except SurveyQuestion.DoesNotExist:
            data = json.dumps({
                "status": "error",
                "message": "Survey question not found."
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        survey_question_object.delete()

        data = json.dumps({
            "status": "success",
            "message": "Survey question deleted successfully."
        })
        return Response(data=data, status=status.HTTP_200_OK)

    else:
        data = json.dumps({
            "status": "error",
            "message": constants.INVALID_REQUEST_METHOD
        })
        return Response(data=data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def update_survey_question_api(request):
    """
    Update survey question API.

    :param request:
        Django request parameter.

    :return:
        Status and message indicating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        question_serializer = UpdateSurveyQuestionSerializer(data=body)
        if question_serializer.is_valid():
            question = question_serializer.validated_data.get('question')
            question_type = question_serializer.validated_data.get('question_type')
            question_option = question_serializer.validated_data.get('options')
            is_mandatory = question_serializer.validated_data.get('is_mandatory')
            has_other_field = question_serializer.validated_data.get('has_other_field')
            application_title_id = question_serializer.validated_data.get('question_id')

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
                question_object = SurveyQuestion.objects.get(id=application_title_id)
            except SurveyQuestion.DoesNotExist:
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

            SurveyQuestionOption.objects.filter(
                question_id=question_object.id
            ).delete()

            if has_options:
                question_id = question_object.id

                bulk_options = [
                    SurveyQuestionOption(
                        question_id=question_id,
                        option=option
                    )
                    for option in question_option
                ]

                SurveyQuestionOption.objects.bulk_create(bulk_options)

                options = SurveyQuestionOption.objects.filter(
                    question_id=question_id
                )
                serializer = SurveyQuestionOptionModelSerializer(options, many=True)
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
def change_survey_type_api(request):
    """
    APi for the change of survey application type to the selected application type.

    :param request:
        Django request parameter.

    :return:
        Status and message indicating success or error.
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = ChangeSurveyTypeSerializer(data=body)
        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        survey_id = serializer.validated_data.get('survey_id')
        application_type = serializer.validated_data.get('application_type')

        try:
            survey_object = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message': 'Survey not found'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:
            application_type = ApplicationType.objects.get(id=application_type)
        except Survey.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message': 'Application type not found'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        survey_object.application_type_id = application_type.id
        survey_object.save()

        files = SurveyAnswer.objects.filter(
            question_id__has_file=True,
            survey_id=survey_id
        ).values_list('answer', flat=True)

        [
            delete_s3_file(file)
            for file in files
        ]

        SurveyAnswer.objects.filter(
            survey_id=survey_id
        ).delete()

        data = json.dumps({
            'status': 'success',
            'message': 'Survey type changed successfully'
        })
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_survey_info_api(request):
    """
    Get selected survey information.

    Args:
        request: Django request parameter
    
    Return
        Response: API response containing
            - Status
            - message
            - data
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = GetSurveyInfoSerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        survey_id = serializer.validated_data.get('survey_id')

        survey_objects = Survey.objects.filter(
            id=survey_id
        ).values(
            'id',
            'application_type_id',
            'application_type__name'
        )

        if not survey_objects.exists():
            data = json.dumps({
                'status': 'error',
                'message': 'Survey not found'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        df_survey = pd.DataFrame(survey_objects)
        data = get_survey_categories(df_survey)
        application_types = ApplicationType.objects.all()
        application_types_serializer = ApplicationTypeSerializer(
            application_types,
            many=True
        )
        df_types = pd.DataFrame(application_types_serializer.data)
        if not df_types.empty:
            df_types['name'] = df_types['name'].apply(
                lambda name:
                "Commercial"
                if name == constants.BUSINESS
                else
                name
            )

        data = json.dumps({
            'status': 'success',
            'message': 'Survey information retrieved successfully',
            'data': data.to_dict('records')[0],
            'application_types': df_types.to_dict('records')
        })
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_multi_survey_api(request):
    """
    Api for the creation of a claim application.

    Args:
        request: Django request parameter
    
    Return
        Response: API response containing
            - Status
            - message
            - data
    """
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = CreateMultiSurveySerializer(data=body)

        if not serializer.is_valid():
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        application_type = serializer.validated_data.get('application_type')
        application_id = serializer.validated_data.get('application_id')

        survey_object = Survey.objects.create(
            application_type_id=application_type,
            application_id=application_id
        )

        surveys_all = Survey.objects.values(
            'id',
            'application_type_id',
            'application_id',
            'application_type__name'
        ).filter(
            application_id=application_id
        )

        survey_objects = surveys_all.filter(
            id=survey_object.id
        )

        if not survey_objects.exists():
            data = json.dumps({
                'status': 'error',
                'message': 'Survey not found'
            })
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        df_survey = pd.DataFrame(survey_objects)
        data = get_survey_categories(df_survey)
        application_types = ApplicationType.objects.all()
        application_types_serializer = ApplicationTypeSerializer(
            application_types,
            many=True
        )
        df_types = pd.DataFrame(application_types_serializer.data)
        if not df_types.empty:
            df_types['name'] = df_types['name'].apply(
                lambda name:
                "Commercial"
                if name == constants.BUSINESS
                else
                name
            )

        data = json.dumps({
            'status': 'success',
            'message': 'Survey created successfully',
            'data': data.to_dict('records')[0],
            'application_types': df_types.to_dict('records'),
            'surveys_all': list(surveys_all)
        })
        return Response(data, status=status.HTTP_200_OK)
