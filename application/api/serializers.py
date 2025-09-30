"""
Application api serializers for cleaning incoming and outgoing data.
"""
from rest_framework import serializers
from system_management.general_func_classes import BaseFormSerializer
from application.models import (
    InsuranceProvider,
    ApplicationType,
    Application,
    Client,
    Assessment,
    TwilioRoom
)
from claims.models import (
    AssessmentNote
)
from system_management.api.serializers import (
    UserModelSerializer,
)


class AssessmentSerializer(BaseFormSerializer):
    """
    Serializer for assessment.
    """
    assessment_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The user type field is required.',
        }
    )
    gps_coordinates = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The gps coordinates field is required.',
            'max_length': 'The gps coordinates field must be less than 250 characters.'
        }
    )


class InsuranceProviderModelSerializer(serializers.ModelSerializer):
    """
    Serializer for insurance provider
    """

    class Meta:
        """Metaclass for insurance provider serializer"""
        model = InsuranceProvider
        fields = (
            'id',
            'insurance_name',
            'contact_no',
            'email'
        )


class ApplicationTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for application type
    """

    class Meta:
        """Metaclass for application type serializer"""
        model = ApplicationType
        fields = (
            'id',
            'name'
        )


class InsuranceProviderSerializer(BaseFormSerializer):
    """Serializer for insurance provider info"""
    insurance_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The insurance name field is required.',
            'max_length': 'The insurance name field must be less than 250 characters.'
        }
    )
    email = serializers.EmailField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The email field is required.',
        }
    )
    contact_no = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The contact number field is required.',
        }
    )


class UpdateInsuranceProviderSerializer(BaseFormSerializer):
    """
    Serializer for update insurance provider info
    """
    insurance_name = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The insurance name field is required.',
            'max_length': 'The insurance name field must be less than 250 characters.'
        }
    )
    email = serializers.EmailField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The email field is required.',
        }
    )
    contact_no = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The contact number field is required.',
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


class DeleteInsuranceProviderSerializer(BaseFormSerializer):
    """
    Serializer for delete insurance provider info.
    """
    insurance_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The insurance id field is required.',
        }
    )


class CreateApplicationSerializer(BaseFormSerializer):
    """Create a application serializer"""
    application_category = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application category field is required.',
            'max_length': 'The application category field must be less than 250 characters.'
        }
    )
    application_type = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application type field is required.',
            'max_length': 'The application type field must be less than 250 characters.'
        }
    )
    user_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The user id field is required.',
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


class AssessmentNoteModalSerializer(serializers.ModelSerializer):
    """Model serializer for assessment note modal"""

    class Meta:
        model = AssessmentNote
        fields = (
            'id',
            'note',
            'file',
            'assessment_id',
            'claim_id',
        )


class SingleAssessmentNoteSerializer(BaseFormSerializer):
    """Serializer for single assessment note"""
    notes_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The notes id field is required.',
        }
    )


class EditAssessmentNoteFileSerializer(BaseFormSerializer):
    """Serializer for edit assessment note file"""
    notes_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The notes id field is required.',
        }
    )
    file = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The file field is required.',
            'max_length': 'The file field must be less than 250 characters.',
        }
    )


class CreateAssessmentNotesSerializer(BaseFormSerializer):
    """
    Create a assessment notes serializer
    """
    assessment_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The assessment id field is required.',
        }
    )
    claim_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The claim id field is required.',
        }
    )
    description = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The description field is required.',
            'max_length': 'The description field must be less than 250 characters.',
        }
    )
    file = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The file field is required.',
            'max_length': 'The file field must be less than 250 characters.',
        }
    )


class CreateAssessmentSerializer(BaseFormSerializer):
    """
    Create a assessment serializer
    """
    application_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application id field is required.',
        }
    )
    description = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The description field is required.',
            'max_length': 'The description field must be less than 250 characters.',
        }
    )
    start_date = serializers.DateTimeField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The start date field is required.',
        }
    )
    end_time = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The end time field is required.',
            'max_length': 'The end time field must be less than 250 characters.',
        }
    )
    event_summary = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The event summary field is required.',
            'max_length': 'The event summary field must be less than 250 characters.',
        }
    )
    event_id = serializers.CharField(
        max_length=250,
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The event id field is required.',
            'max_length': 'The event id field must be less than 250 characters.',
        }
    )


class GetApplicationStatusSerializer(BaseFormSerializer):
    """Serializer for GetApplicationStatus"""
    application_status = serializers.CharField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application status field is required.',
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


class GetApplicationSerializer(BaseFormSerializer):
    """
    Get specific application serializer
    """
    application_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The application id field is required.',
        }
    )


class ClientAssessmentSerializer(serializers.ModelSerializer):
    """Client Assessment Serializer"""

    class Meta:
        model = Client
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
        )


class ApplicationAssessmentSerializer(serializers.ModelSerializer):
    """Application Assessment Serializer"""
    client = ClientAssessmentSerializer(read_only=True)
    assessor = UserModelSerializer(read_only=True)

    class Meta:
        model = Application
        fields = (
            'id',
            'client',
            'assessor'
        )


class CreateRoomSerializer(BaseFormSerializer):
    """
    Serializer for create room
    """
    assessment_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The assessment id field is required.',
        }
    )


class GetAssessmentsSerializer(BaseFormSerializer):
    """Serializer for GetAssessments"""
    date = serializers.DateField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The date field is required.',
        }
    )


class AssessmentModelSerializer(serializers.ModelSerializer):
    """Model serializer for assessment"""
    scheduled_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S") 
    end_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Assessment
        fields = (
            'id', 
            'message', 
            'scheduled_date_time', 
            'end_date_time', 
            'event_id', 
            'summary', 
            'video_link', 
            'client_location', 
            'application_id'
        )


class SelectedAssessmentsSerializer(BaseFormSerializer):
    """Selected Year and month serializer"""
    selected_year = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The selected year field is required.',
        }
    )
    selected_month = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The selected month field is required.',
        }
    )


class AssessmentApplicationSerializer(serializers.ModelSerializer):
    """Model serializer for assessment"""
    scheduled_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S") 
    end_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    application = ApplicationAssessmentSerializer()

    class Meta:
        model = Assessment
        fields = (
            'id', 
            'message', 
            'scheduled_date_time', 
            'end_date_time', 
            'event_id', 
            'summary', 
            'video_link', 
            'client_location', 
            'application'
        )


class GetAssessmentInfoSerializer(BaseFormSerializer):
    """Selected Year and month serializer"""
    assessment_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The assessment id field is required.',
        }
    )


class GetRoomSerializer(BaseFormSerializer):
    """Serializer for Getting Room by id"""
    room_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The room id field is required.',
        }
    )


class EventCalendarSerializer(BaseFormSerializer):
    """Serializer for Getting Room by id"""
    user_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The user id field is required.',
        }
    )


class GetAssessmentEventTokenSerializer(BaseFormSerializer):
    """Serializer for Getting Room by id"""
    twilio_room_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The twilio room id field is required.',
        }
    )
    user_id = serializers.IntegerField(
        required=True,
        read_only=False,
        write_only=False,
        error_messages={
            'required': 'The user id field is required.',
        }
    )


class TwilioRoomModelSerializer(serializers.ModelSerializer):
    """Model serializer for assessment"""
    class Meta:
        model = TwilioRoom
        fields = (
            'id', 
            'room_sid', 
            'room_name', 
            'room_status', 
            'assessment_id'
        )