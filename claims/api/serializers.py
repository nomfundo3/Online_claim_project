"""
Claim api serializers for cleaning incoming and outgoing data.
"""
from rest_framework import serializers
from system_management.general_func_classes import BaseFormSerializer
from claims.models import (
    WhatCategory,
    HowCategory,
    CauseCategory,
    ApplicationHow,
    ApplicationWhat,
    ApplicationCause,
    HowQuestion,
    WhatQuestion,
    HowQuestionOption,
    HowQuestionAnswer,
    WhatQuestionTitle,
    WhatQuestionOption,
    WhatQuestionAnswer,
    HowQuestionTitle,
    AssessmentNote,
    Claim
)
from application.models import (
    Client,
    ClientIncident,
    Business,
    ApplicationType,
    Assessment,
    Application
)


class EditClaimApplicationSerializer(BaseFormSerializer):

    """
    Serializer for editing claim for clients.
    """
    client_id = serializers.IntegerField(
    required=True,
    read_only=False,
    write_only=False,
    error_messages={
        'required': 'The client id field is required.',
        }
    )


    insurance_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The insurance id field is required.',
        }
    )
    policy_no = serializers.CharField(
    max_length=250,
    required=True,
    read_only=False,
    write_only=False,
    error_messages={
        'required': 'The policy number field is required.',
        'max_length': 'The policy number field must be less than 250 characters.'
        }
    )

    street_address = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The street_address field is required.',
            'max_length': 'The street_address field must be less than 250 characters.'
        }
    )
    city = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The incident city field is required.',
            'max_length': 'The incident city field must be less than 250 characters.'
        }
    )
    postal_code = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The  postal code field is required.',
            'max_length': 'The  postal code field must be less than 250 characters.'
        }
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


class AddClientSerializer(BaseFormSerializer):
    """
    Serializer for adding claim clients.
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
    incident_date = serializers.DateTimeField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The incident date field is required.'
        }
    )
    incident_location = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The incident location field is required.',
            'max_length': 'The incident location field must be less than 250 characters.'
        }
    )
    incident_city = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The incident city field is required.',
            'max_length': 'The incident city field must be less than 250 characters.'
        }
    )
    incident_province = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The incident province field is required.',
            'max_length': 'The incident province field must be less than 250 characters.'
        }
    )

    incident_postal = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The incident postal field is required.',
            'max_length': 'The incident postal field must be less than 250 characters.'
        }
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


class EditWhatCategorySerializer(BaseFormSerializer):
    """Serializer for editing what category."""
    category = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category field is required.',
            'max_length': 'The category field must be less than 250 characters.'
        }
    )
    cause_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The cause id field is required.',
        }
    )
    what_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The what id field is required.',
        }
    )


class EditHowCategorySerializer(BaseFormSerializer):
    """Serializer for editing how category."""
    category = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category field is required.',
            'max_length': 'The category field must be less than 250 characters.'
        }
    )
    cause_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The cause id field is required.',
        }
    )
    how_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The how id field is required.',
        }
    )


class EditCauseCategorySerializer(BaseFormSerializer):
    """Serializer for editing how category."""
    category = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category field is required.',
            'max_length': 'The category field must be less than 250 characters.'
        }
    )
    cause_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The cause id field is required.',
        }
    )


class AddHowCategorySerializer(BaseFormSerializer):
    """Add how category serializer."""
    category = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category field is required.',
            'max_length': 'The category field must be less than 250 characters.'
        }
    )
    cause_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The cause id field is required.',
        }
    )


class AddWhatCategorySerializer(BaseFormSerializer):
    """Add what category serializer."""
    category = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category field is required.',
            'max_length': 'The category field must be less than 250 characters.'
        }
    )
    cause_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The cause id field is required.',
        }
    )


class AddCauseCategorySerializer(BaseFormSerializer):
    """Add cause category serializer."""
    category = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category field is required.',
            'max_length': 'The category field must be less than 250 characters.'
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


class WhatCategoryModelSerializer(serializers.ModelSerializer):
    """Model serializer for what category."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for what category."""
        model = WhatCategory
        fields = (
            'id',
            'name',
            'date_created',
            'date_modified',
            'cause_id'
        )
        ordering = ('id',)


class HowCategoryModelSerializer(serializers.ModelSerializer):
    """Model serializer for how category."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for how category."""
        model = HowCategory
        fields = (
            'id',
            'name',
            'date_created',
            'date_modified',
            'cause_id'
        )
        ordering = ('id',)


class CauseCategoryModelSerializer(serializers.ModelSerializer):
    """Model serializer for cause category."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for cause category."""
        model = CauseCategory
        fields = (
            'id',
            'name',
            'date_created',
            'date_modified',
            'application_type_id'
        )
        ordering = ('id',)


class ManageApplicationSerializer(BaseFormSerializer):
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


class ClientModelSerializer(serializers.ModelSerializer):
    """Model serializer for client."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    cover_start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    insurer__insurance_name = serializers.SerializerMethodField()

    business = serializers.SerializerMethodField()
    client_incident = serializers.SerializerMethodField()

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

    @staticmethod
    def get_client_incident(obj):
        """
        Get client incident information
        
        :param obj:
            object type instance
        :return:
            client incident model linked to client
        """
        try:
            client_incident = ClientIncident.objects.get(client_id=obj.id)

        except ClientIncident.DoesNotExist:
            client_incident_data = ''
            return client_incident_data

        serializer = ClientIncidentModelSerializer(client_incident)
        client_incident_data = serializer.data
        return client_incident_data

    @staticmethod
    def get_insurer__insurance_name(obj):
        """
        Get the insurance provider for client based on foreign key.

        :param obj:
            Client class model object.
        :return
            insurance provider name.
        """
        if obj.insurer:
            return obj.insurer.insurance_name
        else:
            return ""

    class Meta:
        """Metaclass for client."""
        model = Client
        fields = (
            'id',
            'first_name',
            'last_name',
            'id_number',
            'email',
            'phone_number',
            'policy_no',
            'cover_start_date',
            'insurer__insurance_name',
            'date_created',
            'date_modified',
            'business',
            'client_incident'
        )
        ordering = ('id',)


class ClientIncidentModelSerializer(serializers.ModelSerializer):
    """Model serializer for client incident."""
    claim_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_of_incident = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for client incident."""
        model = ClientIncident
        fields = (
            'id',
            'date_of_incident',
            'city',
            'street_address',
            'province',
            'postal_code',
            'claim_date_time',
            'client_id'
        )
        ordering = ('id',)


class BusinessModelSerializer(serializers.ModelSerializer):
    """Model serializer for business."""

    class Meta:
        """Metaclass for business."""
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
        ordering = ('id',)


class ApplicationWhatModelSerializer(serializers.ModelSerializer):
    """Application What model serializer for return an application what."""
    what__name = serializers.SerializerMethodField()

    @staticmethod
    def get_what__name(obj):
        """
        Get the application what name.

        :param obj:
            ApplicationWhat class model object.
        :return:
            application what name.
        """
        return obj.what.name

    class Meta:
        """Metaclass for application what."""
        model = ApplicationWhat
        fields = (
            'id',
            'what_id',
            'what__name',
            'application_id'
        )
        ordering = ('id',)


class ApplicationCauseModelSerializer(serializers.ModelSerializer):
    """Application Cause model serializer for return an application cause."""
    cause__name = serializers.SerializerMethodField()

    @staticmethod
    def get_cause__name(obj):
        """
        Get the application cause name.

        :param obj:
            ApplicationCause class model object.
        :return:
            application cause name.
        """
        return obj.cause.name

    class Meta:
        """Metaclass for application cause."""
        model = ApplicationCause
        fields = (
            'id',
            'cause_id',
            'cause__name',
            'application_id'
        )
        ordering = ('id',)


class ApplicationHowModelSerializer(serializers.ModelSerializer):
    """Application How model serializer for return an application how."""
    how__name = serializers.SerializerMethodField()

    @staticmethod
    def get_how__name(obj):
        """
        Get the application how name.

        :param obj:
            ApplicationHow class model object.
        :return:
            application how name.
        """
        return obj.how.name

    class Meta:
        """Metaclass for application how."""
        model = ApplicationHow
        fields = (
            'id',
            'how_id',
            'how__name',
            'application_id'
        )
        ordering = ('id',)


class ApplicationTypeModelSerializer(serializers.ModelSerializer):
    """Application Type model serializer for return an application type."""
    id = serializers.IntegerField(read_only=True)

    class Meta:
        """Metaclass for application type."""
        model = ApplicationType
        fields = (
            'id',
            'name'
        )
        ordering = ('id',)


class ChangeApplicationTypeSerializer(BaseFormSerializer):
    """Change application type serializer."""
    application_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application id field is required.',
        }
    )
    application_type = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application id field is required.',
        }
    )


class ApplicationTypeCategoriesSerializer(BaseFormSerializer):
    """Serializer for application type categories."""
    application_type = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application type field is required.',
        }
    )


class AssignCauseApplicationSerializer(BaseFormSerializer):
    """Serializer for application cause assignment."""
    claim_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The claim id field is required.',
        }
    )
    cause_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The cause id field is required.',
        }
    )


class AssignHowApplicationSerializer(BaseFormSerializer):
    """Serializer for application how assignment."""
    claim_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The claim id field is required.',
        }
    )
    how_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The how id field is required.',
        }
    )


class AssignWhatApplicationSerializer(BaseFormSerializer):
    """Serializer for application what assignment."""
    claim_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The claim id field is required.',
        }
    )
    what_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The what id field is required.',
        }
    )


class TitleAddSerializer(BaseFormSerializer):
    """Serializer for title add."""
    title = serializers.CharField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The title field is required.',
        }
    )
    category_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category id field is required.',
        }
    )


class CreateTitleSerializer(BaseFormSerializer):
    """Serializer for title create."""
    title = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The title field is required.',
            'max_length': 'The title field must be less than 250 characters.'
        }
    )
    category_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category id field is required.',
        }
    )


class CreateTitleQuestionSerializer(BaseFormSerializer):
    """Serializer for the creation of question titles."""
    title_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The title id field is required.',
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
    options = serializers.ListField(
        required=False,
        read_only=False,
        write_only=False,
        child=serializers.CharField(
            max_length=250,
            required=False,
            read_only=False,
            write_only=False,
            error_messages={
                'max_length': 'The options field must be less than 250 characters.'
            }
        )
    )
    is_mandatory = serializers.BooleanField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The is mandatory field is required.',
        }
    )
    has_other_field = serializers.BooleanField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The has other field is required.',
        }
    )


class CategoryIdSerializer(BaseFormSerializer):
    """Serializer for the category id."""
    category_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The category id field is required.',
        }
    )


class HowQuestionModelSerializer(serializers.ModelSerializer):
    """How question model serializer for return an application how."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for application how."""
        model = HowQuestion
        fields = (
            'id',
            'question',
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
            'how_title_id'
        )
        ordering = ('id',)


class WhatQuestionModelSerializer(serializers.ModelSerializer):
    """What question model serializer for return an application what."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    id = serializers.IntegerField(read_only=True)
    what_title_id = serializers.IntegerField(read_only=True)

    class Meta:
        """Metaclass for application what."""
        model = WhatQuestion
        fields = (
            'id',
            'question',
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
            'what_title_id'
        )
        ordering = ('id',)


class HowQuestionOptionModelSerializer(serializers.ModelSerializer):
    """How question option model serializer for return an application how."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    id = serializers.IntegerField(read_only=True)
    question_id = serializers.IntegerField(read_only=True)

    class Meta:
        """Metaclass for application how."""
        model = HowQuestionOption
        fields = (
            'id',
            'option',
            'date_created',
            'date_modified',
            'question_id'
        )
        ordering = ('id',)


class HowQuestionAnswerModelSerializer(serializers.ModelSerializer):
    """How question answer model serializer for return an application how."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for application how."""
        model = HowQuestionAnswer
        fields = (
            'id',
            'answer',
            'date_created',
            'date_modified',
            'claim_id',
            'question_id'
        )
        ordering = ('id',)


class WhatQuestionTitleModelSerializer(serializers.ModelSerializer):
    """What question option model serializer for return an application what."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        """Metaclass for application what."""
        model = WhatQuestionTitle
        fields = (
            'id',
            'title',
            'date_created',
            'date_modified',
            'what_id'
        )
        ordering = ('id',)


class WhatQuestionOptionModelSerializer(serializers.ModelSerializer):
    """What question option model serializer for return an application what."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for application what."""
        model = WhatQuestionOption
        fields = (
            'id',
            'option',
            'date_created',
            'date_modified',
            'question_id'
        )
        ordering = ('id',)


class WhatQuestionAnswerModelSerializer(serializers.ModelSerializer):
    """What question option model serializer for return an application what."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for application what."""
        model = WhatQuestionAnswer
        fields = (
            'id',
            'answer',
            'date_created',
            'date_modified',
            'claim_id',
            'question_id'
        )
        ordering = ('id',)


class HowQuestionTitleModelSerializer(serializers.ModelSerializer):
    """What question option model serializer for return an application what."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for application what."""
        model = HowQuestionTitle
        fields = (
            'id',
            'title',
            'date_created',
            'date_modified',
            'how_id'
        )
        ordering = ('id',)


class GetClaimQuestionsSerializer(BaseFormSerializer):
    """
    Serializer for the retrieval of claim questions.
    """
    application_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application id field is required.',
        }
    )
    what_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The what id field is required.',
        }
    )
    how_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The how id field is required.',
        }
    )


class ClaimSaveQuestionSerializer(BaseFormSerializer):
    """Save claim what and how question serializer."""
    claim_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The claim id field is required.',
        }
    )
    what_answers = serializers.ListField(
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
    how_answers = serializers.ListField(
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


class AssessmentModelSerializer(serializers.ModelSerializer):
    """Serializer for model assessment."""
    scheduled_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    end_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        """Metaclass for model assessment."""
        model = Assessment
        fields = (
            "id",
            "message",
            "scheduled_date_time",
            "end_date_time",
            "event_id",
            "summary",
            "video_link",
            "client_location",
            "application_id"
        )
        ordering = ('id',)


class AssessmentNoteModelSerializer(serializers.ModelSerializer):
    """Serializer for model assessment note."""

    class Meta:
        """Metaclass for model assessment note."""
        model = AssessmentNote
        fields = (
            'id',
            'note',
            'file',
            'date_created',
            'date_modified',
            'assessment_id'
        )
        ordering = ('id',)


class EditTitleSerializer(BaseFormSerializer):
    """
    Serializer for edit title."""

    title = serializers.CharField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The title field is required.',
        }
    )
    title_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The title id field is required.',
        }
    )


class DeleteTitleSerializer(BaseFormSerializer):
    """
    Serializer for delete title."""

    title_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The title id field is required.',
        }
    )


class EditTitleQuestionSerializer(BaseFormSerializer):
    """Serializer for the creation of question titles."""
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
    options = serializers.ListField(
        required=False,
        read_only=False,
        write_only=False,
        child=serializers.CharField(
            max_length=250,
            required=False,
            read_only=False,
            write_only=False,
            error_messages={
                'max_length': 'The options field must be less than 250 characters.'
            }
        )
    )
    is_mandatory = serializers.BooleanField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The is mandatory field is required.',
        }
    )
    has_other_field = serializers.BooleanField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The has other field is required.',
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


class DeleteQuestionSerializer(BaseFormSerializer):
    """Delete question serializer."""
    question_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The question id field is required.',
        }
    )


class GenerateReportClaimSerializer(BaseFormSerializer):
    """
    Generate report claim serializer.
    """
    application_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application id field is required.',
        }
    )


class ApplicationClaimModelSerializer(serializers.ModelSerializer):
    """
    Application claim model serializer.
    """
    client = ClientModelSerializer()
    application_status__name = serializers.SerializerMethodField()
    assessor_id__first_name = serializers.SerializerMethodField()
    assessor_id__last_name = serializers.SerializerMethodField()

    date_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    date_assigned = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    date_created = serializers.DateTimeField(format='%Y-%m-%d')
    date_modified = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    assessment = serializers.SerializerMethodField()

    @staticmethod
    def get_assessment(obj):
        """
        Get the assessment.

        :param obj:
            object type instance
        :return:
            assessment data.
        """
        assessment = Assessment.objects.filter(
            application_id = obj.id
        )
        serializer = AssessmentModelSerializer(assessment, many=True)
        return serializer.data

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


class WhatQuestionTitleSerializer(serializers.ModelSerializer):
    """Serializer for what question title grouping."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    questions = serializers.SerializerMethodField()

    @staticmethod
    def get_questions(obj):
        """
        Get the questions.

        :param obj:
            object type instance
        :return:
            Question group data from what question title.    
        
        """
        questions = WhatQuestion.objects.filter(what_title_id=obj.id)
        serializer = WhatQuestionGroupSerializer(questions, many=True)
        return serializer.data


    class Meta:
        """Metaclass for what question title grouping."""
        model = WhatQuestionTitle
        fields = (
            'id',
            'title',
            'date_created',
            'date_modified',
            'what_id',
            'questions'
        )
        ordering = ('id',)


class WhatQuestionGroupSerializer(serializers.ModelSerializer):
    """What question group serializer."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    options = serializers.SerializerMethodField()

    @staticmethod
    def get_options(obj):
        """Get the options."""
        options = WhatQuestionOption.objects.filter(question_id=obj.id)
        serializer = WhatQuestionOptionModelSerializer(options, many=True)
        return serializer.data

    class Meta:
        """Metaclass for application what."""
        model = WhatQuestion
        fields = (
            'id',
            'question',
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
            'what_title_id',
            'options'
        )
        ordering = ('id',)


class HowQuestionTitleSerializer(serializers.ModelSerializer):
    """Serializer for how question title grouping."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    questions = serializers.SerializerMethodField()

    @staticmethod
    def get_questions(obj):
        """
        Get the questions.

        :param obj:
            object type instance
        :return:
            Question group data from how question title.
        """
        questions = HowQuestion.objects.filter(how_title_id=obj.id)
        serializer = HowQuestionGroupSerializer(questions, many=True)
        return serializer.data


    class Meta:
        """Metaclass for what question title grouping."""
        model = HowQuestionTitle
        fields = (
            'id',
            'title',
            'date_created',
            'date_modified',
            'how_id',
            'questions'
        )
        ordering = ('id',)


class HowQuestionGroupSerializer(serializers.ModelSerializer):
    """How question group serializer."""
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    options = serializers.SerializerMethodField()

    @staticmethod
    def get_options(obj):
        """
        Get the options.
        
        :param obj:
            object type instance
        :return:
            options linked to question by foreign key.
        """
        options = HowQuestionOption.objects.filter(question_id=obj.id)
        serializer = HowQuestionOptionModelSerializer(options, many=True)
        return serializer.data

    class Meta:
        """Metaclass for application how."""
        model = HowQuestion
        fields = (
            'id',
            'question',
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
            'how_title_id',
            'options'
        )
        ordering = ('id',)


class ClaimModelSerializer(serializers.ModelSerializer):
    """Serializer for claim model"""
    application_type__name = serializers.SerializerMethodField()

    @staticmethod
    def get_application_type__name(obj):
        """
        Get the categories.

        :param obj:
            object type instance
        :return:
            application type name data.
        """
        return obj.application_type.name

    class Meta:
        """Metaclass for serializer containing field and model"""
        model = Claim
        fields = (
            'id', 
            'application_id', 
            'application_type_id',
            'application_type__name'
        )


class ClaimApplicationSerializer(BaseFormSerializer):
    """Serializer for the claim application"""
    claim_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The claim id field is required.',
        }
    )
