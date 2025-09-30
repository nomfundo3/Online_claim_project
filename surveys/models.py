"""
Models for survey management of applications of type survey.
"""
from django.db import models
from application.models import (
    Application, 
    ApplicationType
)

class Survey(models.Model):
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
        Metaclass for Survey applications.
        """
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"

    def __str__(self):
        """
        String representation of Survey application.
        """""
        return f"{self.application}"


class SurveyCategory(models.Model):
    """Model for survey categories e.g. Risk, Inspection, etc."""
    name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Keys
    type = models.ForeignKey(
        ApplicationType,
        on_delete=models.CASCADE,
        related_name='survey_type'
    )

    class Meta:
        """Metaclass for SurveyCategory."""
        verbose_name = 'Survey Category'
        verbose_name_plural = 'Survey Categories'

    def __str__(self):
        """String representation of SurveyCategory."""
        return f"{self.name}"


class SurveyCategoryType(models.Model):
    """Model for survey category types e.g. location, security etc."""
    name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Keys
    category = models.ForeignKey(
        SurveyCategory,
        on_delete=models.CASCADE,
        related_name='subcategory_category'
    )

    class Meta:
        """Metaclass for SurveyCategoryType."""
        verbose_name = 'Survey Category Type'
        verbose_name_plural = 'Survey Category Types'

    def __str__(self):
        """String representation of SurveyCategoryType."""
        return f"{self.name}"


class SurveyApplicationTitle(models.Model):
    """Model for application title e.g. Business, Flammables etc."""
    name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Keys
    subcategory_type = models.ForeignKey(
        SurveyCategoryType,
        on_delete=models.CASCADE,
        related_name='application_subcategory_type'
    )

    class Meta:
        """Metaclass for SurveyApplicationTitle."""
        verbose_name = 'Survey Application Title'
        verbose_name_plural = 'Survey Application Titles'

    def __str__(self):
        """String representation of SurveyApplicationTitle."""
        return f"{self.name}"


class SurveyQuestion(models.Model):
    """Model for survey questions."""
    question = models.CharField(max_length=254)
    number = models.IntegerField(default=0000)
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

    #  Foreign Keys
    application_title = models.ForeignKey(
        SurveyApplicationTitle,
        on_delete=models.CASCADE,
        related_name='question_application_title'
    )

    class Meta:
        """Metaclass for SurveyQuestions."""
        verbose_name = 'Survey Question'
        verbose_name_plural = 'Survey Questions'

    def __str__(self):
        """String representation of SurveyQuestions."""
        return f"{self.question}"


class SurveyQuestionOption(models.Model):
    """Model for survey question options for selection and checkbox fields."""
    option = models.CharField(max_length=254)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Keys
    question = models.ForeignKey(
        SurveyQuestion,
        on_delete=models.CASCADE,
        related_name='option_question'
    )

    class Meta:
        """Metaclass for SurveyQuestionOption."""
        verbose_name = 'Survey Question Option'
        verbose_name_plural = 'Survey Question Options'

    def __str__(self):
        """String representation of SurveyQuestionOption."""
        return f"{self.option}"


class SurveyAnswer(models.Model):
    """Model for survey answers."""
    answer = models.CharField(max_length=254)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # Foreign Keys
    question = models.ForeignKey(
        SurveyQuestion,
        on_delete=models.CASCADE,
        related_name='answer_question'
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='answer_application'
    )
    category = models.ForeignKey(
        SurveyCategory,
        on_delete=models.CASCADE,
        related_name='answer_category'
    )
    subcategory_type = models.ForeignKey(
        SurveyCategoryType,
        on_delete=models.CASCADE,
        related_name='answer_subcategory_type'
    )
    application_title = models.ForeignKey(
        SurveyApplicationTitle,
        on_delete=models.CASCADE,
        related_name='answer_application_title'
    )

    class Meta:
        """Metaclass for SurveyAnswers."""
        verbose_name = 'Survey Answer'
        verbose_name_plural = 'Survey Answers'

    def __str__(self):
        """String representation of SurveyAnswers."""
        return f"{self.answer}"
