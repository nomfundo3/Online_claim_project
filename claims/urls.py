"""
The `urls.py` module defines the URL patterns for the application.

The URL patterns define the routes that are available in the application,
as well as the views that are associated with those routes.
"""
from django.urls import path
from claims import views

urlpatterns = [
    path('add_claim_client/', views.add_claim_client, name="add_claim_client"),
    path('claim_client_add/', views.claim_client_add, name="claim_client_add"),

    path('add_cause_category/', views.add_cause_category, name="add_cause_category"),
    path('edit_cause_category/', views.edit_cause_category, name="edit_cause_category"),
    path('del_cause_category/', views.del_cause_category, name="del_cause_category"),

    path('add_how_category/', views.add_how_category, name="add_how_category"),
    path('edit_how_category/', views.edit_how_category, name="edit_how_category"),
    path('del_how_category/', views.del_how_category, name="del_how_category"),

    path('add_what_category/', views.add_what_category, name="add_what_category"),
    path('edit_what_category/', views.edit_what_category, name="edit_what_category"),
    path('del_what_category/', views.del_what_category, name="del_what_category"),

    path('manage_claims/', views.manage_claims, name="manage_claims"),
    path('all_claims/', views.all_claims, name="all_claims"),
    
    path('assessor_claims/', views.assessor_claims, name="assessor_claims"),
    path('manage_application/<int:application_id>',
         views.manage_application, name="manage_application"),
    path('assessment_preview/<int:application_id>',
         views.assessment_preview, name="assessment_preview"),

    path('change_application_type/', views.change_application_type, name="change_application_type"),

    path('assign_what_application/', views.assign_what_application, name="assign_what_application"),
    path('assign_how_application/', views.assign_how_application, name="assign_how_application"),
    path('assign_cause_application/', views.assign_cause_application,
         name="assign_cause_application"),

    path('create_what_title/', views.create_what_title, name="create_what_title"),
    path('create_what_question/', views.create_what_question, name="create_what_question"),
    path('create_how_title/', views.create_how_title, name="create_how_title"),
    path('create_how_question/', views.create_how_question, name="create_how_question"),

    path('what_category_questions/<int:what_id>', views.what_category_questions,
         name="what_category_questions"),
    path('how_category_questions/<int:how_id>', views.how_category_questions,
         name="how_category_questions"),

    path('save_claim_questions/', views.save_claim_questions, name="save_claim_questions"),
    path('edit_title_what/', views.edit_title_what, name="edit_title_what"),
    path('edit_title_how/', views.edit_title_how, name="edit_title_how"),
    path('delete_title_what/', views.delete_title_what, name="delete_title_what"),
    path('delete_title_how/', views.delete_title_how, name="delete_title_how"),

    path('edit_how_question/', views.edit_how_question, name="edit_how_question"),
    path('edit_what_question/', views.edit_what_question, name="edit_what_question"),

    path('delete_how_question/', views.delete_how_question, name="delete_how_question"),
    path('delete_what_question/', views.delete_what_question, name="delete_what_question"),
    path('edit_client_application/', views.edit_client_application, name="edit_client_application"),
    path('edit_business_application/', views.edit_business_application, name="edit_business_application"),
    path('edit_claim_application/', views.edit_claim_application, name="edit_claim_application"),
    path('generate_report_claim/<int:application_id>', views.generate_report_claim, name="generate_report_claim"),

    path('create_sub_claim/', views.create_sub_claim, name="create_sub_claim"),
    path('get_claim_application/', views.get_claim_application, name="get_claim_application"),

    path('report_single_claim/', views.report_single_claim, name="report_single_claim"),
    
    path('get_client_claims/', views.get_client_claims, name="get_client_claims"),
    
]
