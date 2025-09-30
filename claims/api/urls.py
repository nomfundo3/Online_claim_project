"""
Urls for claim app api views for external and internal use.
"""
from django.urls import path
from claims.api import views

urlpatterns = [
    path('add_claim_client_api/', views.add_claim_client_api, name='add_claim_client_api'),
    path('add_claim_business_api/', views.add_claim_business_api, name='add_claim_business_api'),

    path('add_cause_category_api/', views.add_cause_category_api, name="add_cause_category_api"),
    path('edit_cause_category_api/', views.edit_cause_category_api,
         name="edit_cause_category_api"),
    path('del_cause_category_api/', views.del_cause_category_api, name="del_cause_category_api"),

    path('add_how_category_api/', views.add_how_category_api, name="add_how_category_api"),
    path('edit_how_category_api/', views.edit_how_category_api, name="edit_how_category_api"),
    path('del_how_category_api/', views.del_how_category_api, name="del_how_category_api"),

    path('add_what_category_api/', views.add_what_category_api, name="add_what_category_api"),
    path('edit_what_category_api/', views.edit_what_category_api, name="edit_what_category_api"),
    path('del_what_category_api/', views.del_what_category_api, name="del_what_category_api"),

    path('get_claim_categories_api/', views.get_claim_categories_api,
         name="get_claim_categories_api"),

    path('get_all_claims_api/', views.get_all_claims_api, name="get_all_claims_api"),

    path('get_all_assessors_api/', views.get_all_assessors_api,
         name="get_all_assessors_api"),

    path('manage_application_api/', views.manage_application_api, name="manage_application_api"),

    path('change_application_type_api/', views.change_application_type_api,
         name="change_application_type_api"),

    path('application_type_categories_api/', views.application_type_categories_api,
         name="application_type_categories_api"),

    path('assign_what_application_api/', views.assign_what_application_api,
         name="assign_what_application_api"),

    path('assign_how_application_api/', views.assign_how_application_api,
         name="assign_how_application_api"),

    path('assign_cause_application_api/', views.assign_cause_application_api,
         name="assign_cause_application_api"),

    path('what_category_questions_api/', views.what_category_questions_api,
         name="what_category_questions_api"),

    path('how_category_questions_api/', views.how_category_questions_api,
         name="how_category_questions_api"),

    path('create_what_title_api/', views.create_what_title_api, name="create_what_title_api"),

    path('create_question_what_api/', views.create_question_what_api,
         name="create_question_what_api"),

    path('create_how_title_api/', views.create_how_title_api, name="create_how_title_api"),

    path('create_question_how_api/', views.create_question_how_api,
         name="create_question_how_api"),
    path('get_claim_questions_api/', views.get_claim_questions_api,
         name="get_claim_questions_api"),
    path('save_claim_questions_api/', views.save_claim_questions_api,
         name="save_claim_questions_api"),

    path('edit_title_what_api/', views.edit_title_what_api, name="edit_title_what_api"),
    path('edit_title_how_api/', views.edit_title_how_api, name="edit_title_how_api"),
    path('delete_title_what_api/', views.delete_title_what_api, name="delete_title_what_api"),
    path('delete_title_how_api/', views.delete_title_how_api, name="delete_title_how_api"),

    path('edit_how_question_api/', views.edit_how_question_api, name="edit_how_question_api"),
    path('edit_what_question_api/', views.edit_what_question_api, name="edit_what_question_api"),

    path('delete_what_question_api/', views.delete_what_question_api,
         name="delete_what_question_api"),
    path('delete_how_question_api/', views.delete_how_question_api, name="delete_how_question_api"),
    path('edit_client_application_api/', views.edit_client_application_api, name="edit_client_application_api"),
    path('edit_business_application_api/', views.edit_business_application_api, name="edit_business_application_api"),
    path('edit_claim_application_api/', views.edit_claim_application_api, name="edit_claim_application_api"),


    path('generate_report_claim_api/', views.generate_report_claim_api, name="generate_report_claim_api"),
    path('preview_report_claim_api/', views.preview_report_claim_api, name="preview_report_claim_api"),
    path('get_claim_info_api/', views.get_claim_info_api, name="get_claim_info_api"),
    path('create_sub_claim_api/', views.create_sub_claim_api, name="create_sub_claim_api"),
    path('get_claim_application_api/', views.get_claim_application_api, name="get_claim_application_api"),
    
    path('report_single_claim_api/', views.report_single_claim_api, name="report_single_claim_api"),
    path('get_client_claims_api/', views.get_client_claims_api, name="get_client_claims_api"),
    
    
]
