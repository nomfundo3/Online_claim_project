"""
Models for claim management of applications of type survey.
"""
from django.db import models
from application.models import (
    Application,
    ApplicationType,
    Assessment
)
# Create your models here.


class Claim(models.Model):
    """claim process overview"""
    application_type = models.ForeignKey(
        ApplicationType, 
        on_delete=models.CASCADE
    )
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE
    )
    
    class Meta:
        """
        Metaclass for claim applications.
        """
        verbose_name = "Claim"
        verbose_name_plural = "Claims"

    def __str__(self):
        """
        String representation of claim application.
        """""
        return f"{self.application}"


class CauseCategory(models.Model):
    """
    Model for claim management of applications of type claim.
    """
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Key(s)
    application_type = models.ForeignKey(ApplicationType, 
                                         on_delete=models.CASCADE
                                         )
    
    class Meta:
        """
        Metaclass for claim application.
        """
        verbose_name = "Cause Category"
        verbose_name_plural = "Cause Categories"

    def __str__(self):
        """
        String representation of claim application.
        """""
        return f"{self.name}"


class WhatCategory(models.Model):
    """
    Model for claim management of applications of type claim.
    """
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Key
    cause = models.ForeignKey(CauseCategory, on_delete=models.CASCADE)

    class Meta:
        """
        Metaclass for claim application.
        """
        verbose_name = "What Category"
        verbose_name_plural = "What Categories"

    def __str__(self):
        """
        String representation of claim application.
        """""
        return f"{self.name}"


class HowCategory(models.Model):
    """
    Model for claim management of applications of type claim.
    """
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Key
    cause = models.ForeignKey(CauseCategory, on_delete=models.CASCADE)

    class Meta:
        """
        Metaclass for claim application.
        """
        verbose_name = "How Category"
        verbose_name_plural = "How Categories"

    def __str__(self):
        """
        String representation of claim application.
        """""
        return f"{self.name}"


class ApplicationWhat(models.Model):
    """
    Model for claim management of applications of type claim.
    """
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    what = models.ForeignKey(WhatCategory, on_delete=models.CASCADE)

    class Meta:
        """
        Metaclass for claim application.
        """
        verbose_name = "Application What"
        verbose_name_plural = "Application Whats"

    def __str__(self):
        """
        String representation of claim application.
        """""
        return f"{self.claim}"


class ApplicationHow(models.Model):
    """
    Model for claim management of applications of type claim.
    """
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    how = models.ForeignKey(HowCategory, on_delete=models.CASCADE)

    class Meta:
        """
        Metaclass for claim application.
        """
        verbose_name = "Application How"
        verbose_name_plural = "Application Hows"

    def __str__(self):
        """
        String representation of claim application.
        """""
        return f"{self.claim}"


class ApplicationCause(models.Model):
    """
    Model for claim management of applications of type claim.
    """
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    cause = models.ForeignKey(CauseCategory, on_delete=models.CASCADE)

    class Meta:
        """
        Metaclass for claim application.
        """
        verbose_name = "Application Cause"
        verbose_name_plural = "Application Causes"

    def __str__(self):
        """
        String representation of claim application.
        """""
        return f"{self.claim}"


class HowQuestionTitle(models.Model):
    """
    Model for the assignment of how question titles
    """
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Key
    how = models.ForeignKey(HowCategory, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for model how question titles"""
        verbose_name = "How Title"
        verbose_name_plural = "How Titles"

    def __str__(self):
        """String representation of how question titles."""
        return str(self.title)


class HowQuestion(models.Model):
    """
    Model for the creation of how questions
    """
    question = models.CharField(max_length=254)
    question_type = models.CharField(max_length=254)
    is_mandatory = models.BooleanField(default=False)
    has_checkbox = models.BooleanField(default=False)
    has_selection = models.BooleanField(default=False)
    has_text = models.BooleanField(default=False)
    has_date = models.BooleanField(default=False)
    has_file = models.BooleanField(default=False)
    has_other_field = models.BooleanField(default=False)
    has_location = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Key
    how_title = models.ForeignKey(HowQuestionTitle, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for model how question titles"""
        verbose_name = "How Question"
        verbose_name_plural = "How Questions"

    def __str__(self):
        """String representation of how question."""
        return str(self.question)


class HowQuestionOption(models.Model):
    """Model for How question options for selection and checkbox fields."""
    option = models.CharField(max_length=254)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Keys
    question = models.ForeignKey(
        HowQuestion,
        on_delete=models.CASCADE
    )

    class Meta:
        """Metaclass for HowQuestionOption."""
        verbose_name = 'How Question Option'
        verbose_name_plural = 'How Question Options'

    def __str__(self):
        """String representation of HowQuestionOption."""
        return self.option


class HowQuestionAnswer(models.Model):
    """Model for How answers."""
    answer = models.CharField(max_length=254)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Keys
    question = models.ForeignKey(
        HowQuestion,
        on_delete=models.CASCADE
    )
    claim = models.ForeignKey(
        Claim,
        on_delete=models.CASCADE
    )

    class Meta:
        """Metaclass for HowAnswers."""
        verbose_name = 'How Answer'
        verbose_name_plural = 'How Answers'

    def __str__(self):
        """String representation of HowAnswers."""
        return str(self.answer)


class WhatQuestionTitle(models.Model):
    """
    Model for the assignment of what question titles
    """
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Key
    what = models.ForeignKey(WhatCategory, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for model what question titles"""
        verbose_name = "What Title"
        verbose_name_plural = "What Titles"

    def __str__(self):
        """String representation of what question titles."""
        return str(self.title)


class WhatQuestion(models.Model):
    """
    Model for the creation of what questions
    """
    question = models.CharField(max_length=254)
    question_type = models.CharField(max_length=254)
    is_mandatory = models.BooleanField(default=False)
    has_checkbox = models.BooleanField(default=False)
    has_selection = models.BooleanField(default=False)
    has_text = models.BooleanField(default=False)
    has_date = models.BooleanField(default=False)
    has_file = models.BooleanField(default=False)
    has_other_field = models.BooleanField(default=False)
    has_location = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Key
    what_title = models.ForeignKey(WhatQuestionTitle, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for model what question titles"""
        verbose_name = "What Question"
        verbose_name_plural = "What Questions"

    def __str__(self):
        """String representation of what question."""
        return str(self.question)


class WhatQuestionOption(models.Model):
    """Model for What question options for selection and checkbox fields."""
    option = models.CharField(max_length=254)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Keys
    question = models.ForeignKey(
        WhatQuestion,
        on_delete=models.CASCADE
    )

    class Meta:
        """Metaclass for WhatQuestionOption."""
        verbose_name = 'What Question Option'
        verbose_name_plural = 'What Question Options'

    def __str__(self):
        """String representation of WhatQuestionOption."""
        return self.option


class WhatQuestionAnswer(models.Model):
    """Model for What answers."""
    answer = models.CharField(max_length=254)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Keys
    question = models.ForeignKey(
        WhatQuestion,
        on_delete=models.CASCADE
    )
    claim = models.ForeignKey(
        Claim,
        on_delete=models.CASCADE
    )

    class Meta:
        """Metaclass for WhatAnswers."""
        verbose_name = 'What Answer'
        verbose_name_plural = 'What Answers'

    def __str__(self):
        """String representation of WhatAnswers."""
        return self.answer


class AssessmentNote(models.Model):
    """Assessment notes for the scheduled assessment"""
    note = models.CharField(max_length=254)
    file = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign  key(s) to the assessment note model
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)

    class Meta:
        """Metaclass for assessment note"""
        verbose_name = "Assessment Note"
        verbose_name_plural = "Assessment Notes"

    def __str__(self):
        """Return the assessment note"""
        return self.note
