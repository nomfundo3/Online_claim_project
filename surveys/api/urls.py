"""
Urls for survey app api views for external and internal use.
"""
from django.urls import path
from surveys.api import views

urlpatterns = [
    
    path('get_survey_overview_api/', views.get_survey_overview_api, name="get_survey_overview_api"),
    path('surveys_api/', views.surveys_api, name="surveys_api"),
    path('add_survey_client_api/', views.add_survey_client_api, name="add_survey_client_api"),
    path('view_survey_application_api/',
         views.view_survey_application_api, name="view_survey_application_api"),
    path('survey_category_questions_api/',
         views.survey_category_questions_api, name="survey_category_questions_api"),
    path('change_assessor_api/', views.change_assessor_api, name="change_assessor_api"),
    path('add_survey_category_api/', views.add_survey_category_api, name="add_survey_category_api"),
    path('update_survey_category_api/', views.update_survey_category_api,
         name="update_survey_category_api"),
    path('delete_survey_category_api/', views.delete_survey_category_api,
         name="delete_survey_category_api"),
    path('add_survey_category_type_api/', views.add_survey_category_type_api,
         name="add_survey_category_type_api"),
    path('update_survey_category_type_api/', views.update_survey_category_type_api,
         name="update_survey_category_type_api"),
    path('delete_survey_category_type_api/', views.delete_survey_category_type_api,
         name="delete_survey_category_type_api"),
    path('add_survey_title_api/', views.add_survey_title_api, name="add_survey_title_api"),
    path('update_survey_title_api/', views.update_survey_title_api, name="update_survey_title_api"),
    path('delete_survey_title_api/', views.delete_survey_title_api, name="delete_survey_title_api"),
    path('generate_report_api/', views.generate_report_api, name="generate_report_api"),
    path('survey_answer_api/', views.survey_answer_api, name="survey_answer_api"),

    path('get_survey_types_api/', views.get_survey_types_api, name="get_survey_types_api"),

    path('get_survey_categories_api/', views.get_survey_categories_api,
         name="get_survey_categories_api"),

    path('get_survey_titles_api/', views.get_survey_titles_api, name="get_survey_titles_api"),

    path('get_survey_questions_api/', views.get_survey_questions_api,
         name="get_survey_questions_api"),

    path('create_question_survey_api/', views.create_question_survey_api,
         name="create_question_survey_api"),

    path('add_survey_business_api/', views.add_survey_business_api,
         name="add_survey_business_api"),

    path('survey_application_management_api/', views.survey_application_management_api,
         name="survey_application_management_api"),
     
     path('save_survey_questions_api/', views.save_survey_questions_api,
         name="save_survey_questions_api"),
     
     path('delete_survey_question_api/', views.delete_survey_question_api, name="delete_survey_question_api"),
     path('update_survey_question_api/', views.update_survey_question_api, name="update_survey_question_api"),
     path('edit_client_application_api/', views.edit_client_application_api, name="edit_client_application_api"),
     path('edit_business_application_api/', views.edit_business_application_api, name="edit_business_application_api"),

     path('change_survey_type_api/', views.change_survey_type_api, name="change_survey_type_api"),
     path('get_survey_info_api/', views.get_survey_info_api, name="get_survey_info_api"),

     
     path('create_multi_survey_api/', views.create_multi_survey_api, name="create_multi_survey_api"),
     path('survey_report_single_api/', views.survey_report_single_api, name="survey_report_single_api"),

]
