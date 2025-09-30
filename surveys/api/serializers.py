"""
Survey api(s) serializers for cleaning incoming and outgoing data
"""
from rest_framework import serializers
from system_management.general_func_classes import BaseFormSerializer
from system_management.models import User
from surveys.models import (
    SurveyCategoryType,
    SurveyCategory,
    SurveyApplicationTitle,
    SurveyQuestionOption,
    SurveyQuestion,
    SurveyAnswer
)
from application.models import (
    Application, 
    ApplicationStatus, 
    ApplicationType, 
    Client,
    Business,
    Assessment
)
from application.api.serializers import (
    InsuranceProviderModelSerializer
)
from claims.api.serializers import (
    AssessmentModelSerializer
)


class EditBusinessApplicationSerializer(BaseFormSerializer):
    """
    Serializer for editing business clients.
    """
    client_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
           'required': 'The client id field is required.',
        }
    )
    business_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The first name field is required.',
            'max_length': 'The first name field must be less than 250 characters.'
        }
    )
    reg_number = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The last name field is required.',
            'max_length': 'The last name field must be less than 250 characters.'
        }
    )
    business_email = serializers.EmailField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The email field is required.',
            'max_length': 'The email field must be less than 250 characters.'
        }
    )
    vat_number = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The phone number field is required.',
            'max_length': 'The phone number field must be 10 characters.'
        }
    )
    phone_no = serializers.CharField(
        max_length=10,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The id number field is required.',
            'max_length': 'The id number field must be 13 characters.'
        }
    )

class EditClientApplicationSerialize(BaseFormSerializer):
    """
    Serializer for editing claim clients.
    """
    client_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
           'required': 'The client id field is required.',
        }
    )
    first_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The first name field is required.',
            'max_length': 'The first name field must be less than 250 characters.'
        }
    )
    last_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The last name field is required.',
            'max_length': 'The last name field must be less than 250 characters.'
        }
    )
    email = serializers.EmailField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The email field is required.',
            'max_length': 'The email field must be less than 250 characters.'
        }
    )
    phone_number = serializers.CharField(
        max_length=10,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The phone number field is required.',
            'max_length': 'The phone number field must be 10 characters.'
        }
    )
    id_number = serializers.CharField(
        max_length=13,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The id number field is required.',
            'max_length': 'The id number field must be 13 characters.'
        }
    )


class SurveyorUserModelSerializer(serializers.ModelSerializer):
    """Survey users serializer"""

    class Meta:
        """Metacalss for survey user serializer"""
        model = User
        fields = (
            'id',
            'first_name',
            'last_name'
        )


class AddClientSerializer(BaseFormSerializer):
    """
    Serializer for adding client
    """
    insurer_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The insurer id field is required.',
        }
    )
    name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The first name field is required.',
            'max_length': 'The first name field must be less than 250 characters.'
        }
    )
    last_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The last name field is required.',
            'max_length': 'The last name field must be less than 250 characters.'
        }
    )
    email = serializers.EmailField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The email field is required.',
            'max_length': 'The email field must be less than 250 characters.'
        }
    )
    phone_number = serializers.CharField(
        max_length=11,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The phone number field is required.',
            'max_length': 'The phone number field must be 10 characters.'
        }
    )
    id_number = serializers.CharField(
        max_length=13,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The id number field is required.',
            'max_length': 'The id number field must be 13 characters.'
        }
    )
    policy_number = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The last name field is required.',
            'max_length': 'The last name field must be less than 250 characters.'
        }
    )
    incident_location = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The location field is required.',
            'max_length': 'The location field must be less than 250 characters.'
        }
    )


class ApplicationTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationType
        fields = (
            'id',
            'name'
        )
        
class AddBusinessSerializer(BaseFormSerializer):
    """Business information serializer."""
    business_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The business name field is required.',
            'max_length': 'The business name field must be less than 250 characters.'
        }
    )
    business_email = serializers.EmailField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The business email field is required.',
            'max_length': 'The business email field must be less than 250 characters.'
        }
    )
    business_reg_number = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The business registration number field is required.',
            'max_length': 'The business registration number field must be less than 250 characters.'
        }
    )
    business_vat_number = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The business vat number field is required.',
            'max_length': 'The business vat number field must be less than 250 characters.'
        }
    )
    business_phone_number = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The business phone number field is required.',
            'max_length': 'The business phone number field must be less than 250 characters.'
        }
    )
    client_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The client id field is required.',
        }
    )

class ApplicationStatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = (
            'id',
            'name',
        )


class ApplicationModelSerializer(serializers.ModelSerializer):
    application_status__name = serializers.SerializerMethodField()
    assessor_id__first_name = serializers.SerializerMethodField()
    assessor_id__last_name = serializers.SerializerMethodField()

    date_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    date_assigned = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    date_created = serializers.DateTimeField(format='%Y-%m-%d')
    date_modified = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_assessor_id__first_name(obj):
        """
            get type name

            :param obj:
                object type instance
            :return:
                user model: field = first name
            """
        if obj.assessor == '':
            return ''
        
        elif obj.assessor is None:
            return ''
        
        else:
            return obj.assessor.first_name

    @staticmethod
    def get_assessor_id__last_name(obj):
        """
            get type name

            :param obj:
                object type instance
            :return:
                 user model: field = last name
            """
        if obj.assessor == '':
            return ''
        
        elif obj.assessor is None:
            return ''

        else:
            return obj.assessor.last_name

    @staticmethod
    def get_application_status__name(obj):
        """
            get type name

            :param obj:
                object type instance
            :return:
                application status model: field = name
            """
        return obj.application_status.name


    class Meta:
        model = Application
        fields = (
            'id',
            'date_created',
            'date_modified',
            'date_assigned',
            'assessor_id',
            'client_id',
            'application_status_id',
            'application_status__name',
            'assessor_id__first_name',
            'assessor_id__last_name'
        )


class ClientModelSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    insurer = InsuranceProviderModelSerializer()

    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'email',
            'id_number',
            'phone_number',
            'policy_no',
            'date_created',
            'insurer',
        )


class SurveyApplicationTitleSerializer(serializers.ModelSerializer):
    """
    Serializer for survey application title.
    """
    tab_name = serializers.SerializerMethodField()

    @staticmethod
    def get_tab_name(obj):
        """
        get type name
        
        :param obj:
            object type instance
        :return:
            type name as _ link
        """       
        tab_name = str(obj.name).replace(' ', '_')
        return tab_name
    
    class Meta:
        """Metaclass for survey application title serializer"""
        model = SurveyApplicationTitle
        fields = (
            'id',
            'name',
            'subcategory_type_id',
            'tab_name'
        )


class SurveyCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for survey category.
    """
    type__name = serializers.SerializerMethodField()
    tab_name = serializers.SerializerMethodField()

    @staticmethod
    def get_tab_name(obj):
        """
        get type name
        
        :param obj:
            object type instance
        :return:
            type name as _ link
        """       
        tab_name = str(obj.name).replace(' ', '_')
        return tab_name

    @staticmethod
    def get_type__name(obj):
        """
        get type name
        
        :param obj:
            object type instance
        :return:
            type name
        """
        return obj.type.name

    class Meta:
        """Metaclass for survey category serializer"""
        model = SurveyCategory
        fields = (
            'id',
            'name',
            'type_id',
            'type__name',
            'tab_name'
        )


class SurveyCategoryTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for survey category type
    """
    category__name = serializers.SerializerMethodField()
    category__type_id = serializers.SerializerMethodField()
    tab_name = serializers.SerializerMethodField()

    @staticmethod
    def get_tab_name(obj):
        """
        get type name
        
        :param obj:
            object type instance
        :return:
            type name as _ link
        """       
        tab_name = str(obj.name).replace(' ', '_')
        return tab_name
    
    @staticmethod
    def get_category__name(obj):
        """
        get category name

        :param obj:
            object type instance
        :return:
            category name
        """
        return obj.category.name

    @staticmethod
    def get_category__type_id(obj):
        """
        get category type id

        :param obj:
            object type instance
        :return:
            category type id
        """
        return obj.category.type_id

    class Meta:
        """Metaclass for survey category type serializer"""
        model = SurveyCategoryType
        fields = (
            'id',
            'name',
            'category_id',
            'category__type_id',
            'category__name',
            'tab_name'
        )


class AddSurveySurveyCatSerializer(BaseFormSerializer):
    """
    Serializer for add survey category
    """
    category_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category name field is required.',
            'max_length': 'The category name field must be less than 250 characters.'
        }
    )
    application_type = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application type field is required.',
        }
    )


class UpdateSurveyCatSerializer(BaseFormSerializer):
    """
    Serializer for updating survey category
    """
    category_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category id field is required.',
        }
    )
    category_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category name field is required.',
            'max_length': 'The category name field must be less than 250 characters.'
        }
    )
    application_type = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application type field is required.',
        }
    )


class UpdateSurveyCatTypeSerializer(BaseFormSerializer):
    """
    Serializer for updating survey category type.
    """
    category_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category name field is required.',
            'max_length': 'The category name field must be less than 250 characters.'
        }
    )
    category_type_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category type id field is required.',
        }
    )


class AddSurveyTitleSerializer(BaseFormSerializer):
    """
    Serializer for adding survey title
    """
    survey_category_type_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The survey category type id field is required.',
        }
    )
    survey_title_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The survey title field is required.',
            'max_length': 'The survey title field must be less than 250 characters.'
        }
    )


class UpdateSurveyTitleSerializer(BaseFormSerializer):
    survey_title_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The survey title id field is required.',
        }
    )
    survey_title_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The survey title field is required.',
            'max_length': 'The survey title field must be less than 250 characters.'
        }
    )   


class SurveyAnswerSerializer(BaseFormSerializer):
    """
    Serializer for survey answer
    """
    question_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The question id field is required.',
        }
    )
    survey_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application id field is required.',
        }
    )
    answer = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The answer field is required.',
            'max_length': 'The answer field must be less than 250 characters.'
        }
    )


class SurveyQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for survey question
    """

    class Meta:
        """Metaclass for survey question serializer"""
        model = SurveyQuestion
        fields = (
            'id',
            'question',
            'number',
            'question_type',
            'is_mandatory',
            'has_checkbox',
            'has_selection',
            'has_text',
            'has_date',
            'has_file',
            'has_other_field',
            'has_location',
            'date_created',
            'date_modified',
            'application_title_id'
        )


class SurveyQuestionOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for survey question options
    """

    class Meta:
        """Metaclass for survey question options serializer"""
        model = SurveyQuestionOption
        fields = (
            'id',
            'option',
            'date_created',
            'date_modified',
            'question_id'
        )


class CreateQuestionSurveySerializer(BaseFormSerializer):
    """
    Serializer for creating a new question survey.
    """
    application_title_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application title id field is required.',
        }
    )

    question_type = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The question type field is required.',
            'max_length': 'The question type field must be less than 250 characters.'
        }
    )

    question = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The question field is required.',
            'max_length': 'The question field must be less than 250 characters.'
        }
    )
    options = serializers.ListField(
        required=False,
        read_only=False,
        write_only=False,
        allow_empty=True,
        allow_null=True
    )
    is_mandatory = serializers.BooleanField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The "is mandatory" field is required.',
            'invalid': 'The "is mandatory" field must be boolean.'
        }
    )
    has_other_field = serializers.BooleanField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The "has other" field is required.',
            'invalid': 'The "has other" field must be boolean.'
        }
    )


class ManageSurveySerializer(BaseFormSerializer):
    """
    Serializer for manage application.
    """
    application_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application id field is required.',
        }
    )        
class UpdateSurveyQuestionSerializer(BaseFormSerializer):

    question_type = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The question type field is required.',
            'max_length': 'The question type field must be less than 250 characters.'
        }
    )

    question = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The question field is required.',
            'max_length': 'The question field must be less than 250 characters.'
        }
    )
    options = serializers.ListField(
        required=False,
        read_only=False,
        write_only=False,
        allow_empty=True,
        allow_null=True
    )
    is_mandatory = serializers.BooleanField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The "is mandatory" field is required.',
            'invalid': 'The "is mandatory" field must be boolean.'
        }
    )
    has_other_field = serializers.BooleanField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The "has other" field is required.',
            'invalid': 'The "has other" field must be boolean.'
        }
    )
    question_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The question id field is required.',
        }
    )

class SurveyQuestionOptionModelSerializer(serializers.ModelSerializer):
    """How question option model serializer for return an application how."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for application how."""
        model = SurveyQuestionOption
        fields = (
            'id',
            'option',
            'date_created',
            'date_modified',
            'question_id'
        )
        ordering = ('id',)

class DeleteQuestionSerializer(BaseFormSerializer):
    """
    Serializer for manage application.
    """
    question_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The question id field is required.',
        }
    )


class SurveySaveQuestionSerializer(BaseFormSerializer):
    """
    Save survey what and how question serializer.
    """
    survey_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The survey id field is required.',
        }
    )
    survey_answers = serializers.ListField(
        required=False,
        read_only=False,
        write_only=False,
        allow_null=True,
        allow_empty=True,
        child=serializers.DictField(
            required=False,
            read_only=False,
            write_only=False,
            allow_null=True,
            allow_empty=True,
        )
    )


class ApplicationClientModelSerializer(serializers.ModelSerializer):
    """Application Information including client information"""
    application_status__name = serializers.SerializerMethodField()
    assessor_id__first_name = serializers.SerializerMethodField()
    assessor_id__last_name = serializers.SerializerMethodField()

    date_assigned = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    date_created = serializers.DateTimeField(format='%Y-%m-%d')
    date_modified = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    client = ClientModelSerializer()
    assessment = serializers.SerializerMethodField()

    @staticmethod
    def get_assessment(obj):
        """
        get type name

        :param obj:
            object type instance
        :return:
            assessment model: field = assessment
        """
        try:
            assessment = Assessment.objects.get(application_id=obj.id)
        except Assessment.DoesNotExist:
            return ''
            
        assessment_serializer = AssessmentModelSerializer(assessment)
        return assessment_serializer.data

    @staticmethod
    def get_assessor_id__first_name(obj):
        """
            get type name

            :param obj:
                object type instance
            :return:
                user model: field = first name
            """
        if obj.assessor == '':
            return ''
        
        elif obj.assessor is None:
            return ''
        
        else:
            return obj.assessor.first_name

    @staticmethod
    def get_assessor_id__last_name(obj):
        """
            get type name

            :param obj:
                object type instance
            :return:
                 user model: field = last name
            """
        if obj.assessor == '':
            return ''
        
        elif obj.assessor is None:
            return ''

        else:
            return obj.assessor.last_name

    @staticmethod
    def get_application_status__name(obj):
        """
            get type name

            :param obj:
                object type instance
            :return:
                application status model: field = name
            """
        return obj.application_status.name


    class Meta:
        model = Application
        fields = (
            'id',
            'date_created',
            'date_modified',
            'date_assigned',
            'assessor_id',
            'application_status_id',
            'application_status__name',
            'assessor_id__first_name',
            'assessor_id__last_name',
            'client',
            'assessment'
        )


class BusinessModelSerializer(serializers.ModelSerializer):
    """Model serializer for business model"""
    class Meta:
        model = Business
        fields = (
            'id', 
            'business_name', 
            'business_email', 
            'reg_number', 
            'vat_number', 
            'phone_no', 
            'client_id'
        )


class ClientBusinessModelSerializer(serializers.ModelSerializer):
    """Client Information including business information"""
    date_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    insurer = InsuranceProviderModelSerializer()
    business = serializers.SerializerMethodField()

    @staticmethod
    def get_business(obj):
        """
        Get business information
        
        :param obj:
            object type instance
        :return:
            business model linked to client
        """
        try:
            business = Business.objects.get(client_id=obj.id)
        except Business.DoesNotExist:
            business_data = ''
            return business_data
        
        serializer = BusinessModelSerializer(business)
        business_data = serializer.data
        return business_data

    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'email',
            'id_number',
            'phone_number',
            'policy_no',
            'date_created',
            'insurer',
            'business',
        )


class SurveyApplicationRetrieveSerializer(serializers.ModelSerializer):
    """Collect all data for application survey"""
    application_status__name = serializers.SerializerMethodField()
    assessor_id__first_name = serializers.SerializerMethodField()
    assessor_id__last_name = serializers.SerializerMethodField()

    date_assigned = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    date_created = serializers.DateTimeField(format='%Y-%m-%d')
    date_modified = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S') 

    client = ClientBusinessModelSerializer()

    @staticmethod
    def get_assessor_id__first_name(obj):
        """
            get type name

            :param obj:
                object type instance
            :return:
                user model: field = first name
            """
        if obj.assessor == '':
            return ''
        
        elif obj.assessor is None:
            return ''
        
        else:
            return obj.assessor.first_name

    @staticmethod
    def get_assessor_id__last_name(obj):
        """
            get type name

            :param obj:
                object type instance
            :return:
                 user model: field = last name
            """
        if obj.assessor == '':
            return ''
        
        elif obj.assessor is None:
            return ''

        else:
            return obj.assessor.last_name

    @staticmethod
    def get_application_status__name(obj):
        """
            get type name

            :param obj:
                object type instance
            :return:
                application status model: field = name
            """
        return obj.application_status.name
        
    class Meta:
        model = Application
        fields = (
            'id',
            'date_created',
            'date_modified',
            'date_assigned',
            'assessor_id',
            'application_status_id',
            'application_status__name',
            'assessor_id__first_name',
            'assessor_id__last_name',
            'client'
        )


class ChangeSurveyTypeSerializer(BaseFormSerializer):
    """Change survey type serializer"""
    survey_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The survey id field is required.',
        }
    )
    application_type = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application type id field is required.',
        }
    )


class GetSurveyInfoSerializer(BaseFormSerializer):
    """Get survey info serializer"""
    survey_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The survey id field is required.',
        }
    )

class SurveyCategoryModelSerializer(serializers.ModelSerializer):
    """Serializer for survey category"""

    class Meta:
        model = SurveyCategory
        fields = (
            'id',
            'name'
        )


class SurveyCategoryTypeModelSerializer(serializers.ModelSerializer):
    """Serializer for survey category type"""

    class Meta:
        model = SurveyCategoryType
        fields = (
            'id',
            'name',
            'category_id'
        )


class SurveyApplicationTitleModelSerializer(serializers.ModelSerializer):
    """Serializer for survey application title"""

    class Meta:
        model = SurveyApplicationTitle
        fields = (
            'id',
            'name',
            'subcategory_type_id'
        )


class SurveyAnswerLinkSerializer(serializers.ModelSerializer):
    """Serializer for survey answer link"""
    application_title = SurveyApplicationTitleModelSerializer(read_only=True)
    category = SurveyCategoryModelSerializer(read_only=True)
    question = SurveyQuestionSerializer(read_only=True)
    subcategory_type = SurveyCategoryTypeModelSerializer(read_only=True)

    id = serializers.IntegerField(read_only=True)
    survey_id = serializers.IntegerField(read_only=True)
    question_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SurveyAnswer
        fields = (
            'id',
            'survey_id',
            'question_id',
            'answer',
            'application_title', 
            'category', 
            'question', 
            'subcategory_type'
        )


class CreateMultiSurveySerializer(BaseFormSerializer):
    """Create multi survey serializer"""
    application_type = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application type id field is required.',
        }
    )
    application_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application id field is required.',
        }
    )