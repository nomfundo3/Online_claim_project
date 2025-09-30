"""
Models for Assessment app containing the application overview and notes.
"""
from django.db import models
from system_management.models import User


class ApplicationStatus(models.Model):
    """Application status e.g. Pending , Completed or Scheduled"""

    name = models.CharField(max_length=250)

    class Meta:
        """Metaclass for application status"""
        verbose_name = "Application Status"
        verbose_name_plural = "Application Statuses"

    def __str__(self):
        """Return the name of the application status"""
        return f"{self.name}"


class ApplicationType(models.Model):
    """Application type e.g. business or personal"""

    name = models.CharField(max_length=250)

    class Meta:
        """Metaclass for application type"""
        verbose_name = "Application Type"
        verbose_name_plural = "Application Types"

    def __str__(self):
        """Return the name of the application type"""
        return f"{self.name}"


class InsuranceProvider(models.Model):
    """General insurance provider information"""

    insurance_name = models.CharField(max_length=250)
    contact_no = models.CharField(max_length=250)
    email = models.CharField(max_length=250)

    class Meta:
        """Metaclass for insurance provider"""
        verbose_name = "Insurance Provider"
        verbose_name_plural = "Insurance Providers"

    def __str__(self):
        """Return the insurance name"""
        return f"{self.insurance_name}"


class Client(models.Model):
    """Client information model for the application"""
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    id_number = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)
    policy_no = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=250,null=True)

    # Foreign  key(s) to the client model
    insurer = models.ForeignKey(InsuranceProvider, on_delete=models.PROTECT, null=True)

    class Meta:
        """Metaclass for client"""
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        """Return the client name"""
        return str(self.first_name)


class Application(models.Model):
    """A model for the representation of an application e.g. a claim or survey."""
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_assigned = models.DateTimeField(null=True)

    # Foreign key(s) to the application model
    assessor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessor', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
    application_status = models.ForeignKey(ApplicationStatus, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for application"""
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        """Return the application type"""
        return f"{self.assessor}"


class ApplicationLog(models.Model):
    """Application progress log model for admin reference"""

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    log = models.CharField(max_length=250)

    class Meta:
        """Metaclass for application log"""
        verbose_name = "Application Log"
        verbose_name_plural = "Application Logs"

    def __str__(self):
        """Return the log"""
        return f"{self.log}"


class ClientIncident(models.Model):
    """
    Client incident model for the application's client
    """
    date_of_incident = models.DateTimeField()
    city = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    claim_date_time = models.DateTimeField(auto_now_add=True)

    # Foreign  key(s) to the client incident model
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for client incident"""
        verbose_name = "Client Incident"
        verbose_name_plural = "Client Incidents"

    def __str__(self):
        """Return the client incident"""
        return f"{self.client}"


class Business(models.Model):
    """Client business information"""

    business_name = models.CharField(max_length=25)
    business_email = models.CharField(max_length=250)
    reg_number = models.CharField(max_length=250)
    vat_number = models.CharField(max_length=250)
    phone_no = models.CharField(max_length=250)

    # Foreign  key(s) to the business model
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for business"""
        verbose_name = "Business"
        verbose_name_plural = "Businesses"

    def __str__(self):
        """Return the business name"""
        return str(self.business_name)


class Assessment(models.Model):
    """Assessment on google notes"""
    message = models.CharField(max_length=254)
    scheduled_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    event_id = models.CharField(max_length=254)
    summary = models.CharField(max_length=254)
    video_link = models.CharField(max_length=254)
    client_location = models.CharField(max_length=254)

    # Foreign  key(s) to the assessment model
    application = models.OneToOneField(Application, on_delete=models.CASCADE,
                                       related_name='application')

    class Meta:
        """Metaclass for assessment"""
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"

    def __str__(self):
        """Return the assessment message"""
        return str(self.message)


class TwilioRoom(models.Model):
    """Twilio room model for the application"""
    room_name = models.CharField(max_length=250)
    room_sid = models.CharField(max_length=250)
    room_status = models.CharField(max_length=250)

    # Foreign  key(s) to the twilio room model
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for twilio room"""
        verbose_name = "Twilio Room"
        verbose_name_plural = "Twilio Rooms"

    def __str__(self):
        """Return the room name"""
        return str(self.room_name)


class TwilioRecording(models.Model):
    """Twilio recording model for the application"""
    recording_sid = models.CharField(max_length=250)
    recording_url = models.CharField(max_length=250)

    # Foreign  key(s) to the twilio recording model
    twilio_room = models.OneToOneField(TwilioRoom, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for twilio recording"""
        verbose_name = "Twilio Recording"
        verbose_name_plural = "Twilio Recordings"

    def __str__(self):
        """Return the recording sid"""
        return str(self.recording_sid)
